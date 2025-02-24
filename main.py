import random
import os
import json
import time



# these are functions for the buy and sell shop
def buy_item(player):
    """Allows the player to buy items or weapons using gold."""
    shop_items = [
        {"name": "Iron Sword", "ATK": 5.0, "cost": 50, "type": "weapon"},
        {"name": "Health Potion", "heal": 25, "cost": 30, "type": "item"},
    ]
    print("\n--- Shop ---")
    print(f"Gold: {player.get('gold', 0)}")
    for i, item in enumerate(shop_items, start=1):
        if item["type"] == "weapon":
            print(
                f"{i}. {item['name']} (ATK bonus: {item['ATK']:.1f}) - Cost: {item['cost']} gold"
            )
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
                player["inventory"]["weapons"].append(
                    {"name": selected["name"], "ATK": selected["ATK"]}
                )
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
        with open(filename, "w") as f:
            json.dump(player, f, indent=4)
        print("\nPlayer progress saved successfully!")
        return True
    except Exception as e:
        print(f"\nError saving player progress: {e}")
        return False


def load_player(filename="player_save.json"):
    """Load player data from a JSON file."""
    try:
        with open(filename, "r") as f:
            player = json.load(f)
        # Ensure the player has a gold key, add default if missing.
        if "gold" not in player:
            player["gold"] = 100  # or another default value
        print("\nPlayer progress loaded successfully!")
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
        with open(filename, "w") as f:
            json.dump(world_state, f, indent=4)
        print("World progress saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving world progress: {e}")
        return False


