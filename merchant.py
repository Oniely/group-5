# The buying function, now part of the merchant module.
def buy_item(player):
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


# The selling function, now part of the merchant module.
def sell_item(player):
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


# A simple chatbot conversation function for the merchant.
def merchant_chat():
    print("\nMerchant Chat - type 'exit' to end chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Merchant: Very well, let me know if you need anything else.")
            break
        if "job" in user_input.lower():
            print(
                "Merchant: I am a humble merchant, always seeking to trade goods with adventurers like you!"
            )
        elif "name" in user_input.lower():
            print(
                "Merchant: I go by Merchant, though some call me your friend in these parts."
            )
        elif "hello" in user_input.lower() or "hi" in user_input.lower():
            print("Merchant: Hello! How can I help you today?")
        elif "gold" in user_input.lower():
            print("Merchant: Gold is the coin of the realm – use it wisely!")
        else:
            print("Merchant: Hmm, interesting...")


# The main function to talk to the Merchant.
def talk_to_merchant(player):
    print("\n--- Merchant ---")
    print("Merchant: Greetings, traveler! Welcome to my humble shop.")
    while True:
        print("\nWhat would you like to do?")
        print("1. Buy items")
        print("2. Sell items")
        print("3. Chat")
        print("4. Exit conversation")
        choice = input("Enter your choice: ")
        if choice == "1":
            buy_item(player)
        elif choice == "2":
            sell_item(player)
        elif choice == "3":
            merchant_chat()
        elif choice == "4":
            print("Merchant: Farewell, and safe travels!")
            break
        else:
            print("Merchant: I don't understand. Please choose a valid option.")
