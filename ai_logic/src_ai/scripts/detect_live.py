import cv2
import time
from ultralytics import YOLO

MODEL_PATH = "/home/marcin-g-rniak/Docker_PX4_example/runs/obb/train2/weights/best.pt" # dopasować ścieżkę do swojej
CAMERA_PORT = 37

def send_to_pixhawk(see_panel, x=0.0, y=0.0, obrot=0.0, status="SZUKAM"):
    #print(f"Wysyłam -> Panel: {see_panel} | X:{x:.1f} Y:{y:.1f} Angle:{obrot:.2f} | Status:{status}")
    pass

def collect_command_from_pixhawk(buttom):
    if buttom == ord('p'):
        return "Zrobione"
    return "Brak"

def main():
    print(f"Ładowanie wyuczonego modelu z: {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Błąd! Nie znaleziono modelu. Sprawdź ścieżkę. Szczegóły: {e}")
        return

    cap = cv2.VideoCapture(CAMERA_PORT, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print("Błąd: Nie można otworzyć kamery w laptopie.")
        return

    print("Kamera uruchomiona!")
    print("Pokaż puszkę do kamery i obracaj nią. Wciśnij 'Q', aby wyjść.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Błąd pobierania klatki.")
            break

        results = model.predict(frame, conf=0.5, verbose=False)
        buttom = cv2.waitKey(1) & 0xFF

        if results[0].obb is not None and len(results[0].obb) > 0:
            print("Wykryto panel")
            
            data = results[0].obb.xywhr[0] 
            x_center= float(data[0])
            y_center = float(data[1])
            width = float(data[2])
            height = float(data[3])
            rotation_angle = float(data[4])

            send_to_pixhawk(see_panel=True, x=x_center, y=y_center, obrot=rotation_angle)

            command = collect_command_from_pixhawk(buttom)
            
            if command == "Zrobione":
                file_name = f"panel_analiza_{int(time.time())}.jpg"
                
                cv2.imwrite(file_name, frame)
                print(f"Zdjęcie zapisane jako: {file_name}")
                
                send_to_pixhawk(see_panel=True, status="Zrobione")
                
                time.sleep(1) 

        else:
            send_to_pixhawk(see_panel=False, status="Clean")

        annotated_frame = results[0].plot()
        if results[0].obb is not None and len(results[0].obb) > 0:
             cv2.drawMarker(annotated_frame, (int(x_center), int(y_center)), (0, 0, 255), 
                            markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        cv2.imshow("Wykrywanie Puszki na Zywo (OBB)", annotated_frame)

        if buttom == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()