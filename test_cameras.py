"""Test which camera indices work."""
import cv2

print("Testing camera indices...")
working_cameras = []

for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use DirectShow backend on Windows
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            h, w = frame.shape[:2]
            print(f"Camera {i}: WORKING ({w}x{h})")
            working_cameras.append(i)

            # Show preview
            cv2.imshow(f"Camera {i}", frame)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        else:
            print(f"Camera {i}: Opens but no frame")
        cap.release()
    else:
        print(f"Camera {i}: Cannot open")

print(f"\nWorking cameras: {working_cameras}")
if working_cameras:
    print(f"Use camera index: {working_cameras[0]}")
