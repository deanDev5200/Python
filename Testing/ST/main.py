import time
import keyboard
startTime = time.time()
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerResult, GestureRecognizerOptions, RunningMode as VisionRunningMode
import mediapipe as mp
import cv2

model_path = 'D:\Python\Testing\ST\gesture_recognizer.task' 
video = cv2.VideoCapture(0)
_, view = video.read()
scene = False

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global view, jutsu, scene
    view = output_image.numpy_view()
    if len(result.gestures) > 0:
        cat = result.gestures[0][0].category_name
        view = cv2.putText(output_image.numpy_view().copy(), cat, (160, 360), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 6)
        view = cv2.putText(view, cat, (160, 360), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        if cat == 'kagebunshin':
            if not scene:
                keyboard.press("Ctrl+Home")
                time.sleep(0.1)
                keyboard.release("Ctrl+Home")
                scene = True
            else:
                keyboard.press("Ctrl+]")
                time.sleep(0.1)
                keyboard.release("Ctrl+]")
                scene = False
                
            time.sleep(1.5)

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path, delegate=BaseOptions.Delegate.CPU),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

while True:
    _, img = video.read()
    #view = img
    try:
        with GestureRecognizer.create_from_options(options) as recognizer:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
            recognizer.recognize_async(mp_image, round(time.time()-startTime))
    except Exception as e:
        print(e)

    cv2.imshow("epep", view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
