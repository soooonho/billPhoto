"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
// 2. 이미지 전송 함수
function sendImagesToPython(base64Arr) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const python_api_url = "http://192.168.1.108:5000/upload";
            const response = yield fetch(python_api_url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    images: base64Arr,
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = yield response.json();
            console.log("서버 응답:", result);
            alert("사진이 전송되었습니다!");
        }
        catch (error) {
            console.error("전송 중 에러 발생:", error);
        }
    });
}
// 3. 카메라 초기화 함수
function initCamera() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const stream = yield navigator.mediaDevices.getUserMedia({
                video: { facingMode: "user" },
            });
            const videoURL = document.getElementById("webcam");
            if (videoURL) {
                videoURL.srcObject = stream;
            }
        }
        catch (err) {
            alert("카메라 권한을 허용해주세요: " + err);
        }
    });
}
// 4. DOM 요소 참조 및 이벤트 리스너
// 요소가 존재하지 않을 수 있으므로 타입 단언(Type Assertion)을 사용하거나 체크가 필요합니다.
const video = document.getElementById("webcam");
const canvas = document.getElementById("photoCanvas");
const captureBtn = document.getElementById("captureBtn");
let photoBundle = [];
captureBtn === null || captureBtn === void 0 ? void 0 : captureBtn.addEventListener("click", () => __awaiter(void 0, void 0, void 0, function* () {
    // 캡처 전 배열 초기화 (필요 시)
    photoBundle = [];
    for (let i = 0; i < 6; i++) {
        const context = canvas.getContext("2d");
        if (context && video.videoWidth > 0) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL("image/png");
            photoBundle.push(imageData);
            console.log(`${i + 1}번째 사진 캡처 완료`);
            // 마지막 루프에서는 대기하지 않도록 처리 가능
            if (i < 5)
                yield delay(10000);
        }
    }
    // 기존 코드의 오타 수정: sendImageToPython -> sendImagesToPython
    yield sendImagesToPython(photoBundle);
}));
// 실행
initCamera();
//# sourceMappingURL=script.js.map