import random

def open_inventory(player):
    """Displays and manages the player's inventory."""
    print("\n--- Inventory ---")
    
    # Display equipped weapon.
    equipped = player.get("equipped_weapon")
    if equipped:
        print(f"Equipped Weapon: {equipped['name']} (ATK bonus: {equipped['ATK']:.1f})")
    else:
        print("No weapon equipped.")
    
    # List available weapons.
    weapons = player["inventory"]["weapons"]
    if weapons:
        print("Weapons in inventory:")
        for i, weapon in enumerate(weapons, start=1):
            print(f"  {i}. {weapon['name']} (ATK bonus: {weapon['ATK']:.1f})")
    else:
        print("No additional weapons in inventory.")
    
    # List available consumable items.
    items = player["inventory"]["items"]
    if items:
        print("Items:")
        for i, item in enumerate(items, start=1):
            print(f"  {i}. {item['name']}")
    else:
        print("No items in inventory.")
    
    print("\nInventory Options:")
    print("1. Equip a weapon")
    print("2. Use an item")
    print("3. Exit Inventory")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        if weapons:
            print("\nSelect a weapon to equip:")
            for i, weapon in enumerate(weapons, start=1):
                print(f"  {i}. {weapon['name']} (ATK bonus: {weapon['ATK']:.1f})")
            equip_choice = input("Enter the number of the weapon to equip: ")
            try:
                idx = int(equip_choice) - 1
                if idx < 0 or idx >= len(weapons):
                    print("Invalid selection. Exiting inventory.")
                else:
                    player["equipped_weapon"] = weapons[idx]
                    print(f"You have equipped {player['equipped_weapon']['name']}.")
            except ValueError:
                print("Invalid input. Exiting inventory.")
        else:
            print("No weapons available to equip.")
    elif choice == "2":
        if items:
            print("\nSelect an item to use:")
            for i, item in enumerate(items, start=1):
                print(f"  {i}. {item['name']}")
            item_choice = input("Enter the number of the item to use: ")
            try:
                idx = int(item_choice) - 1
                if idx < 0 or idx >= len(items):
                    print("Invalid selection. Exiting inventory.")
                else:
                    item = items.pop(idx)  # Remove the item from inventory once used.
                    if item["name"] == "Small Potion":
                        heal_amount = player["max_HP"] * 0.25
                        old_hp = player["HP"]
                        player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                        print(f"You used a Small Potion and restored {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}")
                    elif item["name"] == "Bomb":
                        print("You throw a Bomb! (Bomb effect not implemented yet.)")
                    else:
                        print("Item effect not implemented.")
            except ValueError:
                print("Invalid input. Exiting inventory.")
        else:
            print("No items available to use.")
    elif choice == "3":
        print("Exiting inventory.")
    else:
        print("Invalid choice. Exiting inventory.")

def choose_class():
    """Player selects a class. Default inventory and equipment are assigned based on class."""
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
            player["max_HP"] = player["HP"]
            # Set up a default inventory with a basic weapon and one Small Potion.
            if choice == "1":
                default_weapon = {"name": "Basic Staff", "ATK": 2.0}
            elif choice == "2":
                default_weapon = {"name": "Basic Sword", "ATK": 2.0}
            else:
                default_weapon = {"name": "Basic Bow", "ATK": 2.0}
            player["inventory"] = {
                "weapons": [default_weapon],
                "items": [{"name": "Small Potion"}]
            }
            player["equipped_weapon"] = default_weapon
            return player
        else:
            print("Invalid choice. Please select a valid class.")

def choose_location(player):
    """Player chooses an area from Spring Village. The inventory is accessible here too."""
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
        print("5. Open Inventory")
        choice = input("Enter the number of your destination: ")
        
        if choice in locations:
            return locations[choice]
        elif choice == "5":
            open_inventory(player)
        else:
            print("Invalid choice. Please select a valid option.")

