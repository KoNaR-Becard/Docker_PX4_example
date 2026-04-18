import cv2
import os
from datetime import datetime

SAVE_DIR = "../datasets/solar_panels/train/clean" 

CAMERA_INDEX = 0

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    absolute_save_dir = os.path.abspath(SAVE_DIR)
    print(f"Katalog zapisu: {absolute_save_dir}")

    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print(f"Błąd: Nie można nawiązać połączenia z kamerą pod indeksem {CAMERA_INDEX}.")
        return

    print("Sterowanie:")
    print(" [S] - Zapisz zdjęcie (trafi do train/clean)")
    print(" [Q] - Wyjdź z programu")

    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Błąd: Nie można pobrać klatki. Zamykam strumień...")
            break

        cv2.imshow("Zbieranie danych - Czyste panele", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') or key == ord('S'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"clean_panel_{timestamp}_{count}.jpg"
            filepath = os.path.join(absolute_save_dir, filename)
            
            cv2.imwrite(filepath, frame)
            print(f"-> Zapisano: {filename}")
            count += 1
        
        elif key == ord('q') or key == ord('Q'):
            print("Zamykanie programu...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()