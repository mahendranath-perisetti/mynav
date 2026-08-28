import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path.startswith('/sheet-data'):
            self.handle_sheet_data()
            return
        super().do_GET()

    def handle_sheet_data(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        sheet_url = params.get('url', [None])[0]

        if not sheet_url:
            self.send_error(400, 'Missing url query parameter')
            return

        try:
            request = urllib.request.Request(
                sheet_url,
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Accept': 'text/csv,text/plain,*/*'
                }
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = response.read()
                content_type = response.headers.get_content_type()
                charset = response.headers.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='replace')

            self.send_response(200)
            self.send_header('Content-Type', f'{content_type}; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body.encode('utf-8'))
        except Exception as exc:
            self.send_error(502, f'Unable to fetch sheet: {exc}')


if __name__ == '__main__':
    port = 8000
    server = ThreadingHTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f'Serving on http://0.0.0.0:{port}/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')
        server.server_close()
