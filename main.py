<<<<<<< Updated upstream
import time
import keyboard
import random

global player
player = {}

inventory = { "Potion": 2, "Gold": 50 }

def select_class():
    print("Choose your class:")
    print("1. Wizard (High magic, low defense)")
    print("2. Swordsman (Balanced offense & defense)")
    print("3. Ranger (High speed, long-range attacks)")
    
    choice = input("Enter choice (1/2/3): ")
    if choice == "1":
        return {"class": "Wizard", "HP": 12, "ATK": 8, "DEF": 4}
    elif choice == "2":
        return {"class": "Swordsman", "HP": 15, "ATK": 10, "DEF": 6}
    elif choice == "3":
        return {"class": "Ranger", "HP": 13, "ATK": 9, "DEF": 5}
    else:
        print("Invalid choice, try again.")
        return select_class()
    
def battle(player, enemy):
    print("Player stats:", player)
    print("Enemy stats:", enemy)
    
    print(f"A wild {enemy.get('name', 'Enemy')} appears!")
    
    while player['HP'] > 0 and enemy["HP"] > 0:
        action = input("Choose action: (Attack/Defend/Run) ").lower()
        
        # roll formula for damage/def
        if action == "attack":
            damage = max(1, player["ATK"] - enemy["DEF"])
            enemy["HP"] -= damage
            print(f"You attack! {enemy.get('name', 'Enemy')} loses {damage} HP.")
        elif action == "defend":
            player["DEF"] += 2
            print("You brace for impact, increasing defense!")
        elif action == "run":
            if random.random() > 0.5:
                print("You successfully escaped!")
                return
            else:
                print("Failed to run!")
        else:
            print("Invalid action. Try again.")
            continue

        if enemy["HP"] > 0:
            enemy_damage = max(1, enemy.get("ATK", 0) - player["DEF"])
            player["HP"] -= enemy_damage

            print(f"{enemy.get('name', 'Enemy')} attacks! You lose {enemy_damage} HP.")

    if player["HP"] <= 0:
        print("Game Over!")
    else:
        lenArray = len(enemy["DROPS"])
        randomDrop = 0
        quantity = random.randint(1, 3)
        
        add_item(enemy["DROPS"][randomDrop], quantity)
        print(f"You defeated {enemy.get('name', 'Enemy')}!")
        
def add_item(item, quantity=1):
    if item in inventory:
        inventory[item] += quantity
    else:
        inventory[item] = quantity
    print(f"Added {quantity} {item}(s) to inventory!")

def forest():
    forest_enemies = {
        'Diwata': {
            "name": "Diwata",
            "HP": 2,
            "DEF": 5,
            "ATK": 6,
            "DROPS": ["Hamburger"]
        },
        'Kapri': {
            "name": "Kapri",
            "HP": 8,
            "DEF": 3,
            "ATK": 5,
            "DROPS": ["Cigars"]
        },
        'Boss': {
            "name": "Boss",
            "HP": 15,
            "DEF": 8,
            "ATK": 10,
            "DROPS": ["Bossing"]
        },
    }
    
    battle(player, forest_enemies['Diwata'])

def cave():
    while True:
        print("CAVE")
        if keyboard.is_pressed("esc"):
            print("Exiting CAVE...")
            main()
            break  # Prevent multiple calls to main()

def swamp():
    while True:
        print("SWAMP")
        if keyboard.is_pressed("esc"):
            print("Exiting SWAMP...")
            main()
            break

def mountain():
    while True:
        print("MOUNTAIN")
        if keyboard.is_pressed("esc"):
            print("Exiting MOUNTAIN...")
            main()
            break

def display_player_hp():
    print(f"Player HP: {player.get('HP', 'Unknown')}")

def display_boss_hp(difficulty):
    # Placeholder for boss HP display logic based on difficulty.
    pass

def starting():
    print("Welcome to Spring Village!")
    print("You wake up in a Village. You see a path leading left, right, up, and down.")

def main():
    global player
    starting()
    
    player = select_class()
    print("Your character:", player)
    
    print("Choose a direction: up (Forest), down (Cave), left (Swamp), right (Mountain)")
    
    while True:
        
        if keyboard.is_pressed("up"):
            forest()
        elif keyboard.is_pressed("down"):
            cave()
        elif keyboard.is_pressed("left"):
            swamp()
        elif keyboard.is_pressed("right"):
            mountain()

<<<<<<< HEAD
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
=======
if __name__ == "__main__":
    main()
>>>>>>> 9e65ec661764ffd6b952fcc224fe9248d7ca0a97
