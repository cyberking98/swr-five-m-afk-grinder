import cv2
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Controller
import time

keyboard = Controller()

def press_and_release(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    print(f"Tangenten {key} trycktes och släpptes.")

def detect_key(templates_keys):
    # Ta skärmdump av hela skärmen
    screenshot = np.array(ImageGrab.grab())
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Förbättra bilden med kantdetektion
    screenshot_edges = cv2.Canny(screenshot_gray, 50, 200)

    for key, template_key in templates_keys.items():
        # Förbättra mallens kontrast och kantdetektera
        template_edges = cv2.Canny(template_key, 50, 200)

        # Matcha kanterna
        key_match = cv2.matchTemplate(screenshot_edges, template_edges, cv2.TM_CCOEFF_NORMED)
        _, key_val, _, key_loc = cv2.minMaxLoc(key_match)
        
        # Sätt ett högre tröskelvärde för att minska felaktigheter
        if key_val > 0.95:  # Justera detta värde om det behövs
            print(f"Bokstaven {key} hittad!")
            press_and_release(key.lower())
            return True
    return False

# Läs in mallar för W, A, S, D
templates_keys = {
    "W": cv2.imread("templates/W.png", 0),
    "A": cv2.imread("templates/A.png", 0),
    "S": cv2.imread("templates/S.png", 0),
    "D": cv2.imread("templates/D.png", 0),
}

# Kontrollera att alla mallar laddas korrekt
for key, img in templates_keys.items():
    if img is None:
        print(f"Fel: {key}.png kunde inte laddas. Kontrollera sökvägen.")
        exit()

# Starta kontinuerlig detektering
while True:
    if detect_key(templates_keys):
        print("En tangent hittades och trycktes.")
    time.sleep(1)
