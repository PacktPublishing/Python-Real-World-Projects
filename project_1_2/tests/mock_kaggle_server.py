"""
    Python Real-World Projects
    Project 1.2: Acquire data from web service
"""
"""
Example headers from datasets/list request

Query: GET https://www.kaggle.com/api/v1/datasets/list?user=carlmcbrideellis&page=1
  'Content-Type': 'application/json'
  'Date': 'Thu, 26 Jan 2023 16:05:40 GMT'
  'Access-Control-Allow-Credentials': 'true'
  'Content-Encoding': 'br'
  'Set-Cookie': 'ka_sessionid=12b3101f27c9e87d7199fcc570ae6bda; max-age=2626560; path=/, GCLB=CLzXifGh49P1QQ; path=/; HttpOnly'
  'Transfer-Encoding': 'chunked'
  'Vary': 'Accept-Encoding'
  'Turbolinks-Location': 'https://www.kaggle.com/api/v1/datasets/list?user=carlmcbrideellis&page=1'
  'X-Kaggle-MillisecondsElapsed': '364'
  'X-Kaggle-RequestId': '6779bd23d387c911743e8ba9f4b657dd'
  'X-Kaggle-ApiVersion': '1.5.12'
  'X-Frame-Options': 'SAMEORIGIN'
  'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload'
  'Content-Security-Policy': "object-src 'none'; script-src 'nonce-5ExpnWEdmsjwQc3OnS2Wug==' 'report-sample' 'unsafe-inline' 'unsafe-eval' 'strict- [...]"
  'X-Content-Type-Options': 'nosniff'
  'Referrer-Policy': 'strict-origin-when-cross-origin'
  'Via': '1.1 google'
  'Alt-Svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'

"""
import csv
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import json
from pathlib import Path
import urllib.parse
import zipfile

class KaggleServer(BaseHTTPRequestHandler):
    """
    See https://github.com/Kaggle/kaggle-api/blob/master/KaggleSwagger.yaml

    JSON datasets look at only a few attributes: title, ref, url, totalBytes
    """
    def do_GET(self):
        if self.path.startswith("/api/v1/datasets/list"):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            page = int(query.get('page', ['1'])[0])
            if page == 1:
                self.send_response(200,'OK')
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                str_content = json.dumps([{'title': 'example1'}, {'title': 'example2'}])
                self.wfile.write(str_content.encode('utf-8'))
            elif page == 2:
                self.send_response(429, "Too Many Requests")
                self.send_header("Retry-After", "30")
                self.end_headers()
            else:
                # Final
                self.send_response(200, 'OK')
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'[]')
        elif self.path.startswith("/api/v1/datasets/download"):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.split('/')
            if path[-2:] == ["carlmcbrideellis", "data-anscombes-quartet"]:
                self.send_response(200,'OK')
                self.send_header("Content-Type", "application/zip")
                self.end_headers()
                zip_content = io.BytesIO()
                with zipfile.ZipFile(zip_content, 'w') as archive:
                    target_path = zipfile.Path(archive, 'Anscombe_quartet_data.csv')
                    with target_path.open('w') as member_file:
                        writer = csv.writer(member_file)
                        writer.writerow(['mock', 'data'])
                        writer.writerow(['line', 'two'])
                # write ZIP Archive to wfile
                self.wfile.write(zip_content.getvalue())
                self.wfile.flush()
                self.close_connection = True
            else:
                self.send_error(404, f"Unknown dataset {path}")
        elif self.path.startswith("/api/v1/datasets/metadata"):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.split('/')
            if path[-2:] == ["carlmcbrideellis", "data-anscombes-quartet"]:
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                str_content = json.dumps({"name": "Data: Anscombe's quartet"})
                self.wfile.write(str_content.encode('utf-8'))
            else:
                self.send_error(404, f"Unknown dataset {path}")
        else:
            self.log_error("Unknown path: %s", self.path)
            self.send_error(404, f"Unknown path {self.path}")

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8080), KaggleServer)
    server.serve_forever()
