import random
import os
import json
import time


#these are functions for the buy and sell shop
def buy_item(player):
    """Allows the player to buy items or weapons using gold."""
    shop_items = [
        {"name": "Iron Sword", "ATK": 5.0, "cost": 50, "type": "weapon"},
        {"name": "Health Potion", "heal": 25, "cost": 30, "type": "item"}
    ]
    print("\n--- Shop ---")
    print(f"Gold: {player.get('gold', 0)}")
    for i, item in enumerate(shop_items, start=1):
        if item["type"] == "weapon":
            print(f"{i}. {item['name']} (ATK bonus: {item['ATK']:.1f}) - Cost: {item['cost']} gold")
        else:
            print(f"{i}. {item['name']} - Cost: {item['cost']} gold")
    
    choice = input("Enter the number of the item to buy (or press Enter to cancel): ")
    if choice.strip() == "":
        print("Purchase cancelled.")
        return
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(shop_items):
            print("Invalid selection.")
            return
        selected = shop_items[idx]
        if player["gold"] >= selected["cost"]:
            player["gold"] -= selected["cost"]
            if selected["type"] == "weapon":
                player["inventory"]["weapons"].append({"name": selected["name"], "ATK": selected["ATK"]})
            elif selected["type"] == "item":
                player["inventory"]["items"].append({"name": selected["name"]})
            print(f"Purchased {selected['name']}!")
        else:
            print("Not enough gold!")
    except ValueError:
        print("Invalid input.")

def sell_item(player):
    """Allows the player to sell items or weapons for gold."""
    print("\n--- Sell Items ---")
    print(f"Gold: {player.get('gold', 0)}")
    print("Choose what you want to sell:")
    print("1. Weapon")
    print("2. Item")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        weapons = player["inventory"]["weapons"]
        if not weapons:
            print("No weapons available to sell.")
            return
        print("Select a weapon to sell:")
        for i, weapon in enumerate(weapons, start=1):
            print(f"{i}. {weapon['name']} - Sell Price: 10 gold")
        selection = input("Enter the number of the weapon to sell: ")
        try:
            idx = int(selection) - 1
            if idx < 0 or idx >= len(weapons):
                print("Invalid selection.")
            else:
                sold_weapon = weapons.pop(idx)
                player["gold"] += 10
                print(f"Sold {sold_weapon['name']} for 10 gold.")
        except ValueError:
            print("Invalid input.")
    elif choice == "2":
        items = player["inventory"]["items"]
        if not items:
            print("No items available to sell.")
            return
        print("Select an item to sell:")
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item['name']} - Sell Price: 5 gold")
        selection = input("Enter the number of the item to sell: ")
        try:
            idx = int(selection) - 1
            if idx < 0 or idx >= len(items):
                print("Invalid selection.")
            else:
                sold_item = items.pop(idx)
                player["gold"] += 5
                print(f"Sold {sold_item['name']} for 5 gold.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Invalid choice.")

def save_player(player, filename="player_save.json"):
    """Save player data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(player, f, indent=4)
        print(f"\nPlayer progress saved successfully!")
        return True
    except Exception as e:
        print(f"\nError saving player progress: {e}")
        return False

def load_player(filename="player_save.json"):
    """Load player data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            player = json.load(f)
        # Ensure the player has a gold key, add default if missing.
        if "gold" not in player:
            player["gold"] = 100  # or another default value
        print(f"\nPlayer progress loaded successfully!")
        return player
    except FileNotFoundError:
        print("\nNo saved player data found. Starting new game...")
        return None
    except Exception as e:
        print(f"\nError loading player progress: {e}")
        return None


