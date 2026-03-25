const express = require('express');
const app = express();
const path = require('path');

// 현재 폴더의 파일을 웹에 띄우도록 설정
app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 노트북의 모든 네트워크 인터페이스(0.0.0.0)에서 접속 허용
const PORT = 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`서버가 시작되었습니다!`);
    console.log(`노트북에서 접속: http://localhost:${PORT}`);
    console.log(`태블릿에서 접속: http://[노트북IP]:${PORT}`);
});

