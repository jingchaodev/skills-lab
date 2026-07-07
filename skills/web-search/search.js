#!/usr/bin/env node
/**
 * web-search — DuckDuckGo search with zero dependencies.
 *
 * Usage:
 *   ./search.js "query terms"
 *   ./search.js -n 10 "query terms"
 *   ./search.js --json "query terms"
 *
 * Hits DuckDuckGo's no-JS HTML endpoint and parses results out of the markup.
 * Prints title, URL, and snippet for each result.
 */

'use strict';

function parseArgs(argv) {
  const opts = { n: 5, json: false, query: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-n' || a === '--num') {
      opts.n = parseInt(argv[++i], 10) || 5;
    } else if (a === '--json') {
      opts.json = true;
    } else if (a === '-h' || a === '--help') {
      opts.help = true;
    } else {
      opts.query.push(a);
    }
  }
  opts.query = opts.query.join(' ').trim();
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
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(parseInt(d, 10)));
}

function stripTags(html) {
  return decodeEntities(html.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
}

// DuckDuckGo wraps outbound links as /l/?uddg=<encoded-real-url>
function unwrapDdgUrl(href) {
  const m = href.match(/[?&]uddg=([^&]+)/);
  if (m) {
    try { return decodeURIComponent(m[1]); } catch { /* fall through */ }
  }
  return href.startsWith('//') ? 'https:' + href : href;
}

function parseResults(html, limit) {
  const results = [];
  // Each result is an <a class="result__a" href="...">title</a> followed by
  // a <a class="result__snippet">snippet</a>.
  const linkRe = /<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g;
  const snippetRe = /<a[^>]+class="result__snippet"[^>]*>([\s\S]*?)<\/a>/g;

  const links = [];
  let m;
  while ((m = linkRe.exec(html)) !== null) {
    links.push({ url: unwrapDdgUrl(decodeEntities(m[1])), title: stripTags(m[2]) });
  }
  const snippets = [];
  while ((m = snippetRe.exec(html)) !== null) {
    snippets.push(stripTags(m[1]));
  }

  for (let i = 0; i < links.length && results.length < limit; i++) {
    if (!links[i].title || !links[i].url) continue;
    results.push({
      title: links[i].title,
      url: links[i].url,
      snippet: snippets[i] || '',
    });
  }
  return results;
}

async function search(query, limit) {
  const url = 'https://html.duckduckgo.com/html/?q=' + encodeURIComponent(query);
  const res = await fetch(url, {
    headers: {
      'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
      'Accept': 'text/html',
    },
  });
  if (!res.ok) throw new Error(`DuckDuckGo returned HTTP ${res.status}`);
  const html = await res.text();
  return parseResults(html, limit);
}

const HELP = `web-search — DuckDuckGo search (zero dependencies)

Usage:
  search.js "query terms"
  search.js -n <count> "query terms"   # number of results (default 5)
  search.js --json "query terms"       # machine-readable JSON output
`;

(async () => {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help || !opts.query) {
    process.stdout.write(HELP);
    process.exit(opts.query ? 0 : 1);
  }
  try {
    const results = await search(opts.query, opts.n);
    if (opts.json) {
      process.stdout.write(JSON.stringify(results, null, 2) + '\n');
      return;
    }
    if (results.length === 0) {
      process.stdout.write('No results.\n');
      return;
    }
    results.forEach((r, i) => {
      process.stdout.write(`${i + 1}. ${r.title}\n   ${r.url}\n`);
      if (r.snippet) process.stdout.write(`   ${r.snippet}\n`);
      process.stdout.write('\n');
    });
  } catch (err) {
    process.stderr.write(`web-search error: ${err.message}\n`);
    process.exit(1);
  }
})();