def save_world(world_state, filename="world_save.json"):
    """Save world progress to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(world_state, f, indent=4)
        print(f"World progress saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving world progress: {e}")
        return False

def load_world(filename="world_save.json"):
    """Load world progress from a JSON file."""
    try:
        with open(filename, 'r') as f:
            world_state = json.load(f)
        print(f"World progress loaded successfully!")
        return world_state
    except FileNotFoundError:
        # Initialize new world state
        return {
            "defeated_enemies": {},  # Format: {"area": ["enemy1", "enemy2", ...]}
            "visited_areas": []
        }
    except Exception as e:
        print(f"Error loading world progress: {e}")
        return None

def update_world_state(world_state, area, enemy_name):
    """Update world state when an enemy is defeated."""
    if area not in world_state["defeated_enemies"]:
        world_state["defeated_enemies"][area] = []
    world_state["defeated_enemies"][area].append(enemy_name)
    
    if area not in world_state["visited_areas"]:
        world_state["visited_areas"].append(area)

def open_inventory(player, in_village=False):
    """Displays and manages the player's inventory.
    If in_village is True, includes options for buying and selling items/weapons."""
    print("\n--- Inventory ---")
    
    # Display player's gold.
    print(f"Gold: {player.get('gold', 0)}")
    
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
    
    # Display options based on location.
    if in_village:
        print("\nInventory Options:")
        print("1. Equip a weapon")
        print("2. Use an item")
        print("3. Buy items/weapons")
        print("4. Sell items/weapons")
        print("5. Exit Inventory")
    else:
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
                    elif item["name"] == "Health Potion":
                        heal_amount = player["max_HP"] * 0.50
                        old_hp = player["HP"]
                        player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                        print(f"You used a Health Potion and restored {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}")
                    else:
                        print("Item effect not implemented.")
            except ValueError:
                print("Invalid input. Exiting inventory.")
        else:
            print("No items available to use.")
    
    # Only show buy/sell options if the player is in the village.
    elif in_village and choice == "3":
        buy_item(player)
    elif in_village and choice == "4":
        sell_item(player)
    elif (in_village and choice == "5") or (not in_village and choice == "3"):
        print("Exiting inventory.")
    else:
        print("Invalid choice. Exiting inventory.")


def choose_class():
    """Player selects a class. Default inventory, equipment, and gold are assigned based on class."""
    classes = {
        "1": {"class": "Wizard", "HP": 12.0, "ATK": 12.0, "DEF": 4.0},
        "2": {"class": "Swordsman", "HP": 15.0, "ATK": 9.0, "DEF": 6.0},
        "3": {"class": "Ranger", "HP": 13.0, "ATK": 10.0, "DEF": 5.0}
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
            # Initialize player's gold
            player["gold"] = 100  
            return player
        else:
            print("Invalid choice. Please select a valid class.")
            
        input("Press Enter to continue...")


def choose_location(player, world_state):
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
        print("6. Exit Game")
        choice = input("Enter the number of your destination: ")
        
        if choice in locations:
            return locations[choice]
        elif choice == "5":
            # In the village, allow buying and selling.
            open_inventory(player, in_village=True)
        elif choice == "6":
            print("Exiting Game...")
            time.sleep(1)
            print("Saved Game Progress Automatically.")
            save_player(player)
            save_world(world_state)
            exit()
        else:
            print("Invalid choice. Please select a valid option.")


def encounter_enemies(area, world_state):
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
    # Filter out defeated enemies
        available_enemies = [
            enemy for enemy in enemies[area]
            if enemy["name"] not in world_state["defeated_enemies"].get(area, [])
        ]
        
        if not available_enemies:
            print(f"\nNo more enemies remain in the {area}!")
            return None
            
        enemy = random.choice(available_enemies)
        print(f"\nWhile in the {area}, you encounter a {enemy['name']}!")
        print(f"Enemy Stats -> HP: {enemy['HP']:.1f}, ATK: {enemy['ATK']:.1f}, DEF: {enemy['DEF']:.1f}")
        return enemy
    else:
        print(f"\nThere are no enemies in the {area}.")
        return None

def battle(player, enemy, world_state, area):
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
            
            raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                player, enemy, weapon_bonus
            )
            
            print(f"\nYou attack with a dice roll of {dice_roll}!")
            print(f"Raw damage: {raw_damage:.1f}")
            print(f"Enemy defense reduces damage by {damage_reduction:.1f}")
            print(f"Final damage dealt: {final_damage:.1f}")
            
            enemy["HP"] -= final_damage
            
            if enemy["HP"] <= 0:
                print(f"You have defeated the {enemy['name']}!")
                update_world_state(world_state, area, enemy["name"])
                save_world(world_state)
                save_player(player)
                break
            
            # Enemy counterattack.
            raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                enemy, player
            )
            print(f"\nThe {enemy['name']} counterattacks with a dice roll of {dice_roll}!")
            print(f"Raw damage: {raw_damage:.1f}")
            print(f"Your defense reduces damage by {damage_reduction:.1f}")
            print(f"Final damage taken: {final_damage:.1f}")
            
            player["HP"] -= final_damage
            
            if player["HP"] <= 0:
                print("You have been defeated!")
                save_world(world_state)
                save_player(player)
                break

        elif action == "2":
            temp_def_bonus = player["DEF"] * 0.5
            player["DEF"] += temp_def_bonus
            
            print("\nYou brace for the enemy's attack! Defense increased by 50%!")
            
            raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                enemy, player
            )
            
            print(f"The {enemy['name']} attacks with a dice roll of {dice_roll}!")
            print(f"Raw damage: {raw_damage:.1f}")
            print(f"Your enhanced defense reduces damage by {damage_reduction:.1f}")
            print(f"Final damage taken: {final_damage:.1f}")
            
            player["HP"] -= final_damage
            
            # Remove temporary defense bonus
            player["DEF"] -= temp_def_bonus
            
            if player["HP"] <= 0:
                save_world(world_state)
                save_player(player)
                print("You have been defeated!")
                break

        elif action == "3":
            run_chance = random.random()
            if run_chance > 0.5:
                print("\nYou successfully escaped the battle!")
                save_world(world_state)
                save_player(player)
                break
            else:
                print("\nEscape failed! The battle continues.")
                raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                    enemy, player
                )
                print(f"As you try to flee, the {enemy['name']} attacks!")
                print(f"You take {final_damage:.1f} damage!")
                player["HP"] -= final_damage
                if player["HP"] <= 0:
                    print("You have been defeated!")
                    save_world(world_state)
                    save_player(player)
                    break
        elif action == "4":
            open_inventory(player)
        else:
            print("\nInvalid action. Please choose again.")

def calculate_damage(attacker, defender, weapon_bonus=0.0):
    """
    Calculate damage dealt by attacker to defender, factoring in:
    - Base attack + weapon bonus
    - Dice roll multiplier
    - Defense reduction
    
    Args:
        attacker (dict): Entity dealing damage with ATK stat
        defender (dict): Entity receiving damage with DEF stat
        weapon_bonus (float): Additional attack bonus from equipped weapon
    
    Returns:
        tuple: (raw_damage, damage_reduction, final_damage)
    """
    # Calculate base damage with weapon bonus if applicable
    base_attack = attacker["ATK"] + weapon_bonus
    
    # Roll dice for damage multiplier (1-6 → 0.1-0.6 multiplier)
    dice_roll = random.randint(1, 6)
    multiplier = dice_roll * 0.1
    
    # Calculate raw damage before defense
    raw_damage = base_attack + (base_attack * multiplier)
    
    # Calculate damage reduction from defense (each point of DEF reduces damage by 10%)
    damage_reduction = raw_damage * (defender["DEF"] / 10)
    
    # Calculate final damage after defense reduction
    final_damage = max(0, raw_damage - damage_reduction)
    
    return raw_damage, damage_reduction, final_damage, dice_roll

def area_loop(player, area, world_state):
    """
    In an area, there's a 30% chance for an immediate enemy encounter.
    If no enemy appears, the player may choose to:
      1. Explore further (guaranteed enemy encounter)
      2. Sleep (restore 25% of max HP)
      3. Return to Village
      4. Open Inventory (without shop options)
    After defeating an enemy, the options reappear.
    """
    while True:
        if player["HP"] <= 0:
            print("You have no HP left. Game Over!")
            break

        if random.random() < 0.3:
            print("\nAn enemy appears out of nowhere!")
            enemy = encounter_enemies(area, world_state)
            if enemy:
                battle(player, enemy, world_state, area)
                if player["HP"] <= 0:
                    break
                continue
        else:
            print(f"\nYou are in the {area} without any immediate threats.")
            print("What would you like to do?")
            print("1. Explore further")
            print("2. Sleep")
            print("3. Return to Village")
            print("4. Open Inventory")
            choice = input("Enter the number of your action: ")
            
            if choice == "1":
                enemy = encounter_enemies(area, world_state)
                if enemy:
                    battle(player, enemy, world_state, area)
                    if player["HP"] <= 0:
                        break
                    continue
            elif choice == "2":
                heal_amount = player["max_HP"] * 0.25
                old_hp = player["HP"]
                player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                print(f"\nYou sleep and restore {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}")
            elif choice == "3":
                print("\nYou return to Spring Village.")
                break
            elif choice == "4":
                # Outside the village, call open_inventory without shop options.
                open_inventory(player, in_village=False)
            else:
                print("Invalid choice. Please choose again.")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Welcome to the Text-Adventure RPG!")
    
    # Choose player class and set up default inventory.
    player = load_player()
    if player is None:
        # If no save exists, create new player
        player = choose_class()
        save_player(player)
    
    world_state = load_world()
        
    print(f"\nYou have chosen {player['class']} with stats:")
    print(f"HP: {player['HP']:.1f}, ATK: {player['ATK']:.1f}, DEF: {player['DEF']:.1f}")
    
    while True:
        if player["HP"] <= 0:
            print("\nGame Over! You have no HP Left!")
            # Option to delete save and start new game
            if input("Start new game? (y/n): ").lower() == 'y':
                os.remove("player_save.json")
                os.remove("world_save.json")
                print("Save files deleted. Restart the game to begin anew.")
            break
        
        # Village: choose destination or access inventory
        destination = choose_location(player, world_state)
        print(f"\nYou leave Spring Village and head towards the {destination}.")
        
        # Begin area exploration loop
        area_loop(player, destination, world_state)
        
        # Auto-save after returning to village
        save_player(player)
        save_world(world_state)
    
    print("\nThank you for playing!")

if __name__ == "__main__":
    main()
