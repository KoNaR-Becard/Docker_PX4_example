import cv2

def test_cameras():
    for i in range(0, 40, 2): 
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f" Kamera znaleziona na porcie: {i}")
            cap.release()
        else:
            pass

if __name__ == "__main__":
    test_cameras()