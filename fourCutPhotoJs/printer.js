class WebBluetoothPrinter {
  constructor() {
    this.device = null;
    this.characteristic = null;
  }

  // 1. 프린터 찾기 및 연결
  async connect() {
    try {
      this.device = await navigator.bluetooth.requestDevice({
        filters: [{ services: ['000018f0-0000-1000-8000-00805f9b34fb'] }], // 일반적인 프린터 서비스 UUID
        optionalServices: ['000018f0-0000-1000-8000-00805f9b34fb']
      });
      const server = await this.device.gatt.connect();
      const service = await server.getPrimaryService('000018f0-0000-1000-8000-00805f9b34fb');
      const characteristics = await service.getCharacteristics();
      this.characteristic = characteristics.find(c => c.properties.write);
      alert("프린터 연결 성공!");
    } catch (error) {
      console.error("연결 실패:", error);
    }
  }

  // 2. 명령어 전송 (ESC/POS)
  async printRaw(data) {
    if (!this.characteristic) return;
    // 영수증 프린터는 한 번에 보낼 수 있는 바이트 제한이 있어 잘라서 보내야 안전함
    const chunkSize = 512;
    for (let i = 0; i < data.byteLength; i += chunkSize) {
      await this.characteristic.writeValue(data.slice(i, i + chunkSize));
    }
  }

  // 3. 텍스트 출력 (한글은 인코딩 처리가 필요함)
  async printText(text) {
    const encoder = new TextEncoder('euc-kr'); // 영수증 프린터는 보통 EUC-KR 사용
    const data = encoder.encode(text + "\n\n\n");
    await this.printRaw(data);
  }
}