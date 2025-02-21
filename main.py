import random

def choose_class():
    classes = {
        "1": {"class": "Wizard", "HP": 12.0, "ATK": 8.0, "DEF": 4.0},
        "2": {"class": "Swordsman", "HP": 15.0, "ATK": 10.0, "DEF": 6.0},
        "3": {"class": "Ranger", "HP": 13.0, "ATK": 9.0, "DEF": 5.0}
    }
    
    while True:
        print("\nChoose your class:")
        print("1. Wizard")
        print("2. Swordsman")
        print("3. Ranger")
        choice = input("Enter the number of your choice: ")
        
        if choice in classes:
            player = classes[choice]
            # Store maximum HP for healing later.
            player["max_HP"] = player["HP"]
            return player
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

def encounter_enemies(area):
    # Each enemy is defined with float stats.
    enemies = {
        "Forest": [
            {"name": "Diwata", "HP": 8.0, "ATK": 5.0, "DEF": 3.0},
            {"name": "Kapri", "HP": 10.0, "ATK": 6.0, "DEF": 4.0},
            {"name": "Tikbalang", "HP": 9.0, "ATK": 7.0, "DEF": 2.0}
        ],
        "Mountains": [
            {"name": "Bandit", "HP": 10.0, "ATK": 6.0, "DEF": 3.0},
            {"name": "Giant Centipede", "HP": 8.0, "ATK": 7.0, "DEF": 3.0},
            {"name": "Rodent", "HP": 9.0, "ATK": 5.0, "DEF": 4.0}
        ],
        "Cave": [
            {"name": "Mananggal", "HP": 7.0, "ATK": 5.0, "DEF": 2.0},
            {"name": "Tyanak", "HP": 6.0, "ATK": 4.0, "DEF": 2.0},
            {"name": "Tik-tik", "HP": 8.0, "ATK": 6.0, "DEF": 3.0}
        ],
        "Swamp": [
            {"name": "Swamp Beast", "HP": 9.0, "ATK": 6.0, "DEF": 3.0},
            {"name": "Bog Creature", "HP": 8.0, "ATK": 5.0, "DEF": 2.0},
            {"name": "Mud Monster", "HP": 7.0, "ATK": 4.0, "DEF": 2.0}
        ]
    }
    
    if area in enemies:
        enemy = random.choice(enemies[area])
        print(f"\nWhile in the {area}, you encounter a {enemy['name']}!")
        print(f"Enemy Stats -> HP: {enemy['HP']:.1f}, ATK: {enemy['ATK']:.1f}, DEF: {enemy['DEF']:.1f}")
        return enemy
    else:
        print(f"\nThere are no enemies in the {area}.")
        return None

