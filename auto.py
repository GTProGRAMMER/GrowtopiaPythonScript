import win32gui
import win32con
import time
import random
import threading
import keyboard

# Configuration
block_placement_coord1 = None
block_placement_coord2 = None
repeat_interval = 0.5
repeat_count = None
stop_bot = False

# Get Growtopia window handle
def get_growtopia_window():
    window_name = "Growtopia"
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        raise Exception("Growtopia window not found. Make sure the game is running.")
    return hwnd

# Get the window size and position
def get_window_rect(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    return left, top, width, height

# Scale coordinates based on window position
def scale_coordinates(hwnd, x, y):
    left, top, width, height = get_window_rect(hwnd)
    scaled_x = left + x  # Add window's left edge
    scaled_y = top + y   # Add window's top edge
    return scaled_x, scaled_y

# Simulate a mouse click within the window
def click_window(hwnd, x, y):
    scaled_x, scaled_y = scale_coordinates(hwnd, x, y)
    lParam = (scaled_y << 16) | scaled_x
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, lParam)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    print(f"Clicked at ({scaled_x}, {scaled_y}) within Growtopia window.")

# Simulate keypress (e.g., Spacebar)
def press_key(hwnd, key):
    key_map = {
        'space': win32con.VK_SPACE,
    }
    virtual_key = key_map[key]
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, virtual_key, 0)
    print(f"Pressed key: {key}")

# Introduce a random delay
def random_delay():
    delay_choices = [(random.uniform(0.1, 0.3), 99), (random.uniform(0.05, 2), 1)]
    delay_time = random.choices(
        population=[x[0] for x in delay_choices], 
        weights=[x[1] for x in delay_choices], 
        k=1
    )[0]
    print(f"Random delay: {delay_time} seconds.")
    time.sleep(delay_time)

# Farming logic
def place_block(hwnd, coord1, coord2):
    print(f"Placing block between {coord1} and {coord2}")
    x1, y1 = coord1[0] + random.randint(-10, 10), coord1[1] + random.randint(-10, 10)
    x2, y2 = coord2[0] + random.randint(-10, 10), coord2[1] + random.randint(-10, 10)
    click_window(hwnd, x1, y1)
    random_delay()
    click_window(hwnd, x2, y2)

def break_block(hwnd):
    print("Breaking block with Spacebar")
    random_delay()

    # Valitaan satunnainen purkuajan kesto painallukselle
    break_time_choices = [(random.uniform(2.5, 3.0), 99), (random.uniform(2.5, 3.5), 1)]
    break_time = random.choices(
        population=[x[0] for x in break_time_choices], 
        weights=[x[1] for x in break_time_choices], 
        k=1
    )[0]

    print(f"Hold time: {break_time} seconds")
    press_key(hwnd, 'space')  # Paina välilyöntiä
    time.sleep(break_time)  # Pidä pohjassa
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)  # Vapauta näppäin

def farm_blocks(hwnd, repeat_count):
    global stop_bot
    count = 0
    while not stop_bot and (repeat_count is None or count < repeat_count):
        print(f"Cycle {count + 1} starting...")
        place_block(hwnd, block_placement_coord1, block_placement_coord2)
        time.sleep(repeat_interval)
        break_block(hwnd)
        time.sleep(repeat_interval)
        random_delay()
        count += 1
    print("Farming complete!")

# Monitor keyboard for 'Q' to stop
def monitor_keyboard():
    global stop_bot
    while True:
        if keyboard.is_pressed('q'):
            print("Hard stop: 'Q' pressed. Stopping immediately.")
            stop_bot = True
            break
        time.sleep(0.1)

# Set coordinates manually using mouse + Enter
def set_coordinates():
    print("Click on the first placement coordinate...")
    while not keyboard.is_pressed("enter"):
        coord1 = win32gui.GetCursorPos()
        print(f"Current mouse position: {coord1}", end="\r")
        time.sleep(0.1)
    coord1 = win32gui.GetCursorPos()
    print(f"\nFirst coordinate set: {coord1}")

    time.sleep(1)

    print("Click on the second placement coordinate...")
    while not keyboard.is_pressed("enter"):
        coord2 = win32gui.GetCursorPos()
        print(f"Current mouse position: {coord2}", end="\r")
        time.sleep(0.1)
    coord2 = win32gui.GetCursorPos()
    print(f"\nSecond coordinate set: {coord2}")

    # Rescale the coordinates to Growtopia window's position
    hwnd = get_growtopia_window()
    left, top, width, height = get_window_rect(hwnd)
    
    # Translate the screen coordinates to Growtopia window coordinates
    coord1_rescaled = (coord1[0] - left, coord1[1] - top)
    coord2_rescaled = (coord2[0] - left, coord2[1] - top)

    return coord1_rescaled, coord2_rescaled

if __name__ == "__main__":
    hwnd = get_growtopia_window()
    print("Growtopia window found.")

    block_placement_coord1, block_placement_coord2 = set_coordinates()
    keyboard_thread = threading.Thread(target=monitor_keyboard, daemon=True)
    keyboard_thread.start()

    print("Starting block farming bot. Press 'Q' to stop.")
    farm_blocks(hwnd, repeat_count)
