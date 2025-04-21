# camera_usb.py – USB camera initialization for Limelight 3A
import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

camera = None  # OpenCV VideoCapture object

def init_camera():
    """Initialize the USB camera. Returns True if successful, False if not."""
    global camera
    # If a camera was already open, release it first
    if camera:
        camera.release()
        cv2.destroyAllWindows()
    # Open the camera (CAMERA_INDEX can be an integer index or a device path string like "/dev/video10")
    camera = cv2.VideoCapture("/dev/video10", cv2.CAP_V4L2)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    if not camera.isOpened():
        print(f"❌ Ошибка: камера не инициализирована ({CAMERA_INDEX})")
        return False
    print(f"✅ Камера инициализирована: {CAMERA_INDEX}")
    return True

def capture_frame():
    """Capture a frame from the camera. Returns the frame image or None if failed."""
    if not camera:
        print("⚠️ Камера не инициализирована")
        return None
    ret, frame = camera.read()
    if not ret:
        print("⚠️ Не удалось считать кадр")
        return None
    return frame

def release_camera():
    """Release the camera and any OpenCV windows."""
    global camera
    if camera:
        camera.release()
        cv2.destroyAllWindows()
        camera = None
