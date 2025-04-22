# routines/camera_only.py
import cv2
from vision import camera_stream

if __name__ == "__main__":
    if not camera_stream.init_camera():
        exit()

    while True:
        frame = camera_stream.get_frame()
        if frame is None:
            break

        cv2.imshow("Limelight Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_stream.release_camera()
    cv2.destroyAllWindows()