def load_world(filename="world_save.json"):
    """Load world progress from a JSON file."""
    try:
        with open(filename, "r") as f:
            world_state = json.load(f)
        print("World progress loaded successfully!")
        return world_state
    except FileNotFoundError:
        # Initialize new world state
        return {
            "defeated_enemies": {},  # Format: {"area": ["enemy1", "enemy2", ...]}
            "visited_areas": [],
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

# (Optional) Update open_inventory so that it no longer shows buy/sell options when in the village:
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
    
    # Provide a simple inventory management menu (without buy/sell options)
    print("\nInventory Options:")
    print("1. Equip a weapon")
    print("2. Use an item")
    print("3. Search Inventory")
    print("4. Exit Inventory")
    
    choice = input("\nEnter your choice: ")

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
                    save_player(player)
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
                        heal_amount = player["max_HP"] * item["heal"]
                        old_hp = player["HP"]
                        player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                        print(f"You used a Small Potion and restored {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}")
                    elif item["name"] == "Health Potion":
                        heal_amount = player["max_HP"] * item["heal"]
                        old_hp = player["HP"]
                        player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                        print(
                            f"You used a Health Potion and restored {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}"
                        )
                    else:
                        print("Item effect not implemented.")
                    
                    save_player(player)

            except ValueError:
                print("Invalid input. Exiting inventory.")
        else:
            print("No items available to use.")
    elif choice == "3": 
        search_inventory(player)
    # Only show buy/sell options if the player is in the village.
    elif in_village and choice == "4":
        buy_item(player)
    elif in_village and choice == "5":
        sell_item(player)
    elif (in_village and choice == "6") or (not in_village and choice == "4"):
        print("Exiting inventory.")
    else:
        print("Invalid choice. Exiting inventory.")


def search_inventory(player):
    keyword = input("\nSearch From Inventory: ").lower().strip()

    found_items = []

    if keyword == "":
        return

    print("\n--- Search Results ---")
    # Search weapons
    for i, weapon in enumerate(player["inventory"]["weapons"]):
        if keyword in weapon["name"].lower():
            found_items.append(("weapon", i, weapon))

    # Search items
    for i, item in enumerate(player["inventory"]["items"]):
        if keyword in item["name"].lower():
            found_items.append(("item", i, item))

    if not found_items:
        print("No matching items found.")
        try_again = input("\nTry again? (y/others): ").lower().strip()

        if try_again == "y":
            clear_terminal()
            search_inventory(player)
        else:
            return

    # Display results
    for i, (item_type, idx, item) in enumerate(found_items, 1):
        if item_type == "weapon":
            print(f"{i}. {item['name']} (Weapon, ATK: {item['ATK']:.1f})")
        else:
            print(f"{i}. {item['name']} (Item)")

    # Let user select an item from results
    choice = ""
    if found_items:
        choice = input(
            "\nSelect an item number to use/equip (or press Enter to cancel): "
        )

    if choice.strip():
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(found_items):
                item_type, original_idx, item = found_items[idx]
                if item_type == "weapon":
                    # Equip weapon
                    player["equipped_weapon"] = item
                    print(f"Equipped {item['name']}")
                else:
                    # Use item (remove from inventory)
                    player["inventory"]["items"].pop(original_idx)
                    if item["name"] in "potion":
                        heal_amount = player["max_HP"] * item["heal"]
                        old_hp = player["HP"]
                        player["HP"] = min(player["HP"] + heal_amount, player["max_HP"])
                        print(
                            f"Used {item['name']} and restored {player['HP'] - old_hp:.1f} HP"
                        )
                    else:
                        print(f"Used {item['name']}")
                save_player(player)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")


def choose_class():
    """Player selects a class. Default inventory, equipment, and gold are assigned based on class."""
    classes = {
        "1": {
            "class": "Wizard",
            "HP": 20.0,
            "ATK": 6.0,
            "DEF": 4.0,
            "LVL": 1,
            "EXP": 0,
        },
        "2": {
            "class": "Swordsman",
            "HP": 25.0,
            "ATK": 5.0,
            "DEF": 6.0,
            "LVL": 1,
            "EXP": 0,
        },
        "3": {
            "class": "Ranger",
            "HP": 22.0,
            "ATK": 5.5,
            "DEF": 5.0,
            "LVL": 1,
            "EXP": 0,
        },
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
                "items": [
                    {
                        "name": "Small Potion",
                        "heal": 0.25,
                    },
                    {"name": "Health Potion", "heal": 0.5},
                ],
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
    locations = {"1": "Forest", "2": "Cave", "3": "Mountains", "4": "Swamp"}

    while True:
        print("\nWelcome to Spring Village!")
        print("What would you like to do?")
        console.print(table_menu)
        choice = input("Enter action input: ")
        
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
    """Randomly selects an enemy for the given area, including bosses if conditions are met."""
    # Regular enemies by area
    enemies = {
        "Forest": [
            {
                "name": "Diwata",
                "HP": 18.0,
                "ATK": 4.5,
                "DEF": 4.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Healing Herb", "type": "item"},
                    {"name": "Nature Staff", "type": "weapon", "ATK": 3.0},
                ],
            },
            {
                "name": "Kapri",
                "HP": 20.0,
                "ATK": 4.0,
                "DEF": 5.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Mystic Acorn", "type": "item"},
                    {"name": "Wooden Sword", "type": "weapon", "ATK": 2.5},
                ],
            },
            {
                "name": "Tikbalang",
                "HP": 22.0,
                "ATK": 5.5,
                "DEF": 3.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Lucky Feather", "type": "item"},
                    {"name": "Hoof Blade", "type": "weapon", "ATK": 3.5},
                ],
            },
        ],
        "Mountains": [
            {
                "name": "Mananggal",
                "HP": 25.0,
                "ATK": 5.0,
                "DEF": 4.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Bat Wing", "type": "item"},
                    {"name": "Cursed Dagger", "type": "weapon", "ATK": 4.0},
                ],
            },
            {
                "name": "Tyanak",
                "HP": 18.0,
                "ATK": 6.0,
                "DEF": 3.5,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Demonic Doll", "type": "item"},
                    {"name": "Tiny Blade", "type": "weapon", "ATK": 3.0},
                ],
            },
            {
                "name": "Tik-tik",
                "HP": 20.0,
                "ATK": 5.0,
                "DEF": 5.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Dark Essence", "type": "item"},
                    {"name": "Shadow Bow", "type": "weapon", "ATK": 3.5},
                ],
            },
        ],
        "Cave": [
            {
                "name": "Skeleton",
                "HP": 16.0,
                "ATK": 4.5,
                "DEF": 3.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Bone Fragment", "type": "item"},
                    {"name": "Ancient Sword", "type": "weapon", "ATK": 3.0},
                ],
            },
            {
                "name": "Cave Bat",
                "HP": 15.0,
                "ATK": 4.0,
                "DEF": 3.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Echo Crystal", "type": "item"},
                    {"name": "Sonic Blade", "type": "weapon", "ATK": 2.5},
                ],
            },
            {
                "name": "Goblin",
                "HP": 18.0,
                "ATK": 5.0,
                "DEF": 4.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Gold Nugget", "type": "item"},
                    {"name": "Goblin Sword", "type": "weapon", "ATK": 3.0},
                ],
            },
        ],
        "Swamp": [
            {
                "name": "Swamp Beast",
                "HP": 24.0,
                "ATK": 5.0,
                "DEF": 5.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Toxic Fang", "type": "item"},
                    {"name": "Poison Blade", "type": "weapon", "ATK": 4.0},
                ],
            },
            {
                "name": "Bog Creature",
                "HP": 20.0,
                "ATK": 4.5,
                "DEF": 4.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Cursed Gem", "type": "item"},
                    {"name": "Bog Staff", "type": "weapon", "ATK": 3.5},
                ],
            },
            {
                "name": "Mud Monster",
                "HP": 22.0,
                "ATK": 4.0,
                "DEF": 6.0,
                "EXP_DROP": 100,
                "DROPS": [
                    {"name": "Dark Shard", "type": "item"},
                    {"name": "Mud Hammer", "type": "weapon", "ATK": 3.0},
                ],
            },
        ],
    }

    # Bosses by area. Each boss includes a "trigger_kill_count" key to define when it should appear.
    bosses = {
        "Forest": [
            {
                "name": "Big Boss",
                "HP": 50.0,
                "ATK": 8.0,
                "DEF": 5.0,
                "EXP_DROP": 500,
                "DROPS": [
                    {"name": "Forest Boss Trophy", "type": "item"},
                ],
                "trigger_kill_count": 3,
            }
        ],
        "Mountains": [
            {
                "name": "Big Boss",
                "HP": 50.0,
                "ATK": 8.0,
                "DEF": 5.0,
                "EXP_DROP": 500,
                "DROPS": [
                    {"name": "Mountains Boss Trophy", "type": "item"},
                ],
                "trigger_kill_count": 3,
            }
        ],
        "Cave": [
            {
                "name": "Big Boss",
                "HP": 50.0,
                "ATK": 8.0,
                "DEF": 5.0,
                "EXP_DROP": 500,
                "DROPS": [
                    {"name": "Cave Boss Trophy", "type": "item"},
                ],
                "trigger_kill_count": 3,
            }
        ],
        "Swamp": [
            {
                "name": "Big Boss",
                "HP": 50.0,
                "ATK": 8.0,
                "DEF": 5.0,
                "EXP_DROP": 500,
                "DROPS": [
                    {"name": "Swamp Boss Trophy", "type": "item"},
                ],
                "trigger_kill_count": 3,
            }
        ],
    }

    # First, check if a boss should appear in this area.
    if area in bosses and bosses[area]:
        defeated_in_area = world_state["defeated_enemies"].get(area, [])
        # Build a list of boss names for easier checking (using lowercase for case-insensitivity)
        boss_names = [boss["name"].lower() for boss in bosses[area]]
        # Count defeated enemies that are NOT bosses.
        non_boss_defeated = [
            name for name in defeated_in_area if name.lower() not in boss_names
        ]
        boss_candidates = []

        for boss in bosses[area]:
            # Check if the boss hasn't been defeated and if the required kill count has been reached.
            if boss["name"] not in defeated_in_area and len(
                non_boss_defeated
            ) >= boss.get("trigger_kill_count", 3):
                boss_candidates.append(boss)

        if boss_candidates:
            boss = random.choice(boss_candidates)
            print(f"\nA mighty presence is felt... {boss['name']} appears!")
            print(
                f"Enemy Stats -> HP: {boss['HP']:.1f}, ATK: {boss['ATK']:.1f}, DEF: {boss['DEF']:.1f}"
            )
            # Reset the non-boss kill count by removing non-boss enemy names from the list.
            # This prevents the boss from re-triggering on subsequent encounters.
            return boss

    # If no boss is triggered, proceed with normal enemy encounters.
    if area in enemies:
        available_enemies = [
            enemy
            for enemy in enemies[area]
            if enemy["name"] not in world_state["defeated_enemies"].get(area, [])
        ]

        if not available_enemies:
            print(f"\nNo more enemies remain in the {area}!")
            return None

        enemy = random.choice(available_enemies)
        print(f"\nWhile in the {area}, you encounter a {enemy['name']}!")
        print(
            f"Enemy Stats -> HP: {enemy['HP']:.1f}, ATK: {enemy['ATK']:.1f}, DEF: {enemy['DEF']:.1f}"
        )
        return enemy
    else:
        print(f"\nThere are no enemies in the {area}.")
        return None


