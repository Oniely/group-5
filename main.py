import random
import os
import json
import time

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
        "1": {"class": "Wizard", "HP": 20.0, "ATK": 6.0, "DEF": 4.0},
        "2": {"class": "Swordsman", "HP": 25.0, "ATK": 5.0, "DEF": 6.0},
        "3": {"class": "Ranger", "HP": 22.0, "ATK": 5.5, "DEF": 5.0}
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
            open_inventory(player)
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
            {"name": "Diwata", "HP": 18.0, "ATK": 4.5, "DEF": 4.0, "DROPS": ["Healing Herb", "Enchanted Leaf"]},
            {"name": "Kapri", "HP": 20.0, "ATK": 4.0, "DEF": 5.0, "DROPS": ["Mystic Acorn", "Wooden Charm"]},
            {"name": "Tikbalang", "HP": 22.0, "ATK": 5.5, "DEF": 3.0, "DROPS": ["Hoof Pendant", "Lucky Feather"]}
        ],
        "Mountains": [
            {"name": "Mananggal", "HP": 25.0, "ATK": 5.0, "DEF": 4.0, "DROPS": ["Bat Wing", "Cursed Fang"]},
            {"name": "Tyanak", "HP": 18.0, "ATK": 6.0, "DEF": 3.5, "DROPS": ["Demonic Doll", "Tiny Claw"]},
            {"name": "Tik-tik", "HP": 20.0, "ATK": 5.0, "DEF": 5.0, "DROPS": ["Shadow Feather", "Dark Essence"]}
        ],
        "Cave": [
            {"name": "Skeleton", "HP": 16.0, "ATK": 4.5, "DEF": 3.0, "DROPS": ["Bone Fragment", "Rusty Sword"]},
            {"name": "Cave Bat", "HP": 15.0, "ATK": 4.0, "DEF": 3.0, "DROPS": ["Bat Fang", "Echo Crystal"]},
            {"name": "Goblin", "HP": 18.0, "ATK": 5.0, "DEF": 4.0, "DROPS": ["Goblin Dagger", "Gold Nugget"]}
        ],
        "Swamp": [
            {"name": "Swamp Beast", "HP": 24.0, "ATK": 5.0, "DEF": 5.0, "DROPS": ["Swamp Sludge", "Toxic Fang"]},
            {"name": "Bog Creature", "HP": 20.0, "ATK": 4.5, "DEF": 4.0, "DROPS": ["Rotten Bark", "Cursed Gem"]},
            {"name": "Mud Monster", "HP": 22.0, "ATK": 4.0, "DEF": 6.0, "DROPS": ["Hardened Mud", "Dark Shard"]}
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

def display_battle_screen(player, enemy):
    """Display a Pokemon-style battle screen with ASCII art"""
    clear_terminal()
    print("\n" + "="*60)
    print(f"Your {player['class']:<30} Enemy {enemy['name']}")
    print(f"HP: {player['HP']:.1f}/{player['max_HP']:.1f}{' '*20}HP: {enemy['HP']:.1f}/{enemy['max_HP']:.1f}")
    print("\n")
    print(fr"   O    {' '*20}     /\___/\ ")
    print(fr"  /|\   {' '*20}    (  o o  )")
    print(fr"  / \   {' '*20}     >  ^  <")
    print("\n" + "="*60)
    
def display_attack_animation(attacker_name, defender_name, damage, is_player):
    """Display attack animation with ASCII art"""
    # Forward attack animation
    forward_animations = [
        ">>----->",
        " >>---->",
        "  >>--->",
        "   >>-->",
        "    >>->",
        "     >>>"
    ]
    
    # Backward attack animation
    backward_animations = [
        "<-----<<",
        "<----<< ",
        "<---<<  ",
        "<--<<   ",
        "<-<<    ",
        "<<<     "
    ]
    
    animations = forward_animations if is_player else backward_animations
    
    for frame in animations:
        clear_terminal()
        print("\n" * 2)
        if is_player:
            print(" "*10 + frame + " "*20)  # Player attacks right to left
        else:
            print(" "*20 + frame + " "*10)  # Enemy attacks left to right
        print("\n" * 2)
        time.sleep(0.1)
    
    print(f"\n{attacker_name} deals {damage:.1f} damage to {defender_name}!")
    time.sleep(1)

def display_defend_animation(defender_name):
    """Display defend animation with ASCII art"""
    animations = [
        "╔═══╗",
        "║   ║",
        "╚═══╝"
    ]
    
    clear_terminal()
    print("\n" * 2)
    for line in animations:
        print(" "*20 + line)
    print(f"\n{defender_name} takes a defensive stance!")
    time.sleep(1)

def battle(player, enemy, world_state, area):
    """Battle loop with Pokemon-style animations"""
    # Add max_HP to enemy for HP bar display
    enemy["max_HP"] = enemy["HP"]
    
    print(f"\nA wild {enemy['name']} appears!")
    time.sleep(1)
    
    while player["HP"] > 0 and enemy["HP"] > 0:
        display_battle_screen(player, enemy)
        print("\nWhat will you do?")
        print("1. Attack")
        print("2. Defend")
        print("3. Run")
        print("4. Open Inventory")
        action = input("Enter your choice: ")
        
        if action == "1":
            weapon_bonus = player["equipped_weapon"]["ATK"] if player.get("equipped_weapon") else 0.0
            raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                player, enemy, weapon_bonus
            )
            
            # Player Attack
            display_attack_animation(player["class"], enemy["name"], final_damage, True)
            enemy["HP"] -= final_damage
            
            if enemy["HP"] <= 0:
                display_battle_screen(player, enemy)
                print(f"\nThe {enemy['name']} has been defeated!")
                update_world_state(world_state, area, enemy["name"])
                
                
                save_world(world_state)
                save_player(player)
                time.sleep(2)
                break
            
            # Enemy counterattack
            raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                enemy, player
            )
            
            display_attack_animation(enemy["name"], player["class"], final_damage, False)
            player["HP"] -= final_damage
            
            if player["HP"] <= 0:
                display_battle_screen(player, enemy)
                print("\nYou have been defeated!")
                save_world(world_state)
                save_player(player)
                time.sleep(2)
                break

        elif action == "2":
            temp_def_bonus = player["DEF"] * 0.5
            player["DEF"] += temp_def_bonus
            
            display_defend_animation(player["class"])
            
            raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                enemy, player
            )
            
            display_attack_animation(enemy["name"], player["class"], final_damage, False)
            player["HP"] -= final_damage
            
            player["DEF"] -= temp_def_bonus
            
            if player["HP"] <= 0:
                display_battle_screen(player, enemy)
                print("\nYou have been defeated!")
                save_world(world_state)
                save_player(player)
                time.sleep(2)
                break

        elif action == "3":
            run_chance = random.random()
            if run_chance > 0.5:
                print("\nYou successfully escaped the battle!")
                save_world(world_state)
                save_player(player)
                time.sleep(2)
                break
            else:
                print("\nEscape failed! The battle continues.")
                raw_damage, damage_reduction, final_damage, dice_roll = calculate_damage(
                    enemy, player
                )
                print(f"As you try to flee, the {enemy['name']} attacks!")
                print(f"You take {final_damage:.1f} damage!")
                player["HP"] -= final_damage
                
                time.sleep(1)
                
                if player["HP"] <= 0:
                    print("You have been defeated!")
                    save_world(world_state)
                    save_player(player)
                    break
        elif action == "4":
            open_inventory(player)
        else:
            print("\nInvalid action. Please choose again.")
            time.sleep(1)

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
            enemy = encounter_enemies(area, world_state)
            if enemy:
                battle(player, enemy, world_state, area)
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
                enemy = encounter_enemies(area, world_state)
                if enemy:
                    battle(player, enemy, world_state, area)
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
