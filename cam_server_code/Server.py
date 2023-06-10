from flask import Flask, render_template, Response
import requests

app = Flask(__name__)

# URLs of the video streams from ESP32s
stream1_url = 'http://192.168.2.3/' 
stream2_url = 'http://192.168.2.6/' 
stream3_url = 'http://192.168.2.4/' 
stream4_url = 'http://192.168.2.2/'


def generate_frames():
    while True:
        # Request frames from the ESP32 cameras
        response1 = requests.get(stream1_url)
        response2 = requests.get(stream2_url)
        response3 = requests.get(stream3_url)
        response4 = requests.get(stream4_url)

        if response1.status_code != 200 or response2.status_code != 200:
            break

        # Yield the concatenated frames as a multipart response
        yield (b'--frame\r\n'
               b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
               + response1.content + b'\r\n'
               b'--frame\r\n'
               b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
               + response2.content + b'\r\n'
               b'--frame\r\n'
               b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
               + response3.content + b'\r\n'
               b'--frame\r\n'
               b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
               + response4.content + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
