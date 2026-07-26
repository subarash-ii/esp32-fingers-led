import serial
import serial.tools.list_ports
import sys
import time
import cv2
import mediapipe as mp

def find_esp_port():
    esp_keywords= r"CP210|CH340|FTDI|USB VID:PID=303A"
    ports = list(serial.tools.list_ports.grep(esp_keywords))

    if not ports:
        return None

    return ports[0].device


esp_port = find_esp_port()

if not esp_port:
    sys.exit("Error: ESP not found")

ser = serial.Serial(esp_port, 115200, timeout=1, dsrdtr=False, rtscts=False)

ser.setDTR(False)
ser.setRTS(False)
time.sleep(2)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

index = 0
middle = 0
ring = 0
pinky = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        index_top = hand.landmark[8]
        index_bottom = hand.landmark[5]

        middle_top = hand.landmark[12]
        middle_bottom = hand.landmark[9]

        ring_top = hand.landmark[16]
        ring_bottom = hand.landmark[13]

        pinky_top = hand.landmark[20]
        pinky_bottom = hand.landmark[17]

        if index_top.y > index_bottom.y: index = 1
        else: index = 0

        if middle_top.y > middle_bottom.y: middle = 1
        else: middle = 0

        if ring_top.y > ring_bottom.y: ring = 1
        else: ring = 0

        if pinky_top.y > pinky_bottom.y: pinky = 1
        else: pinky = 0
    else:
        index = 0
        middle = 0
        ring = 0
        pinky = 0

    byte = (index << 3) | (middle << 2) | (ring << 1) | pinky

    ser.write(bytes([byte]))

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord("q"):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()