def display_battle_screen(player, enemy):
    """Display a Pokemon-style battle screen with ASCII art"""
    clear_terminal()
    print("\n" + "=" * 60)
    print(f"Your {player['class']:<30} Enemy {enemy['name']}")
    print(
        f"HP: {player['HP']:.1f}/{player['max_HP']:.1f}{' ' * 20}HP: {enemy['HP']:.1f}/{enemy['max_HP']:.1f}"
    )
    print("\n")

    # Check if the enemy has custom ASCII art already
    if "ascii_art" in enemy:
        print(enemy["ascii_art"])
    # If enemy is Diwata, use the custom ASCII art you provided
    elif enemy["name"].lower() == "diwata":
        print(rf"        {' ' * 20}         .==-.                .-==.   ")
        print(rf"        {' ' * 20}       //`^\\\_    (\_/)    _///^`\\  ")
        print(rf"        {' ' * 20}       //  ^  \\   (o.o)   //  ^  \\  ")
        print(rf"        {' ' * 20}      / | ^ ^ | \  (> <) / | ^ ^ | \  ")
        print(rf"   O    {' ' * 20}     /  |  ^  |  \      /  |  ^  |  \ ")
        print(rf"  /|\   {' ' * 20}        \  ^  /            \  ^  /    ")
        print(rf"  / \   {' ' * 20}         `---`              `---`     ")
    # Otherwise, show the default enemy art
    else:
        print(rf"   O    {' ' * 20}     /\___/\ ")
        print(rf"  /|\   {' ' * 20}    (  o o  )")
        print(rf"  / \   {' ' * 20}     >  ^  <")

    print("\n" + "=" * 60)


