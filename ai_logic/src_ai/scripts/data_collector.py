import os
import cv2
from datetime import datetime
import rclpy
from rclpy.node import Node

class CameraSaverNode(Node):
    """
    ROS 2 Node for capturing and saving camera frames.
    """
    def __init__(self):
        super().__init__('camera_saver_node')
        
        self.save_dir = os.path.abspath("../datasets/solar_panels/train/clean")
        os.makedirs(self.save_dir, exist_ok=True)
        
        self.camera_index = 37
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        self.count = 0
        
        if not self.cap.isOpened():
            self.get_logger().error(f"Failed to open camera with index {self.camera_index}")
            return
            
        print(f"Save directory: {self.save_dir}")
        print("Controls:\n [S] - Save image\n [Q] - Quit")
        
        self.timer = self.create_timer(0.033, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        cv2.imshow("Data Collection - Clean Panels", frame)
        key = cv2.waitKey(1) & 0xFF

        if key in [ord('s'), ord('S')]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"clean_panel_{timestamp}_{self.count}.jpg"
            filepath = os.path.join(self.save_dir, filename)
            
            cv2.imwrite(filepath, frame)
            print(f"-> Saved: {filename}")
            self.count += 1
          
        elif key in [ord('q'), ord('Q')]:
            print("Shutting down...")
            rclpy.shutdown()

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    
    node = CameraSaverNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()