import pyautogui
from pynput import mouse, keyboard
import json
import time

# Global variables
event_count = 0
log_data = []

# Function to capture screenshot with timestamped filename
def capture_screenshot():
    global event_count
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    # Generate timestamp with microseconds
    timestamp = time.strftime("%Y%m%d_%H%M%S_%f")
    # Save screenshot to file with timestamped filename
    screenshot_path = f"screenshot_{timestamp}.png"
    screenshot.save(screenshot_path)
    return screenshot_path

# Function to handle mouse events
def on_click(x, y, button, pressed):
    global event_count
    if pressed:
        event_count += 1
        screenshot_path = capture_screenshot()
        log_data.append({"event_type": "mouse_click", "screenshot_path": screenshot_path, "coordinates": (x, y), "timestamp": time.time()})
        update_log_file()

# Function to handle keyboard events
def on_press(key):
    global event_count
    event_count += 1
    screenshot_path = capture_screenshot()
    try:
        log_data.append({"event_type": "key_press", "screenshot_path": screenshot_path, "key_pressed": key.char, "timestamp": time.time()})
    except AttributeError:
        log_data.append({"event_type": "key_press", "screenshot_path": screenshot_path, "key_pressed": str(key), "timestamp": time.time()})
    update_log_file()

# Function to update the log file
def update_log_file():
    global log_data
    with open("event_log.json", "w") as json_file:
        json.dump(log_data, json_file, indent=4)

# Start listening for mouse events
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# Start listening for keyboard events
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

try:
    # Main loop to capture screenshots and handle events
    while True:
        pass
except KeyboardInterrupt:
    pass
finally:
    # Stop mouse and keyboard listeners
    mouse_listener.stop()
    keyboard_listener.stop()
