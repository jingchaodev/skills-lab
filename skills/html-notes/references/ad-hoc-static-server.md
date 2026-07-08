# workspace wiki HTML companion: ad-hoc browser-openable server fallback

Use this when a workspace wiki HTML companion exists under `<wiki-root>/...`, but no dashboard/wiki server is currently reachable and the user still needs a browser-openable URL.

## Pattern

Serve the workspace wiki root over the chosen local/private static-server host with a tiny static server that preserves the chosen hosted-path convention.

```python
#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote
import os

ROOT = Path('<wiki-root>').resolve()

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?', 1)[0].split('#', 1)[0]
        path = unquote(path)
        rel = path.removeprefix('/w/').lstrip('/')
        target = (ROOT / rel).resolve()
        if ROOT not in target.parents and target != ROOT:
            return str(ROOT / '__forbidden__')
        return str(target)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

if __name__ == '__main__':
    host = os.environ.get('HOST', '<host>')
    port = int(os.environ.get('PORT', '8123'))
    print(f'serving {ROOT} at http://{host}:{port}/', flush=True)
    ThreadingHTTPServer((host, port), Handler).serve_forever()
```

## Steps

1. Choose a reachable host/interface (`127.0.0.1` for local-only, a private-network IP for another device, or a public host only when explicitly intended).
2. Write the server script outside the skill/wiki content area, e.g. `<tmp-dir>/serve_notes.py`.
3. Start it as a long-lived background process bound to that host/interface.
4. Verify both routes with `curl -I`:
   - `http://<host>:8123<served-notes-url>/_html/<note>.html`
   - `http://<host>:8123<served-notes-url>/<source>.md` or the relevant source path.
5. Report the served HTML URL, not a `file://` path.

## Guardrails

- This is a fallback for reading-layer delivery, not a replacement for the real wiki/static-site host.
- Do not expose `0.0.0.0` unless explicitly asked; prefer the chosen host/interface.
- Keep the server root locked to `<wiki-root>` and reject path traversal.
- Use `Cache-Control: no-store` so readers see fresh HTML during iterative note patches.
