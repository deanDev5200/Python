import time
startTime = time.time()
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerResult, GestureRecognizerOptions, RunningMode as VisionRunningMode
import mediapipe as mp
import cv2

model_path = 'D:\Python\Testing\ST\gesture_recognizer.task'
video = cv2.VideoCapture(0)
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if len(result.gestures) > 0:
        print(f'gesture recognition result: {result.gestures[0]}')

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path, delegate=BaseOptions.Delegate.CPU),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
print('a')

while True:
    _, img = video.read()
    with GestureRecognizer.create_from_options(options) as recognizer:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        recognizer.recognize_async(mp_image, round(time.time()-startTime))

    cv2.imshow("epep", mp_image.numpy_view())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()