import requests

stream_url = 'http://172.20.10.2'

response = requests.head(stream_url)
content_type = response.headers.get('content-type')

print('Content-Type:', content_type)
