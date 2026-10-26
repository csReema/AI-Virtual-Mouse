"""
AI Virtual Mouse
Control the mouse pointer with your index finger using your webcam.

Gestures:
- Move index fingertip: move pointer
- Pinch index finger + thumb: left click
- Press Q in the camera window to quit

Notes:
- macOS may ask for Camera and Accessibility permissions.
- This project uses MediaPipe Hands and PyAutoGUI.
"""

import cv2
import mediapipe as mp
import pyautogui
import math
import time

CAMERA_INDEX = 0
FRAME_REDUCTION = 100
SMOOTHING = 5
CLICK_DISTANCE = 35
CLICK_COOLDOWN = 0.6

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

screen_width, screen_height = pyautogui.size()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

previous_x, previous_y = 0, 0
last_click_time = 0.0

def distance(point_a, point_b):
    return math.hypot(point_a[0] - point_b[0], point_a[1] - point_b[1])

def main():
    global previous_x, previous_y, last_click_time

    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("Error: Could not open the camera. Check macOS Camera permissions.")
        return

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as hands:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read a frame from the camera.")
                break

            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            cv2.rectangle(
                frame,
                (FRAME_REDUCTION, FRAME_REDUCTION),
                (frame_width - FRAME_REDUCTION, frame_height - FRAME_REDUCTION),
                (255, 255, 255),
                2,
            )

            status = "Show one hand to the camera"
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                x = int(index_tip.x * frame_width)
                y = int(index_tip.y * frame_height)
                thumb_x = int(thumb_tip.x * frame_width)
                thumb_y = int(thumb_tip.y * frame_height)

                usable_width = max(1, frame_width - 2 * FRAME_REDUCTION)
                usable_height = max(1, frame_height - 2 * FRAME_REDUCTION)
                mapped_x = (x - FRAME_REDUCTION) / usable_width * screen_width
                mapped_y = (y - FRAME_REDUCTION) / usable_height * screen_height
                mapped_x = max(0, min(screen_width - 1, mapped_x))
                mapped_y = max(0, min(screen_height - 1, mapped_y))

                current_x = previous_x + (mapped_x - previous_x) / SMOOTHING
                current_y = previous_y + (mapped_y - previous_y) / SMOOTHING
                pyautogui.moveTo(current_x, current_y)

                pinch_distance = distance((x, y), (thumb_x, thumb_y))
                now = time.time()
                if pinch_distance < CLICK_DISTANCE:
                    status = "Pinch detected: click"
                    if now - last_click_time > CLICK_COOLDOWN:
                        pyautogui.click()
                        last_click_time = now
                else:
                    status = "Move index finger | Pinch to click"

                previous_x, previous_y = current_x, current_y

            cv2.putText(
                frame, status, (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2
            )
            cv2.putText(
                frame, "Press Q to quit", (20, frame_height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )
            cv2.imshow("AI Virtual Mouse", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
