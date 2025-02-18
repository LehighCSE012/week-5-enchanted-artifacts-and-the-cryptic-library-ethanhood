"""This is the week 4 coding assigment"""
import random
def display_player_status(player_stats):
    """This method displays the player status"""
    print("Your current health: " + str(player_stats["health"]))

def handle_path_choice(player_stats):
    """This method handles the path choice"""
    choice=random.choice(["left", "right"])
    if choice=="right":
        print("You fall into a pit and lose 15 health points.")
        player_stats["health"] = player_stats["health"]-15
        if player_stats["health"] < 0:
            player_stats["health"]=0
            print("You are barely alive!")
    else:
        print("You encounter a friendly gnome who heals you for 10 health points")
        if player_stats["health"]<= 90:
            player_stats["health"]=player_stats["health"]+10
    
    return player_stats

def player_attack(monster_health):
    """This method deals with the monsters health when a
    player makes an attack"""
    print("You strike the monster for 15 damage!")
    monster_health = monster_health-15
    updated_monster_health = monster_health
    return updated_monster_health

def monster_attack(player_stats):
    """This method deals with the players health when a
    monster makes an attack"""
    critical = random.random()
    if critical<=.5:
        player_stats["health"] = player_stats["health"]-20
        print("The monster lands a critical hit for 20 damage!")
    else:
        player_stats["health"] = player_stats["health"]-10
        print("The monster hits you for 10 damage!")
    
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """This method deals with the combat
    by calling the attack functions"""
    while 1:
        if player_stats['health']<=0:
            print("Game Over")
            treasure_found_and_won = False
            break
        if monster_health<=0:
            print("You defeated the monster!")
            treasure_found_and_won = has_treasure
            break
        monster_health = player_attack(monster_health)
        display_player_status(player_stats)
        player_stats = monster_attack(player_stats)


    return treasure_found_and_won # boolean

def check_for_treasure(has_treasure):
    """This method checks for treasure"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory, item):
    """This method adds item to inventory"""
    # Using append to add to the end of the list the new item
    inventory.append(item)
    print("You acquired a " + str(item) + "!")
    return inventory

def display_inventory(inventory):
    """This method displays items in inventory"""
    i = 1
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        # Using a for in statement to parse through the inventory
        for item in inventory:
            print(str(i) + ". " + str(item))
            i=i+1

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Using room for this for and in statement to parse through
    each room which is a tuple in the list"""
    smart = False
    for room in dungeon_rooms:
        print("You enter the " + room[0])
        if room[0]=="Cryptic Library":
            possible_clues = {
                "The treasure is buried beneath the old oak tree.",
                "Only the wise owl knows the path through the labyrinth.",
                "The ancient runes reveal the password to the sealed gate.",
                "A candle in the dark will show the hidden passage."
            }
            random_clues = random.sample(list(possible_clues), 2)
            clues.add(random_clues)
            artifact_name = "staff_of_wisdom"
            if artifact_name in inventory:
                smart = True
                print("The Staff of Wisdom hums in your hand")
        if room[1] != "None":
            #Using this to test tuple for first room
            test=0
            while test==0:
                new_item = "lock"
                #room[1] = new_item <- get an error if this code is uncommented
                print("Could not change " + str(room[1]) + " to " + new_item + ".")
                test = test+1
            #End of test
            print("You found a " + str(room[1]) + " in the room.")
            inventory = acquire_item(inventory, room[1])
        match room[2]:
            case "puzzle":
                print("You encounter a puzzle!")
                choice = input("Would you like to solve or skip the puzzle?\n")
                if choice=="solve":
                    result = random.choice([True, False])
                    if result:
                        print(room[3][0])
                        player_stats["health"] = player_stats["health"] + int(room[3][2])
                    else:
                        print(room[3][1])
                        player_stats["health"] = player_stats["health"] + int(room[3][2])
                        display_player_status(player_stats)
                else:
                    if smart:
                        print("The player used their knowledge to bypass the challenge")
                        smart = False
                    else:
                        print("You can't bypass without staff")
            case "trap":
                print("You see a potential trap!")
                choice = input("Would you like to disarm or bypass the trap?\n")
                if choice=="disarm":
                    # True is success and False is failure
                    result = random.choice([True, False])
                    if result:
                        print(room[3][0])
                        player_stats["health"] = player_stats["health"] + int(room[3][2])
                    else:
                        print(room[3][1])
                        player_stats["health"] = player_stats["health"] + int(room[3][2])
                        display_player_status(player_stats)
                else:
                    print("Really? Okay fine, be boring...")
            case "none":
                print("There doesn't seem to be a challenge in this room. You move on.")
        if player_stats["health"] <= 0:
            player_stats["health"]=0
            print("You are barely alive!")
        display_inventory(inventory)

    display_player_status(player_stats)
    return player_stats, inventory, clues