def display_attack_animation(attacker_name, defender_name, damage, is_player):
    """Display attack animation with ASCII art"""
    # Forward attack animation
    forward_animations = [
        ">>----->",
        " >>---->",
        "  >>--->",
        "   >>-->",
        "    >>->",
        "     >>>",
    ]

    # Backward attack animation
    backward_animations = [
        "<-----<<",
        "<----<< ",
        "<---<<  ",
        "<--<<   ",
        "<-<<    ",
        "<<<     ",
    ]

    animations = forward_animations if is_player else backward_animations

    for frame in animations:
        clear_terminal()
        print("\n" * 2)
        if is_player:
            print(" " * 10 + frame + " " * 20)  # Player attacks right to left
        else:
            print(" " * 20 + frame + " " * 10)  # Enemy attacks left to right
        print("\n" * 2)
        time.sleep(0.1)

    print(f"\n{attacker_name} deals {damage:.1f} damage to {defender_name}!")
    time.sleep(1)


def display_defend_animation(defender_name):
    """Display defend animation with ASCII art"""
    animations = ["╔═══╗", "║   ║", "╚═══╝"]

    clear_terminal()
    print("\n" * 2)
    for line in animations:
        print(" " * 20 + line)
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
            weapon_bonus = (
                player["equipped_weapon"]["ATK"]
                if player.get("equipped_weapon")
                else 0.0
            )
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

                drop = random.choice(enemy["DROPS"])
                if drop["type"] == "weapon":
                    player["inventory"]["weapons"].append(
                        {"name": drop["name"], "ATK": drop["ATK"]}
                    )
                    print(
                        f"\nThe enemy dropped a {drop['name']} (Weapon, ATK: {drop['ATK']})!"
                    )
                else:
                    player["inventory"]["items"].append({"name": drop["name"]})
                    print(f"\nThe enemy dropped a {drop['name']} (Item)!")

                add_experience(player, enemy["EXP_DROP"])

                save_world(world_state)
                save_player(player)
                time.sleep(2)
                break

            # Enemy counterattack (or boss action)
            if enemy["name"].lower() == "big boss":
                boss_action = random.choice(["attack", "heal"])
                if boss_action == "attack":
                    raw_damage, damage_reduction, final_damage, dice_roll = (
                        calculate_damage(enemy, player)
                    )
                    display_attack_animation(
                        enemy["name"], player["class"], final_damage, False
                    )
                    player["HP"] -= final_damage
                else:  # Heal action
                    heal_amount = enemy["max_HP"] * 0.2  # Boss heals 20% of max HP
                    old_hp = enemy["HP"]
                    enemy["HP"] = min(enemy["HP"] + heal_amount, enemy["max_HP"])
                    print(
                        f"\n{enemy['name']} uses Heal and recovers {enemy['HP'] - old_hp:.1f} HP!"
                    )
                    time.sleep(1)
            else:
                raw_damage, damage_reduction, final_damage, dice_roll = (
                    calculate_damage(enemy, player)
                )
                display_attack_animation(
                    enemy["name"], player["class"], final_damage, False
                )
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
            display_attack_animation(
                enemy["name"], player["class"], final_damage, False
            )
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
                raw_damage, damage_reduction, final_damage, dice_roll = (
                    calculate_damage(enemy, player)
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
      4. Open Inventory (without shop options)
    After defeating an enemy, the options reappear.
    """

    if world_state["defeated_enemies"] and world_state["defeated_enemies"].get(area):
        if len(world_state["defeated_enemies"][area]) == 4:
            print("Area is Closed!")
            print("You have already cleared this area!")
            time.sleep(3)
            return

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
                print(
                    f"\nYou sleep and restore {player['HP'] - old_hp:.1f} HP. Current HP: {player['HP']:.1f}"
                )
            elif choice == "3":
                print("\nYou return to Spring Village.")
                break
            elif choice == "4":
                # Outside the village, call open_inventory without shop options.
                open_inventory(player, in_village=False)
            else:
                print("Invalid choice. Please choose again.")


def add_experience(player, amount):
    player["EXP"] = player.get("EXP", 0) + amount
    player["LVL"] = player.get("LVL", 1)

    while True:
        exp_needed = player["LVL"] * 100

        if player["EXP"] >= exp_needed:
            player["LVL"] += 1
            player["EXP"] -= exp_needed
            exp_needed = player["LVL"] * 100

            # Stat increases on LVL up
            player["max_HP"] += 5.0
            player["HP"] = player["max_HP"]
            player["ATK"] += 1.0
            player["DEF"] += 1.0

            print(f"\nLevel Up! You are now level {player['LVL']}!")
            print("Stats increased:")
            print(f"HP: +5.0 (Now {player['max_HP']:.1f})")
            print(f"ATK: +1.0 (Now {player['ATK']:.1f})")
            print(f"DEF: +1.0 (Now {player['DEF']:.1f})\n")
        else:
            # Show remaining EXP needed when not leveling up
            print(f"EXP: {player['EXP']}/{exp_needed}")
            break

    save_player(player)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def show_intro_story():
    story = """
    In the mystical realm of Maharlika, nestled between ancient mountains and enchanted forests, 
    lies the peaceful Spring Village. For generations, it served as a sanctuary where humans and 
    magical creatures lived in harmony.

    But darkness has begun to stir. Strange occurrences plague the once-peaceful lands 
    surrounding Spring Village. The Diwata, usually benevolent forest spirits, have grown hostile. 
    Fearsome Kapre now terrorize travelers, and the dreaded Tikbalang roam the forests at night.

    As an adventurer drawn to Spring Village by tales of these disturbances, you've arrived at 
    a critical moment. The village elder speaks of an ancient evil awakening in the depths of 
    the nearby caves, its influence corrupting the magical creatures of the land.

    Armed with your chosen skills and the blessing of the village elder, you must investigate 
    the four regions surrounding Spring Village: the Enchanted Forest, the Shadow Cave, 
    the Mystic Mountains, and the Cursed Swamp.

    The fate of Spring Village now rests in your hands...
    """

    print("\n" + "=" * 80)
    print(story.strip())
    print("=" * 80 + "\n")
    input("Press Enter to begin your adventure...")


def main():
    print("Welcome to the Text-Adventure RPG!")

    # Choose player class and set up default inventory.
    player = load_player()
    if player is None:
        show_intro_story()
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
            if input("Start new game? (y/n): ").lower() == "y":
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
