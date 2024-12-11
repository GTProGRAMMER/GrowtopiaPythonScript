import pyautogui
import time
import random
import threading
import keyboard

block_placement_coord1 = None
block_placement_coord2 = None
repeat_interval = 0.5
repeat_count = None

stop_bot = False

def monitor_keyboard():
    global stop_bot
    while True:
        if keyboard.is_pressed('q'):
            print("Hard stop: 'Q' pressed. Stopping immediately.")
            stop_bot = True
            break
        time.sleep(0.1)

def random_delay():
    delay_choices = [(random.uniform(0.1, 0.3), 99), (random.uniform(0.05, 2), 1)]
    delay_time = random.choices(
        population=[x[0] for x in delay_choices], 
        weights=[x[1] for x in delay_choices], 
        k=1
    )[0]
    print(f"Random delay: {delay_time} seconds.")
    time.sleep(delay_time)

def set_coordinates():
    print("Click on the first placement coordinate...")
    while not keyboard.is_pressed("enter"):
        coord1 = pyautogui.position()
        print(f"Current mouse position: {coord1}", end="\r")
        time.sleep(0.1)
    coord1 = pyautogui.position()
    print(f"\nFirst coordinate set: {coord1}")
    
    time.sleep(1)
    
    print("Click on the second placement coordinate...")
    while not keyboard.is_pressed("enter"):
        coord2 = pyautogui.position()
        print(f"Current mouse position: {coord2}", end="\r")
        time.sleep(0.1)
    coord2 = pyautogui.position()
    print(f"\nSecond coordinate set: {coord2}")
    
    return coord1, coord2

def place_block(coord1, coord2):
    print(f"Placing block between {coord1} and {coord2}")
    x1, y1 = coord1[0] + random.randint(-10, 10), coord1[1] + random.randint(-10, 10)
    x2, y2 = coord2[0] + random.randint(-10, 10), coord2[1] + random.randint(-10, 10)
    
    pyautogui.moveTo(x1, y1)
    pyautogui.click()
    print(f"Clicked at ({x1}, {y1})")
    
    random_delay()
    
    pyautogui.moveTo(x2, y2)
    pyautogui.click()
    print(f"Clicked at ({x2}, {y2})")

def break_block():
    print("Breaking block with Spacebar")
    random_delay()
    
    keyboard.press('space')
    
    break_time_choices = [(random.uniform(3.0, 3.5), 99), (random.uniform(3.0, 4.0), 1)]
    break_time = random.choices(
        population=[x[0] for x in break_time_choices], 
        weights=[x[1] for x in break_time_choices], 
        k=1
    )[0]
    
    print(f"Hold time: {break_time} seconds")
    time.sleep(break_time)
    keyboard.release('space')

def farm_blocks(repeat_count):
    global stop_bot
    count = 0
    while not stop_bot and (repeat_count is None or count < repeat_count):
        print(f"Cycle {count + 1} starting...")
        place_block(block_placement_coord1, block_placement_coord2)
        time.sleep(repeat_interval)
        break_block()
        time.sleep(repeat_interval)
        random_delay()
        count += 1
    print("Farming complete!")

if __name__ == "__main__":
    print("Press Enter to select placement coordinates.")
    block_placement_coord1, block_placement_coord2 = set_coordinates()

    keyboard_thread = threading.Thread(target=monitor_keyboard, daemon=True)
    keyboard_thread.start()

    print("Starting block farming bot. Press 'Q' to stop.")
    farm_blocks(repeat_count)
