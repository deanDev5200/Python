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
jutsu = False
scene = False

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global view, jutsu, scene
    if len(result.gestures) > 0:
        try:
            cat = result.gestures[0][0].category_name
            if cat == 'kagebunshin' and not jutsu:
                print('nice')
                jutsu = True
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
                    
                time.sleep(1)
                jutsu = False
        except Exception as e:
            print(e)

    view = output_image.numpy_view()

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
