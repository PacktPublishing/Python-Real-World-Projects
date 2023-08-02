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
import io
import json
import zipfile
from bottle import route, run, request, HTTPResponse

@route('/api/v1/datasets/list')
def datasets_list(name):
    page = request.query.page or '1'
    if page == '1':
        mock_body = [
            {'title': 'example1'},
            {'title': 'example2'}
        ]
        response = HTTPResponse(
            body=json.dumps(mock_body),
            status=200,
            headers={'Content-Type': 'application/json'}
        )
    elif page == '2':
        response = HTTPResponse(
            status=429,
            headers={'Retry-After': '30'}
        )
    else:
        response = HTTPResponse(
            body=json.dumps([]),
            status=200,
            headers={'Content-Type': 'application/json'}
        )
    return response

@route('/api/v1/datasets/download/<ownerSlug>/<datasetSlug>')
def datasets_download(ownerSlug, datasetSlug):
    if ownerSlug == "carlmcbrideellis" and datasetSlug == "data-anscombes-quartet":
        zip_content = io.BytesIO()
        with zipfile.ZipFile(zip_content, 'w') as archive:
            target_path = zipfile.Path(archive, 'Anscombe_quartet_data.csv')
            with target_path.open('w') as member_file:
                writer = csv.writer(member_file)
                writer.writerow(['mock', 'data'])
                writer.writerow(['line', 'two'])
        response = HTTPResponse(
            body=zip_content.getvalue(),
            status=200,
            headers={"Content-Type": "application/zip"}
        )
        return response
    # All other requests...
    response = HTTPResponse(
        status=404
    )
    return response

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080)
