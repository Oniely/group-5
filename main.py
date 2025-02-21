def choose_class():
    classes = {
        "1": {"class": "Wizard", "HP": 12, "ATK": 8, "DEF": 4},
        "2": {"class": "Swordsman", "HP": 15, "ATK": 10, "DEF": 6},
        "3": {"class": "Ranger", "HP": 13, "ATK": 9, "DEF": 5}
    }

    while True:
        print("\nChoose your class:")
        print("1. Wizard")
        print("2. Swordsman")
        print("3. Ranger")
        choice = input("Enter the number of your choice: ")

        if choice in classes:
            return classes[choice]
        else:
            print("Invalid choice. Please select a valid class.")

def choose_location():
    locations = {
        "1": "Forest",
        "2": "Cave",
        "3": "Mountains",
        "4": "Swamp"
    }

    while True:
        print("\nWelcome to Spring Village!")
        print("Where would you like to go?")
        print("1. Forest")
        print("2. Cave")
        print("3. Mountains")
        print("4. Swamp")
        choice = input("Enter the number of your destination: ")

        if choice in locations:
            return locations[choice]
        else:
            print("Invalid choice. Please select a valid location.")

def main():
    print("Welcome to the Text-Adventure RPG!")
    player = choose_class()
    print(f"\nYou have chosen {player['class']} with stats:")
    print(f"HP: {player['HP']}, ATK: {player['ATK']}, DEF: {player['DEF']}")

    destination = choose_location()
    print(f"\nYou leave Spring Village and head towards the {destination}.")

if __name__ == "__main__":
    main()