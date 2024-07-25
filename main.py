from ultralytics import YOLO
import cv2
import numpy as np
from datetime import datetime

zamanlar = {}
date_format = '%Y-%m-%d %H:%M:%S.%f'
referans_sure_ms = 4500  # Referans süre (milisaniye)
mesafe_metre = 200  # Araçların geçtiği mesafe (px)

def main(video_path, model_path):
 
    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"HATA: DOSYA BULUNAMADI {video_path}")
        return

    # Çizgi parametreleri
    line1_y = 50  # Üst çizgi
    line2_y = None  # Alt çizgi
    line_color = (0, 0, 0)  # Siyah çizgi
    line_thickness = 3  # Çizgi kalınlığı

    # Boş alan ve metin parametreleri
    boş_sahne_genişlik = 400  # Boş alan genişliği
    metin_renk = (0, 0, 0) 
    metin_boyut = 0.6
    metin_kalınlık = 1
    metin_yükseklik = 30  # Boş alana yazılacak metinler arasındaki yükseklik

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break

        results = model.track(frame, persist=True)

        frame_with_boxes = results[0].plot()

        height, width, _ = frame_with_boxes.shape

        if line2_y is None:
            line2_y = height - 50

        boş_sahne = np.zeros((height, boş_sahne_genişlik, 3), dtype=np.uint8)
        boş_sahne[:] = (255, 255, 255) 

        metin_y = 30

        for box_id, zaman in zamanlar.items():
            if zaman['giris_zamani'] is not None and zaman['cikis_zamani'] is not None:
                giris_zamani = datetime.strptime(zaman['giris_zamani'], date_format)
                cikis_zamani = datetime.strptime(zaman['cikis_zamani'], date_format)
                fark = (cikis_zamani - giris_zamani).total_seconds() * 1000  # Farkı milisaniye cinsinden hesapla
                
                if fark > referans_sure_ms:

                    hız_m_s = mesafe_metre / (fark / 1000)  # m/s
                    hız_km_s = hız_m_s * 3.6  # km/s
                    speed_text = f"ID: {box_id} Hiz: {hız_km_s:.2f} km/s Sure: {(fark)/1000:.2f} sn"
                    
                    cv2.putText(boş_sahne, speed_text, (10, metin_y), cv2.FONT_HERSHEY_SIMPLEX, metin_boyut, metin_renk, metin_kalınlık)
                    metin_y += metin_yükseklik

        frame_with_boxes = np.hstack((boş_sahne, frame_with_boxes))

        # Çizgileri çiz
        cv2.line(frame_with_boxes, (boş_sahne_genişlik, line1_y), (width + boş_sahne_genişlik, line1_y), line_color, line_thickness)
        cv2.line(frame_with_boxes, (boş_sahne_genişlik, line2_y), (width + boş_sahne_genişlik, line2_y), line_color, line_thickness)

        for result in results:
            boxes = result.boxes
            for box in boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                box_center_y = (y1 + y2) // 2
                box_id = int(box.id) if box.id is not None else -1

        
                if box_id not in zamanlar:
                    zamanlar[box_id] = {'giris_zamani': None, 'cikis_zamani': None}

                if y1 < line2_y < y2 and zamanlar[box_id]['giris_zamani'] is None:
                    zamanlar[box_id]['giris_zamani'] = datetime.now().strftime(date_format)
                    print(f"girdi:  {box_id}")

                if y1 < line1_y < y2 and zamanlar[box_id]['cikis_zamani'] is None:
                    zamanlar[box_id]['cikis_zamani'] = datetime.now().strftime(date_format)
                    print(f"çıktı:  {box_id}")

                color = (255, 0, 0)  
                speed_text = ""

                if zamanlar[box_id]['giris_zamani'] is not None and zamanlar[box_id]['cikis_zamani'] is not None:
                    giris_zamani = datetime.strptime(zamanlar[box_id]['giris_zamani'], date_format)
                    cikis_zamani = datetime.strptime(zamanlar[box_id]['cikis_zamani'], date_format)
                    fark = (cikis_zamani - giris_zamani).total_seconds() * 1000  
                    
                    if fark > 0:  
                        hız_m_s = mesafe_metre / (fark / 1000)  # m/s
                        hız_km_s = hız_m_s * 3.6  # km/s
                        speed_text = f"{hız_km_s:.2f} km/s"
                    
                    if fark > referans_sure_ms:
                        color = (0, 0, 255)  # Kırmızı
                elif y1 < line1_y < y2 or y1 < line2_y < y2:
                    color = (0, 255, 0)  # Yeşil

                cv2.rectangle(frame_with_boxes, (x1 + boş_sahne_genişlik, y1), (x2 + boş_sahne_genişlik, y2), color, 2)
                if speed_text:
                    cv2.putText(frame_with_boxes, speed_text, (x1 + boş_sahne_genişlik, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow('Tracked Objects', frame_with_boxes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(zamanlar)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = './videos/ccc.mp4'
    model_path = './models/yolov8n.pt'
    main(video_path, model_path)
