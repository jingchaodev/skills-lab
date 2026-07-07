#!/usr/bin/env node
/**
 * web-fetch — fetch a web page and extract readable text. Zero dependencies.
 *
 * Usage:
 *   ./fetch.js <url>            # extract readable text (default)
 *   ./fetch.js <url> --raw      # emit raw HTML
 *   ./fetch.js <url> --links    # list all links (text -> href)
 *
 * The text extractor strips scripts/styles/nav/boilerplate and collapses
 * whitespace. It's heuristic, not a full Readability port, but handles docs,
 * blog posts, and READMEs well.
 */

'use strict';

function parseArgs(argv) {
  const opts = { url: null, raw: false, links: false };
  for (const a of argv) {
    if (a === '--raw') opts.raw = true;
    else if (a === '--links') opts.links = true;
    else if (a === '-h' || a === '--help') opts.help = true;
    else if (!opts.url) opts.url = a;
  }
  return opts;
}

function decodeEntities(str) {
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(parseInt(d, 10)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
}

function extractText(html) {
  let s = html;
  // Drop non-content elements entirely.
  s = s.replace(/<script[\s\S]*?<\/script>/gi, ' ');
  s = s.replace(/<style[\s\S]*?<\/style>/gi, ' ');
  s = s.replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ');
  s = s.replace(/<head[\s\S]*?<\/head>/gi, ' ');
  s = s.replace(/<nav[\s\S]*?<\/nav>/gi, ' ');
  s = s.replace(/<footer[\s\S]*?<\/footer>/gi, ' ');
  s = s.replace(/<header[\s\S]*?<\/header>/gi, ' ');
  s = s.replace(/<aside[\s\S]*?<\/aside>/gi, ' ');
  s = s.replace(/<!--[\s\S]*?-->/g, ' ');
  // Turn block-level closes into newlines so structure survives.
  s = s.replace(/<\/(p|div|section|article|li|h[1-6]|tr|br|pre|blockquote)\s*>/gi, '\n');
  s = s.replace(/<br\s*\/?>/gi, '\n');
  // Strip remaining tags.
  s = s.replace(/<[^>]+>/g, ' ');
  s = decodeEntities(s);
  // Normalize whitespace: collapse spaces, cap consecutive blank lines.
  s = s.replace(/[ \t]+/g, ' ');
  s = s.replace(/ *\n */g, '\n');
  s = s.replace(/\n{3,}/g, '\n\n');
  return s.trim();
}

function extractLinks(html, baseUrl) {
  const out = [];
  const re = /<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    let href = decodeEntities(m[1]);
    const text = decodeEntities(m[2].replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
    if (href.startsWith('#') || href.startsWith('javascript:')) continue;
    try { href = new URL(href, baseUrl).href; } catch { /* keep as-is */ }
    out.push({ text: text || '(no text)', href });
  }
  return out;
}

const HELP = `web-fetch — fetch a page and extract readable text (zero dependencies)

Usage:
  fetch.js <url>          # extract readable text (default)
  fetch.js <url> --raw    # raw HTML
  fetch.js <url> --links  # list links as "text -> href"
`;

(async () => {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help || !opts.url) {
    process.stdout.write(HELP);
    process.exit(opts.url ? 0 : 1);
  }
  try {
    const res = await fetch(opts.url, {
      redirect: 'follow',
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
      },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
    const html = await res.text();

    if (opts.raw) {
      process.stdout.write(html);
    } else if (opts.links) {
      for (const l of extractLinks(html, res.url || opts.url)) {
        process.stdout.write(`${l.text} -> ${l.href}\n`);
      }
    } else {
      process.stdout.write(extractText(html) + '\n');
    }
  } catch (err) {
    process.stderr.write(`web-fetch error: ${err.message}\n`);
    process.exit(1);
  }
})();
