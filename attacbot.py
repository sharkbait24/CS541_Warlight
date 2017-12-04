# ---------------------------------------------------------------------#
# Warlight AI Challenge - Attack Bot                                   #
# ============                                                         #
#                                                                      #
# Last update: 20 Mar, 2014                                            #
#                                                                      #
# @author Jackie <jackie@starapple.nl>                                 #
# @version 1.0                                                         #
# @license MIT License (http://opensource.org/licenses/MIT)            #
# ---------------------------------------------------------------------#

# Modified by Joe Coleman
#
# Original code has been modified for our CS 541 project to
# work with our modified map and split from the bot class to
# provide a convenient way for us to create new AIs

from randombot import MyRandom
from regionsorter import Sorter
from bot import Bot, PlaceArmyBuilder, AttackTransferBuilder, PickStartingBuilder
from const import PLACE_ARMIES, ATTACK_TRANSFER, NO_MOVES
from math import fmod, pi
from time import clock
from map import Map

# AttacBot decides to attack enemy positions over spreading army out to neutral
# territory 
class AttacBot(Bot):

    def __init__(self, map_weights, heuristic):
        super(AttacBot, self).__init__(map_weights, heuristic)


    # Choose a random 6 regions from the ones supplied
    # options[0] is time limit
    ''' THIS SHOULD BE MODIFIED TO PICK OUT OF THE BOTTLE NECKED REGIONS 
        WE WILL USE options PROVIDED BY SERVER AND EVALUATE WHICH 
        LOCATION FOR PLACING TROOPS '''
    def pick_starting_regions(self, options):
        option = self.parse_pick_starting_regions(options)
        ordered_regions = Sorter.sorting(option, self, True)
        builder = PickStartingBuilder()
        builder.add_all(ordered_regions[:6])
        return builder.to_string()

    # Places up to 2 armies on random regions
    ''' REPLACE SHUFFLED_REGIONS WITH TUPLE FOR split_last_update WHICH SPLITS 
        THE LIST OF REGIONS INTO player_owned , neighbors , outliers ''' 
    def place_armies(self, time_limit):
        placements = PlaceArmyBuilder(self.name)
        troops_remaining = self.available_armies
        owned , neighbors, outliers = self.map.split_last_update(self.name) 

        if self.turn_elapsed == 1:
            owned = Sorter.sorting(owned, self, True)
            best = owned[0]
            placements.add(best.id, troops_remaining)
            troops_remaining = 0
        else:
            regions = []
            vulnerable = {}
            for i in neighbors :
                regions.extend(Map.get_owned_in_list(i.neighbors, self.name))

            for region in regions:
                if region in vulnerable :
                    vulnerable[region] = vulnerable.get(region) + 1
                else:
                    vulnerable[region] = 1

            vuln = [[key, value] for key, value in vulnerable.items()]
            vuln.sort(key=lambda region: region[1], reverse=True)
            ordered_vuln = []
            for region in vuln :
                ordered_vuln.append(region[0])

            index = 0
            length = len(ordered_vuln)
            while troops_remaining and index < length:     
                region = ordered_vuln[index]
                if troops_remaining > 1:
                    placements.add(region.id, 2)
                    region.troop_count += 2
                    troops_remaining -= 2
                else:
                    placements.add(region.id, 1)
                    region.troop_count += 1
                    troops_remaining -= 1
                index += 1

            if troops_remaining > 0 :
                placements.add(ordered_vuln[0].id, troops_remaining)
                ordered_vuln[0].troops_remaining += troops_remaining
                troops_remaining = 0;

        self.turn_elapsed = self.turn_elapsed + 1
        return placements.to_string()

    # Currently checks whether a region has more than six troops placed to attack,
    # or transfers if more than 1 unit is available.
    def attack_transfer(self, time_limit):
        attack_transfers = AttackTransferBuilder(self.name)
        owned_regions = self.map.get_owned_regions(self.name)

        num_enemies = dict()
        for region in owned_regions:
            enemies = 0
            for neighbor in region.neighbors:
                if self.name != neighbor.owner:
                    enemies += 1
            num_enemies[region.id] = enemies

        prioritize = []
        # Setting up priority values for attacking unowned regions
        for region in owned_regions:
            for neighbor in region.neighbors:
                if neighbor.owner != self.name:
                    # if neighbor.owner in self.opponents:
                    edges = len(neighbor.neighbors)
                    priority = edges * ((region.troop_count - 1) / neighbor.troop_count)
                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": region.troop_count - 1,
                        "priority": priority,
                    })

                    no_attack = edges
                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": 0,
                        "priority": no_attack,
                    })
                else:
                    edges = len(neighbor.neighbors)
                    if num_enemies[region.id] == 0:
                        priority = edges * 10
                    else:
                        priority = edges * (num_enemies[neighbor.id] / num_enemies[region.id])

                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": region.troop_count - 1,
                        "priority": priority,
                    })

                    no_attack = edges
                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": 0,
                        "priority": no_attack,
                    })

        prioritize.sort(key=lambda to_move: to_move["priority"], reverse=True)

        for move in prioritize:
            if move["region"].troop_count > 1:
                if move["troops"] > 1:
                    attack_transfers.add(move["region"].id, move["neighbor"].id, move["troops"])
                move["region"].troop_count = 1

        return attack_transfers.to_string()

        """
        for region in owned_regions:
            neighbors = [neighbor for neighbor in region.neighbors]   # make a copy of references to neighbor regions
            length = len(neighbors)
            index = 0
            done = False
            while index < length and not done:
                target_region = neighbors[index]
                if self.name != target_region.owner:
                    if (region.troop_count - target_region.troop_count) > 1:
                        attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                        region.troop_count = 1
                        done = True
                # below is for regions that we own.
                elif region.troop_count > 1:
                    region_enemy_count = 0
                    target_enemy_count = 0
                    for adjacent in target_region.neighbors:
                        if adjacent.owner != region.owner:
                            target_enemy_count += 1
                    for target_adjacent in region.neighbors:
                        if target_adjacent.owner != region.owner:
                            region_enemy_count += 1

                    if region_enemy_count < target_enemy_count:
                        attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                        region.troop_count = 1
                        done = True
                    else :
                        two = 1 + 1
                index += 1

        return attack_transfers.to_string()
        """



"""elif region_enemy_count > 0 and region.troop_count > 1:
                        attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                        region.troop_count  = 1
                        #target_region.troop_count = 1
                        #print('transferring to frontier')

                    elif region_enemy_count == 0 and region.troop_count > 1 and target_enemy_count > 0 :
                        attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                        region.troop_count = 1
                        #print('transfering to frontier')"""