def discover_artifact(player_stats, artifacts, artifact_name, inventory):
    if artifact_name in artifacts:
            artifact = artifacts[artifact_name]
            print("You have found " + str(artifact["description"]))
            inventory = acquire_item(inventory, artifact)
            if(artifact["effect"] == "increases health"):
                player_stats["health"] = player_stats["health"] + int(artifact["power"])
            if(artifact["effect"] == "enhances attack"):
                player_stats["attack"] = player_stats["attack"] + int(artifact["power"])
            print("The artifact's power helps " + str(artifact["effect"]))
            del artifacts[artifact_name]
    else:
        print("You found nothing of interest. Just a " + artifact_name)
    
    return player_stats, artifacts

def find_clue(clues, new_clue):
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print("You discovered a new clue: " + str(new_clue))
    
    return clues

def main():

    """Main game loop."""

    dungeon_rooms = [

    ("Dusty library", "key", "puzzle",

     ("Solved puzzle!", "Puzzle unsolved.", -5)),

    ("Narrow passage, creaky floor", "torch", "trap",

     ("Avoided trap!", "Triggered trap!", -10)),

    ("Grand hall, shimmering pool", "healing potion", "none", None),

    ("Small room, locked chest", "treasure", "puzzle",

     ("Cracked code!", "Chest locked.", -5)),

    ("Cryptic Library", None, "library", None)

    ]

    player_stats = {
            'health': 100, 
            'attack': 5}

    monster_health = 70

    inventory = []

    clues = set()

    artifacts = {

        "amulet_of_vitality": {

            "description": "Glowing amulet, life force.",

            "power": 15,

            "effect": "increases health"

        },

        "ring_of_strength": {

            "description": "Powerful ring, attack boost.",

            "power": 10,

            "effect": "enhances attack"

        },

        "staff_of_wisdom": {

            "description": "Staff of wisdom, ancient.",

            "power": 5,

            "effect": "solves puzzles"

        }

    }

    has_treasure = random.choice([True, False])



    display_player_status(player_stats)

    player_stats = handle_path_choice(player_stats)



    if player_stats['health'] > 0:

        treasure_obtained_in_combat = combat_encounter(

            player_stats, monster_health, has_treasure)

        if treasure_obtained_in_combat is not None:

            check_for_treasure(treasure_obtained_in_combat)



        if random.random() < 0.3:

            artifact_keys = list(artifacts.keys())

            if artifact_keys:

                artifact_name = random.choice(artifact_keys)

                player_stats, artifacts = discover_artifact(

                    player_stats, artifacts, artifact_name, inventory)

                display_player_status(player_stats)



        if player_stats['health'] > 0:

            player_stats, inventory, clues = enter_dungeon(

                player_stats, inventory, dungeon_rooms, clues, artifacts)

            print("\n--- Game End ---")

            display_player_status(player_stats)

            print("Final Inventory:")

            display_inventory(inventory)

            print("Clues:")

            if clues:

                for clue in clues:

                    print(f"- {clue}")

            else:

                print("No clues.")

if __name__ == "__main__":
    main()
