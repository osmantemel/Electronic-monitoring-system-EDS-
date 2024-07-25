# Elektronik Denetleme Sistemi

Bu proje, bir elektronik denetleme sistemini simüle eden bir Python uygulamasıdır. Sistem, YOLOv8 modelini kullanarak araçların hızını hesaplar ve referans süreyi aşan araçları işaretler.

## Özellikler

- Video akışında araçları tespit eder ve takip eder.
- Araçların geçtiği mesafeyi ve süreyi kullanarak hız hesaplar.
- Referans süreyi aşan araçların hız bilgilerini gösterir.
- Video üzerinde tespit edilen araçları ve hız bilgilerini görsel olarak gösterir.

## Gereksinimler

- Python 3.7 veya üstü
- OpenCV
- NumPy
- Ultralytics YOLO

## Kurulum

1. **Python ve gerekli kütüphaneleri yükleyin**:
    ```bash
    pip install opencv-python numpy ultralytics
    ```

2. **YOLO modelini indirin**:
   - YOLOv8 model dosyasını [buradan](https://github.com/ultralytics/yolov8/releases) indirin ve `./models/yolov8n.pt` yoluna kaydedin.

3. **Video dosyasını temin edin**:
   - Video dosyanızı `./videos/xxx.mp4` yoluna yerleştirin.

## Kullanım

1. **Kodunuzu çalıştırın**:
    ```bash
    python main.py
    ```

2. **Kod içeriği**:
    - `video_path`: Video dosyasının yolu.
    - `model_path`: YOLO model dosyasının yolu.

## Kod Açıklaması

### Ana Fonksiyon: `main(video_path, model_path)`

- **Giriş**: 
  - `video_path`: İşlenecek video dosyasının yolu.
  - `model_path`: YOLO model dosyasının yolu.
  
- **Çıktı**:
  - Araçların hız bilgilerini ve referans süreyi aşan araçları video üzerinde gösterir.

### Temel Parametreler

- `referans_sure_ms`: Araçların referans süreyi aşması durumunda hızlarının işaretlenmesini belirleyen süre (milisaniye cinsinden).
- `mesafe_metre`: Araçların geçtiği mesafe (piksel cinsinden).

## Sorun Giderme

- **OpenCV Hatası**: Eğer `cv2.imshow()` fonksiyonunda hata alıyorsanız, OpenCV'yi yeniden yüklemeyi deneyin.

## Katkıda Bulunma

Herhangi bir hata düzeltme veya özellik ekleme konusunda katkıda bulunmak isterseniz, lütfen bir pull request oluşturun veya sorun bildirin.