def battle(player, enemy):
    print(f"\nBattle Start! You vs. {enemy['name']}")
    # Battle continues until one side is defeated or the player successfully runs.
    while player["HP"] > 0 and enemy["HP"] > 0:
        print(f"\nYour HP: {player['HP']:.1f} | {enemy['name']} HP: {enemy['HP']:.1f}")
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Run")
        action = input("Enter the number of your action: ")
        
        if action == "1":
            # Player attack: dice roll adds a multiplier to the base ATK.
            dice_roll = random.randint(1, 6)
            multiplier = dice_roll * 0.1
            damage = player["ATK"] + (player["ATK"] * multiplier)
            print(f"\nYou attack with a dice roll of {dice_roll} (multiplier {multiplier:.1f}), dealing {damage:.1f} damage!")
            enemy["HP"] -= damage
            
            if enemy["HP"] <= 0:
                print(f"You have defeated the {enemy['name']}!")
                break
            
            # Enemy counterattacks.
            enemy_dice = random.randint(1, 6)
            enemy_multiplier = enemy_dice * 0.1
            enemy_damage = enemy["ATK"] + (enemy["ATK"] * enemy_multiplier)
            print(f"The {enemy['name']} counterattacks with a dice roll of {enemy_dice} (multiplier {enemy_multiplier:.1f}), dealing {enemy_damage:.1f} damage!")
            player["HP"] -= enemy_damage
            
            if player["HP"] <= 0:
                print("You have been defeated!")
                break

        elif action == "2":
            # Defend: reduce incoming enemy attack by player's defense percentage.
            print("\nYou brace for the enemy's attack!")
            enemy_dice = random.randint(1, 6)
            enemy_multiplier = enemy_dice * 0.1
            enemy_damage = enemy["ATK"] + (enemy["ATK"] * enemy_multiplier)
            damage_reduction = enemy_damage * (player["DEF"] / 10)
            effective_damage = enemy_damage - damage_reduction
            print(f"The {enemy['name']} attacks with a dice roll of {enemy_dice} (multiplier {enemy_multiplier:.1f}), dealing {enemy_damage:.1f} damage!")
            print(f"Your defense reduces the damage by {damage_reduction:.1f}, so you take {effective_damage:.1f} damage!")
            player["HP"] -= effective_damage
            
            if player["HP"] <= 0:
                print("You have been defeated!")
                break

        elif action == "3":
            # Attempt to run with a 50% chance of success.
            run_chance = random.random()
            if run_chance > 0.5:
                print("\nYou successfully escaped the battle!")
                break
            else:
                print("\nEscape failed! The battle continues.")
                enemy_dice = random.randint(1, 6)
                enemy_multiplier = enemy_dice * 0.1
                enemy_damage = enemy["ATK"] + (enemy["ATK"] * enemy_multiplier)
                print(f"As you try to flee, the {enemy['name']} attacks, dealing {enemy_damage:.1f} damage!")
                player["HP"] -= enemy_damage
                if player["HP"] <= 0:
                    print("You have been defeated!")
                    break
        else:
            print("\nInvalid action. Please choose again.")

def area_loop(player, area):
    """
    Manages what happens when the player is in an area.
    A 30% chance for a random enemy encounter is checked first.
    If no enemy appears, the player can choose to explore further (guaranteed encounter),
    sleep (restore 25% of max HP), or return to the village.
    """
    while True:
        if player["HP"] <= 0:
            print("You have no HP left. Game Over!")
            break

        # 30% chance for an immediate enemy encounter.
        if random.random() < 0.3:
            print("\nAn enemy appears out of nowhere!")
            enemy = encounter_enemies(area)
            if enemy:
                battle(player, enemy)
                if player["HP"] <= 0:
                    break
                # After battle, redirect back to area options.
                continue
        else:
            print(f"\nYou are in the {area} without any immediate threats.")
            print("What would you like to do?")
            print("1. Explore further")
            print("2. Sleep")
            print("3. Return to Village")
            choice = input("Enter the number of your action: ")
            
            if choice == "1":
                # Active exploration guarantees an enemy encounter.
                enemy = encounter_enemies(area)
                if enemy:
                    battle(player, enemy)
                    if player["HP"] <= 0:
                        break
                    continue  # Return to area options after battle.
            elif choice == "2":
                # Sleep and restore 25% of the player's max HP.
                heal_amount = player["max_HP"] * 0.25
                old_hp = player["HP"]
                player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                print(f"\nYou sleep and restore {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}")
            elif choice == "3":
                print("\nYou return to Spring Village.")
                choose_location()
            else:
                print("Invalid choice. Please choose again.")

def main():
    print("Welcome to the Text-Adventure RPG!")
    
    # Choose player class.
    player = choose_class()
    print(f"\nYou have chosen {player['class']} with stats:")
    print(f"HP: {player['HP']:.1f}, ATK: {player['ATK']:.1f}, DEF: {player['DEF']:.1f}")
    
    # Choose destination.
    destination = choose_location()
    print(f"\nYou leave Spring Village and head towards the {destination}.")
    
    # Begin area loop.
    area_loop(player, destination)
    
    print("\nThank you for playing!")

if __name__ == "__main__":
    main()
