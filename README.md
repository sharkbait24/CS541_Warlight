A basic setup for building and testing bots for the Warlight AI Challenge on www.theaigames.com.

Built with Python 3.6

# Warlight
The Warlight implementation on *theaigames* used by this program has all of its specifics on its site at: http://theaigames.com/competitions/warlight-ai-challenge.  It is recommended that you read the **Rules** and **Getting Started** pages before working with these bots.

# New Bots
New bots are made by creating a new class derived from Bot.  See randombot.py for an example.  There are 3 abstract functions in Bot that need to be implemented: (Note: all time limits are in milliseconds, and all arguments are in string format)
### pick_starting_regions(options)
Options is a list of strings where option[0] is time limit for response, and the remaining are region ids to select from.  The bot must return a string of 6 region ids from options, space delimited.
### place_armies(time)
Time is the time limit.  The bot must return a string of army placements using up the **available_armies** in the Bot class that is populated each turn by the server.  Any armies not placed are lost, so always place all of them.  A helper function **PlaceArmyBuilder** in the *bot.py* file can be used to make the output generation easy.
### attack_transfer(time)
Time is the time limit.  The bot returns a string of army movements (transfer between owned regions or attack if going into region owned by another).  The same string is used for both attack and transfer moves, as the server is responsible for determining which is appropriate.  It is ok to choose to do nothing on a turn, in which case you should send 'No moves' to the server.  Additional restrictions on movement, and how attacking is calculated, can be found on the *theaigames* site.  

A helper function **AttackTransferBuilder** in the *bot.py* file can be used for output generation.  If you create a new instance of AttackTransferBuilder each time, you can call *to_string* without adding any moves to properly output 'No moves'.
### Map.last_update[]
The *Map.last_update* for the bot contains a list of all map updates supplied by the server at the start of the turn.  This represents the "visible" map for the bot and contains all regions the bot owns, plus adjacent regions (neighbors) and any regions the bot lost last turn.  In general this should be used over the *Map.regions* for looking at the whole map, since Map.regions is a dictionary and not easily iterated over.
### Adding Your Bot
To make your bot easily usable by everyone else, and testable, you need to import your new bot class in **ailist.py** and also create a new dictionary entry for the class in the *AiList* class.  This will allow you to select the bot in the *BotTester*.

Since *ailist.py* in imported in *warlight_player.py* you can easily set your new bot class to be used on *theaigames* site.

# New Map Weights
This and heuristics are a bit experimental and it is hard to say if they will actually be useful, but that's what a college project is for.

All weights are in the **map_weights.py** file.  A *UniformWeights* map weight is supplied giving all regions and super regions a weight of 1.  Mappings for region and super region ids to names can be found in **RegionMap** and **SuperRegionMap** classes in *map.py*.  New weights can simply be a duplicate class with different values.
### Adding Your Weight
Add your new weight class to the **WeightList** class dictionary in *map_weights.py*.  This will allow your weight to be tested in the *BotTester*.  **Note**: There are currently no tests specific to weights, so they will need to be paired with a bot that uses them.

# New Heuristics
Due to the significant hidden information in this game, heuristics will likely be difficult to create.  

All heuristics are in the **heuristics.py** file.  A *RegionsNotCaptured* heuristic is supplied which returns the number of regions not owned by the player.
### Heuristic base class and evaluate(bot)
New heuristics should be derived from the *Heuristic* class, which includes an abstract function **evaluate(bot)** which needs to be implemented.  Since the entire *Bot* base class is given to the function, it can look at all of the bot's data, including name, map, and map weights.

The heuristic should return a number from its *evaluate* function, where lower is considered better.
### Add Your Heuristic
Add your heuristic to the **HeuristicList** class dictionary in *heuristics.py*.  This will allow your heuristic to be tested in the *BotTester*.

# Local Testing
### BotTester
The *BotTester* class in the **bot_tests.py** file can be executed locally to perform offline tests against a bot, weight, and heuristic combo.  Running the *bot_tests.py* file will give a prompt to choose the bot, weight and heuristic from a list of options contained in their respective dictionaries (*AiList*, *WeightList*, *HeuristicList*).

Then you are given a choice of all available tests from the *TestList* in **testlist.py**.
### PickStartingTest 
Gives a default selection of region ids to the bot and outputs the 6 it chooses.  Tests:
* pick_starting_regions()
### StandardTurnTest
Gives a default map update, opponent moves and starting armies to the bot.  Asks for army placement and attack/transfer moves, and prints results. Tests:
* place_armies()
* attack_transfer()
### HeuristicTest
Gives a default map update, opponent moves and starting armies to the bot.  Asks for heuristic evaluation and prints result.  Tests:
* bot.heuristic.evaluate()
### Adding Tests
A new test can be added to the list, by creating a new class that derives from Test, and implements the abstract function **test(tester)**.  The *BotTester* is given to the function to make accessing the bot, weights, heuristic, region map and super region map easy.  There are also several helper print functions in the **Print** class in *testlist.py*.

New test classes need to be added to the **TestList** class dictionary to be callable from *BotTester*.
# Warlight AI Challenge
To run this bot you need to zip all of the .py files (**except** *testlist.py* and *bot_tests.py*) and upload the zip to *theaigames* site.  Be sure to modify your local copy of *warlight_player.py* to use the bot, weight and heuristic you want.

# Support Functions
Some additional helper functions that can be helpful for working with this program.
### Do/Undo Map Changes
The *Map* class includes functions to perform temporary changes on itself:
* do_temp_update(from_region, from_qty, to_region, to_qty, to_region_owner)
* undo_last_temp_update()
* undo_all_temp_updates()

These changes **do** modify the map, so make sure you undo all of them before leaving your function or you may see unexpected behavior.
### split_last_update(player)
In the *Map* class, this function can be used to partition the map update recieved for the start of this turn into *player_owned*, *neighbor_regions*, and *other* lists.  This can make working with the "visible" map easier.  Note: the *other* lists will be populated if you lost a region last turn that had no neighbors (or lost multiple adjacent regions).
### const.py
Not a function, but constants for command and names and starting values used by *theaigames* site are supplied in here.  Use these as much as possible, instead of hardcoding values, to make bugs less likely.

# Final Notes
### opponent_moves
*theaigames* server supplies the opponent's moves for the last turn to you, which are parsed in the *Map* class and placed into **opponent_place_armies** and **opponent_attack_moves** (also contains transfer moves).  Those moves only need to be used if your ai makes decisions based on them, as the *Map.last_update* already has the results of those moves in it.
