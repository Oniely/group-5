import time
import keyboard

def forest():
    
    
    while True:
        print("FOREST")
        
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            main() 

def cave():
    # Example structure for cave; you can modify similarly.
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
