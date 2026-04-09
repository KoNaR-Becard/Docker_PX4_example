from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt') 
cap = cv2.VideoCapture(36)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("AI startuje... 'q' aby wyjsc")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Brak obrazu na porcie 32. Sprobuj 34 lub sprawdz kabel.")
        break

    results = model(frame, stream=True, conf=0.4)

    for r in results:
        annotated_frame = r.plot()
        cv2.imshow("MSI AI - Test RealSense", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()