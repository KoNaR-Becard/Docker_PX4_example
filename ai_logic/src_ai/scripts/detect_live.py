import os
import cv2
import time
import rclpy
from rclpy.node import Node
from ultralytics import YOLO

class PanelDetectionNode(Node):
    def __init__(self):
        super().__init__('panel_detection_node')
        
        self.declare_parameter('model_path', '/app/models/best.pt')
        self.model_path = self.get_parameter('model_path').get_parameter_value().string_value
        
        self.camera_port = 37
        
        print(f"Loading trained model from: {self.model_path}")
        if not os.path.exists(self.model_path):
            print(f"Error! Model file does not exist at: {self.model_path}")
            raise SystemExit

        try:
            self.model = YOLO(self.model_path)
        except Exception as e:
            print(f"Error! Failed to load model. Details: {e}")
            raise SystemExit

        self.cap = cv2.VideoCapture(self.camera_port, cv2.CAP_V4L2)
        
        if not self.cap.isOpened():
            print("Error: Cannot open camera.")
            raise SystemExit

        print("Camera started!")
        print("Show the panel to the camera and rotate it. Press 'Q' to quit.")

        self.last_save_time = 0.0
        self.timer = self.create_timer(0.033, self.timer_callback)

    def send_to_pixhawk(self, see_panel, x=0.0, y=0.0, obrot=0.0, status="SEARCHING"):
        pass

    def collect_command_from_pixhawk(self, button):
        if button == ord('p'):
            return "DONE"
        return "NONE"

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error capturing frame.")
            rclpy.shutdown()
            return

        results = self.model.predict(frame, conf=0.5, verbose=False)
        button = cv2.waitKey(1) & 0xFF

        if results[0].obb is not None and len(results[0].obb) > 0:
            print("Panel detected")
            
            data = results[0].obb.xywhr[0] 
            x_center = float(data[0])
            y_center = float(data[1])
            width = float(data[2])
            height = float(data[3])
            rotation_angle = float(data[4])

            self.send_to_pixhawk(True, x_center, y_center, rotation_angle)

            command = self.collect_command_from_pixhawk(button)
            
            if command == "DONE" and (time.time() - self.last_save_time) > 1.0:
                file_name = f"panel_analysis_{int(time.time())}.jpg"
                
                cv2.imwrite(file_name, frame)
                print(f"Image saved as: {file_name}")
                
                self.send_to_pixhawk(True, status="DONE")
                self.last_save_time = time.time()

        else:
            self.send_to_pixhawk(False, status="CLEAN")

        annotated_frame = results[0].plot()
        if results[0].obb is not None and len(results[0].obb) > 0:
             cv2.drawMarker(annotated_frame, (int(x_center), int(y_center)), (0, 0, 255), 
                            markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        cv2.imshow("Live Panel Detection (OBB)", annotated_frame)

        if button == ord('q'):
            rclpy.shutdown()

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    try:
        node = PanelDetectionNode()
        rclpy.spin(node)
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        if 'node' in locals():
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()