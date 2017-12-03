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
        region_index = 0
        troops_remaining = self.available_armies
        owned_regions = self.map.get_owned_regions(self.name)  # returns a copy of references to owned regions
        owned , neighbors, outliers = self.map.split_last_update(self.name) 
        """for i in neighbors:
            print(i.id)"""
            
       
        regions = []
        if self.turn_elapsed == 1:
            owned = Sorter.sorting(owned, self, True)
            best = owned[0]
            placements.add(best.id, troops_remaining)
            troops_remaining = 0
        else:
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
                troops_remaining = 0;

        self.turn_elapsed = self.turn_elapsed + 1
        return placements.to_string()

    # Currently checks whether a region has more than six troops placed to attack,
    # or transfers if more than 1 unit is available.
    def attack_transfer(self, time_limit):
        attack_transfers = AttackTransferBuilder(self.name)
        owned_regions = self.map.get_owned_regions(self.name)
        for region in owned_regions:
            #print('checking region')
            neighbors = [region for region in region.neighbors]   # make a copy of references to neighbor regions
            while len(neighbors) > 1:
                #print('checking neighbors')
                target_region = neighbors[MyRandom.randrange(0, len(neighbors))] 
                #below is the case for neighboring enemy regions.
                if region.owner != target_region.owner and region.troop_count - target_region.troop_count >= 2 :
                    attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                    region.troop_count = 1
                
                #below is for regions that we own.
                elif region.owner == target_region.owner and target_region.troop_count > 1:
                    region_enemy_count = 0
                    target_enemy_count = 0
                    for adjacent in target_region.neighbors :
                        if adjacent.owner != region.owner :
                            target_enemy_count += 1
                    for target_adjacent in region.neighbors :
                        if target_adjacent.owner != region.owner :
                            region_enemy_count += 1
                    
                    if region_enemy_count == 0 and target_enemy_count == 0 :
                        attack_transfers.add(target_region.id, region.id, target_region.troop_count - 1)
                        target_region.troop_count = 1
                    
                    elif target_enemy_count == 0 and target_region.troop_count > 1:
                        attack_transfers.add(target_region.id, region.id, target_region.troop_count - 1)
                        target_region.troop_count = 1

                    elif region_enemy_count == 0 and region.troop_count > 1 and target_enemy_count > 0 :
                        attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                        region.troop_count = 1
                    
                neighbors.remove(target_region)
        return attack_transfers.to_string()


                

