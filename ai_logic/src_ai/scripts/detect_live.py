import cv2
from ultralytics import YOLO

MODEL_PATH = "/home/marcin-g-rniak/Docker_PX4_example/runs/obb/train2/weights/best.pt" # dopasować ścieżkę do swojej

def main():
    print(f"Ładowanie wyuczonego modelu z: {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Błąd! Nie znaleziono modelu. Sprawdź ścieżkę. Szczegóły: {e}")
        return

    cap = cv2.VideoCapture(32, cv2.CAP_V4L2) # dopasować do kamerki z drona(port 36/34?)
    
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
        
        annotated_frame = results[0].plot()

        cv2.imshow("Wykrywanie Puszki na Zywo (OBB)", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()