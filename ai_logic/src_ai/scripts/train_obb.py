from ultralytics import YOLO

DATA_YAML_PATH = "/home/marcin-g-rniak/Docker_PX4_example/ai_logic/src_ai/datasets/puszka_obb/data.yaml"

def main():
    print("Start treningu YOLOv8 OBB obrócone ramki")

    model = YOLO("yolov8n-obb.pt")

    results = model.train(
        data=DATA_YAML_PATH, 
        epochs=30,
        imgsz=640,
        device="cpu"
    )
    
    print("Trening zakończony")

if __name__ == "__main__":
    main()