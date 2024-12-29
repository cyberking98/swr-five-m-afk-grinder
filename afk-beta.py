import cv2
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Controller, Listener, Key
import time
from rich.console import Console
from rich.live import Live
import os
import sys
import time
from rich.panel import Panel
from rich.progress import Progress



os.system('cybex rp grinder')

#asci animated logo
def animate_logo():
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    logo = """
//  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\ 
// ( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )
//  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ < 
//  /\_/\    __  __    _    ____  _____   ______   __   ______   ______  _______  __    /\_/\ 
// ( o.o )  |  \/  |  / \  |  _ \| ____| | __ ) \ / /  / ___\ \ / / __ )| ____\ \/ /   ( o.o )
//  > ^ <   | |\/| | / _ \ | | | |  _|   |  _ \\ V /  | |    \ V /|  _ \|  _|  \  /     > ^ < 
//  /\_/\   | |  | |/ ___ \| |_| | |___  | |_) || |   | |___  | | | |_) | |___ /  \     /\_/\ 
// ( o.o )  |_|  |_/_/   \_\____/|_____| |____/ |_|    \____| |_| |____/|_____/_/\_\   ( o.o )
//  > ^ <                                                                               > ^ < 
//  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\ 
// ( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )
//  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ < 
    """
    
    console = Console()
    lines = logo.split('\n')
    for line in lines:
        console.print(f"[bold red]{line}[/bold red]")
        time.sleep(0.05)
    print("")

animate_logo()
# Skapa en Rich-konsol
console = Console()
console.print("[blue bold]script is ready to use[/blue bold]")

keyboard = Controller()
script_paused = False  # Variabel för att hantera pausläget


def press_and_release(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    console.print(f"[blue]Tangenten {key.upper()} trycktes och släpptes.[/blue]")


def detect_key(templates_keys):
    global script_paused
    if script_paused:
        console.print("[red]Skriptet är pausat. Tryck 'Insert' för att återuppta.[/red]")
        console.print("[green bold]script made by cybex#[/green bold]")
        time.sleep(1)
        return False

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
            console.print(f"[yellow]Bokstaven {key.upper()} hittad![/yellow]")
            press_and_release(key.lower())

            # Specialfall för `E`
            if key == "E":
                console.print("[green bold]Du sålde en vara![/green bold]")

            return True
    return False


# Läs in mallar för W, A, S, D och E
templates_keys = {
    "W": cv2.imread("templates/W.png", 0),
    "A": cv2.imread("templates/A.png", 0),
    "S": cv2.imread("templates/S.png", 0),
    "D": cv2.imread("templates/D.png", 0),
    "E": cv2.imread("templates/E.png", 0),
}

# Kontrollera att alla mallar laddas korrekt
for key, img in templates_keys.items():
    if img is None:
        console.print(f"[red bold]Fel: {key}.png kunde inte laddas. Kontrollera sökvägen.[/red bold]")
        exit()


# Funktion för att hantera tangenttryckningar
def on_press(key):
    global script_paused
    if key == Key.insert:
        script_paused = not script_paused
        if script_paused:
            console.print("[red bold]Skriptet pausat. Tryck 'Insert' igen för att återuppta.[/red bold]")

            
            console.print("[green bold]script made by cybex#[/green bold]")
        else:
            console.print("[green bold]Skriptet återupptaget.[/green bold]")


# Starta en tangentlyssnare i en separat tråd
listener = Listener(on_press=on_press)
listener.start()

# Starta kontinuerlig detektering
while True:
    if detect_key(templates_keys):
        console.print("[cyan]En tangent hittades och trycktes.[/cyan]")
    time.sleep(1)
