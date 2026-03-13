from PIL import Image
import qrcode
import os
from datetime import datetime

print("프로그램 시작")

# QR 임시 링크 (누가 이거 만들어주길 바람)
TEMP_QR_LINK = "https://google.com"


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
def add_frame_with_photos(photo_paths, frame_path):

    print("사진 + 프레임 합성...")

    frame = Image.open(frame_path).convert("RGBA")

    photo_width = 471
    photo_height = 300

    imgs = [Image.open(p).convert("RGB") for p in photo_paths]
    imgs = [center_crop(img, photo_width, photo_height) for img in imgs]

    positions = [
        (60, 80),
        (60, 420),
        (60, 760),
        (60, 1100)
    ]

    for img, pos in zip(imgs, positions):
        frame.paste(img, pos)

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

    return output_name


def main():

    photos = [
        "photos/photo1.png",
        "photos/photo2.png",
        "photos/photo3.png",
        "photos/photo4.png"
    ]

    now = datetime.now()

    folder_name = now.strftime("%Y-%m-%d_%H-%M")

    session_folder = f"output/{folder_name}"

    os.makedirs(session_folder, exist_ok=True)

    photo_name = now.strftime("%H-%M") + ".png"

    output_file = f"{session_folder}/{photo_name}"

    framed_img = add_frame_with_photos(
        photos,
        "frames/normal_frame.png"
    )

    # 임시 QR 링크 사용
    qr_img = create_qr(TEMP_QR_LINK)

    combine_photo_qr(framed_img, qr_img, output_file)

    print("완성된 파일:", output_file)
    print("QR 링크:", TEMP_QR_LINK)


if __name__ == "__main__":
    main()