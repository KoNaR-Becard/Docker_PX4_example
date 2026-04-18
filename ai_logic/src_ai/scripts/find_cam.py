import cv2

def main():
    print("Rozpoczynam skanowanie portów (0-10)")
    
    for i in range(40):
        cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f" Prawdziwy obraz wideo jest pod indeksem: {i}")
            else:
                print(f"Port {i} otwiera się, ale nie zwraca obrazu.")
            cap.release()
        else:
            print(f"Port {i} jest zamknięty lub niedostępny.")

    print("Koniec skanowania")

if __name__ == "__main__":
    main()