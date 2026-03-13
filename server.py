from flask import Flask, send_from_directory
import os

app = Flask(__name__)

OUTPUT_FOLDER = "output"


@app.route("/")
def home():
    return "포토부스 서버 실행중"


@app.route("/photo/<filename>")
def download(filename):

    for root, dirs, files in os.walk(OUTPUT_FOLDER):
        if filename in files:
            return send_from_directory(root, filename)

    return "파일 없음"


app.run(host="0.0.0.0", port=5000)