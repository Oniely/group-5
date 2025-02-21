<<<<<<< Updated upstream
import time
import keyboard

def forest():
    
    
    while True:
        print("FOREST")
        
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            main()

def cave():
    while True:
        print("CAVE")
        
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            main()
        

def swamp():
    while True:
        print("SWAMP")
        
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            main()

def mountain():
    while True:
        print("MOUNTAIN")
        
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            main()

def display_player_hp():
    pass

def display_boss_hp(difficulty):
    pass

def starting():
    print("Welcome to Spring Village!")
    time.sleep(1)
    print("You wake up in a Village. You see a path leading left, right, up, and down.") 

def main():
    starting()
    
    while True:
        if keyboard.is_pressed("up"):
            forest()
        elif keyboard.is_pressed("down"):
            cave()
        elif keyboard.is_pressed("left"):
            swamp()
        elif keyboard.is_pressed("right"):
            mountain()

main()
=======
import sys

# Define a cross-platform getch function.
try:
    # Windows implementation
    import msvcrt

    def getch():
        ch = msvcrt.getch()
        # If an arrow key is pressed, msvcrt.getch() returns a prefix (b'\x00' or b'\xe0').
        # You must call getch() again to get the actual key code.
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            return ch.decode('utf-8')
        else:
            return ch.decode('utf-8')
except ImportError:
    # Unix-like system implementation
    import tty, termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch1 = sys.stdin.read(1)
            # Arrow keys on Unix return an escape sequence starting with '\x1b'
            if ch1 == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return ch3  # This will be 'A', 'B', 'C', or 'D'
            return ch1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Mapping explanation:
# On Windows (using msvcrt.getch), arrow keys return:
#   Up:    'H'
#   Down:  'P'
#   Left:  'K'
#   Right: 'M'
#
# On Unix-like systems, the getch function above returns:
#   Up:    'A'
#   Down:  'B'
#   Right: 'C'
#   Left:  'D'
#
# You can map these to numeric options as needed.

def get_direction_option():
    print("Press an arrow key to choose an option:")
    print("  Up Arrow    → Option 1")
    print("  Down Arrow  → Option 2")
    print("  Left Arrow  → Option 3")
    print("  Right Arrow → Option 4")
    
    ch = getch()
    
    # Map the keys accordingly, accommodating differences between Windows and Unix.
    if ch in ('H', 'A'):  # 'H' on Windows, 'A' on Unix for Up arrow.
        return 1
    elif ch in ('P', 'B'):  # 'P' on Windows, 'B' on Unix for Down arrow.
        return 2
    elif ch in ('K', 'D'):  # 'K' on Windows, 'D' on Unix for Left arrow.
        return 3
    elif ch in ('M', 'C'):  # 'M' on Windows, 'C' on Unix for Right arrow.
        return 4
    else:
        return None

# Example usage in a text-based adventure:
print("Text-Based Adventure Game")
print("Where do you want to go?")

# Instead of asking for a number with input(), we wait for an arrow key press.
option = get_direction_option()

if option == 1:
    print("You have gone to the forest")
elif option == 2:
    print("You have gone to the swamp")
elif option == 3:
    print("You have gone to the mountains")
elif option == 4:
    print("You have gone to the castle")
else:
    print("Invalid key pressed!")
>>>>>>> Stashed changes
