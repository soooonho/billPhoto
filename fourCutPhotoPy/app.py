from flask import Flask, request, jsonify
from flask_cors import CORS # 태블릿에서 접속 시 보안 허용을 위해 필요
import cv2
import numpy as np
import base64
import os
from PIL import Image
import qrcode
from datetime import datetime
import io
TEMP_QR_LINK = "https://google.com"
app = Flask(__name__)
CORS(app) # 모든 도메인에서의 접근을 허용

# 프레임 이미지 로드 (배경이 투명한 PNG)
FRAME_PATH = 'frame.png'
images=[]
selected_images=[]
professor=Image.open("professor.png").convert("RGBA")
def pillow_to_base64(img):
    buffered = io.BytesIO()
    # 이미지를 PNG 포맷으로 메모리에 저장
    img.save(buffered, format="PNG")
    # 메모리에 저장된 바이너리를 읽어서 base64로 인코딩
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"
@app.route('/upload', methods=['POST'])
def upload_image():
    images.clear()
    dataset = request.json.get('images', [])
    
    for base64_data in dataset:
        header, encoded = base64_data.split(",", 1)
        data = base64.b64decode(encoded)
        
        img = Image.open(io.BytesIO(data)).convert("RGB")
        #640*480
        img.paste(professor, (0, 0), professor)
        img.save("texture_overlay.png")
        # 4. 이제 PIL 객체가 리스트에 들어갑니다.
        images.append(img)
    processed_images=[]
    for image in images:
        processed_images.append(pillow_to_base64(image))

    return jsonify({
        "status": "success",
        "processed_images": processed_images
    }), 200
@app.route('/upload_selected',methods=['POST'])
def add_frame():
    selected_images.clear()
    dataset = request.json.get('selected_images', [])
    for base64_data in dataset:
        header, encoded = base64_data.split(",", 1)
        data = base64.b64decode(encoded)
        
        img = Image.open(io.BytesIO(data)).convert("RGB")
        
        # 4. 이제 PIL 객체가 리스트에 들어갑니다.
        selected_images.append(img)
    framed_image=main()
    return jsonify({
        "status": "success",
        "result_image": pillow_to_base64(framed_image)
    }), 200
def center_crop(img, target_width, target_height):

    width, height = img.size

    target_ratio = target_width / target_height
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    return img.resize((target_width, target_height), Image.LANCZOS)


# 프레임 + 사진 합성
def add_frame_with_photos(photos, frame_path):

    print("사진 + 프레임 합성...")

    frame = Image.open(frame_path).convert("RGBA")

    photo_width = 471
    photo_height = 300

    photos = [center_crop(photo, photo_width, photo_height) for photo in photos]

    positions = [
        (60, 80),
        (60, 420),
        (60, 760),
        (60, 1100)
    ]

    for photo, pos in zip(photos, positions):
        frame.paste(photo, pos)

    return frame


# QR 생성
def create_qr(url):

    print("QR 코드 생성...")

    qr = qrcode.make(url)

    return qr


# 사진 + QR 합성
def combine_photo_qr(photo_img, qr_img, output_name):

    print("QR 합성...")

    qr = qr_img.resize((200,200))

    new_height = photo_img.height + qr.height + 30

    canvas = Image.new("RGB", (photo_img.width, new_height), (255,255,255))

    canvas.paste(photo_img, (0,0))
    canvas.paste(qr, (photo_img.width//2 - qr.width//2, photo_img.height + 10))
    canvas.save(output_name)

    return canvas


def main():
    now = datetime.now()

    folder_name = now.strftime("%Y-%m-%d_%H-%M")

    session_folder = f"output/{folder_name}"

    os.makedirs(session_folder, exist_ok=True)

    photo_name = now.strftime("%H-%M") + ".png"

    output_file = f"{session_folder}/{photo_name}"

    framed_img = add_frame_with_photos(
        selected_images,
        "frame.png"
    )

    # 임시 QR 링크 사용
    qr_img = create_qr(TEMP_QR_LINK)

    framed_image=combine_photo_qr(framed_img, qr_img, output_file)

    print("완성된 파일:", output_file)
    print("QR 링크:", TEMP_QR_LINK)
    return framed_image
if __name__ == '__main__':
    if not os.path.exists('photos'): os.makedirs('photos')
    app.run(host='0.0.0.0', port=5000)