def encounter_enemies(area):
    """Randomly selects an enemy for the given area."""
    enemies = {
        "Forest": [
            {"name": "Diwata", "HP": 8.0, "ATK": 5.0, "DEF": 3.0},
            {"name": "Kapri", "HP": 10.0, "ATK": 6.0, "DEF": 4.0},
            {"name": "Tikbalang", "HP": 9.0, "ATK": 7.0, "DEF": 2.0}
        ],
        "Mountains": [
            {"name": "Mananggal", "HP": 10.0, "ATK": 6.0, "DEF": 3.0},
            {"name": "Tyanak", "HP": 8.0, "ATK": 7.0, "DEF": 3.0},
            {"name": "Tik-tik", "HP": 9.0, "ATK": 5.0, "DEF": 4.0}
        ],
        "Cave": [
            {"name": "Skeleton", "HP": 7.0, "ATK": 5.0, "DEF": 2.0},
            {"name": "Cave Bat", "HP": 6.0, "ATK": 4.0, "DEF": 2.0},
            {"name": "Goblin", "HP": 8.0, "ATK": 6.0, "DEF": 3.0}
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
    """Battle loop where the player can attack, defend, run, or access inventory."""
    print(f"\nBattle Start! You vs. {enemy['name']}")
    while player["HP"] > 0 and enemy["HP"] > 0:
        print(f"\nYour HP: {player['HP']:.1f} | {enemy['name']} HP: {enemy['HP']:.1f}")
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Run")
        print("4. Open Inventory")
        action = input("Enter the number of your action: ")
        
        if action == "1":
            # Calculate player's total attack (base ATK + equipped weapon bonus).
            weapon_bonus = player["equipped_weapon"]["ATK"] if player.get("equipped_weapon") else 0.0
            base_attack = player["ATK"] + weapon_bonus
            dice_roll = random.randint(1, 6)
            multiplier = dice_roll * 0.1  # E.g., dice roll 5 => 0.5 multiplier.
            damage = base_attack + (base_attack * multiplier)
            print(f"\nYou attack with a dice roll of {dice_roll} (multiplier {multiplier:.1f}), dealing {damage:.1f} damage!")
            enemy["HP"] -= damage
            
            if enemy["HP"] <= 0:
                print(f"You have defeated the {enemy['name']}!")
                break
            
            # Enemy counterattack.
            enemy_dice = random.randint(1, 6)
            enemy_multiplier = enemy_dice * 0.1
            enemy_damage = enemy["ATK"] + (enemy["ATK"] * enemy_multiplier)
            print(f"The {enemy['name']} counterattacks with a dice roll of {enemy_dice} (multiplier {enemy_multiplier:.1f}), dealing {enemy_damage:.1f} damage!")
            player["HP"] -= enemy_damage
            
            if player["HP"] <= 0:
                print("You have been defeated!")
                break

        elif action == "2":
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
        elif action == "4":
            open_inventory(player)
        else:
            print("\nInvalid action. Please choose again.")

def area_loop(player, area):
    """
    In an area, there's a 30% chance for an immediate enemy encounter.
    If no enemy appears, the player may choose to:
      1. Explore further (guaranteed enemy encounter)
      2. Sleep (restore 25% of max HP)
      3. Return to Village
      4. Open Inventory
    After defeating an enemy, the options reappear.
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
                continue  # After battle, re-check the area.
        else:
            print(f"\nYou are in the {area} without any immediate threats.")
            print("What would you like to do?")
            print("1. Explore further")
            print("2. Sleep")
            print("3. Return to Village")
            print("4. Open Inventory")
            choice = input("Enter the number of your action: ")
            
            if choice == "1":
                enemy = encounter_enemies(area)
                if enemy:
                    battle(player, enemy)
                    if player["HP"] <= 0:
                        break
                    continue  # Return to area options after battle.
            elif choice == "2":
                heal_amount = player["max_HP"] * 0.25
                old_hp = player["HP"]
                player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                print(f"\nYou sleep and restore {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}")
            elif choice == "3":
                print("\nYou return to Spring Village.")
                break
            elif choice == "4":
                open_inventory(player)
            else:
                print("Invalid choice. Please choose again.")

def main():
    print("Welcome to the Text-Adventure RPG!")
    
    # Choose player class and set up default inventory.
    player = choose_class()
    print(f"\nYou have chosen {player['class']} with stats:")
    print(f"HP: {player['HP']:.1f}, ATK: {player['ATK']:.1f}, DEF: {player['DEF']:.1f}")
    
    # Village: choose destination or access inventory.
    destination = choose_location(player)
    print(f"\nYou leave Spring Village and head towards the {destination}.")
    
    # Begin area exploration loop.
    area_loop(player, destination)
    
    print("\nThank you for playing!")

if __name__ == "__main__":
    main()
