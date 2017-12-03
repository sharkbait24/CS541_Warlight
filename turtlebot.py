# ---------------------------------------------------------------------#
# Warlight AI Challenge - Starter Bot                                  #
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

from map import Map
from bot import Bot, PlaceArmyBuilder, AttackTransferBuilder, PickStartingBuilder
from const import PLACE_ARMIES, ATTACK_TRANSFER, NO_MOVES
from math import fmod, pi
from time import clock
from regionsorter import Sorter


# TurtleBot decides to attack enemy positions over spreading army out to nutrual
# territory
class TurtleBot(Bot):
    def __init__(self, map_weights, heuristic):
        super(TurtleBot, self).__init__(map_weights, heuristic)

    # Choose a random 6 regions from the ones supplied
    # options[0] is time limit
    ''' THIS SHOULD BE MODIFIED TO PICK OUT OF THE BOTTLE NECKED REGIONS 
        WE WILL USE options PROVIDED BY SERVER AND EVALUATE WHICH 
        PriorityWeights ARE = 0 MEANING THE LOCATION IS A BOTTLENECK(DESIRABLE)
        LOCATION FOR PLACING TROOPS '''
    
    def pick_starting_regions(self, options):
        option = self.parse_pick_starting_regions(options)
        ordered_regions = Sorter.sorting(option, self, False) # false means ascending order
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
        owned, neighbors, outliers = self.map.split_last_update(self.name)
        
        in_super = set()
        
        for region in owned:
            in_super.add(region.super_region)
        
        in_super = list(in_super)
        
        new_in_super = [(x,len(x.regions) - len(Map.get_owned_in_list(x.regions, self.name))) for x in in_super]

        shuffled_regions = MyRandom.shuffle(owned_regions)
        
        new_in_super.sort(key=lambda super_region: super_region[1] )
        


        while troops_remaining:

            if self.turn_elapsed == 1:
                owned = Sorter.sorting(owned, self, False)
                best = owned[0]
                placements.add(best.id, troops_remaining)
                troops_remaining = 0

            else:
                
                for x in new_in_super:
                    if x[1] != 0:
                        for y in x[0].regions:
                            if y.owner != self.name:
                                owned_neighbors = Map.get_owned_in_list(y.neighbors, self.name)
                                for z in owned_neighbors:
                                    if troops_remaining > 0:
                                        placements.add(z.id, 1)
                                        troops_remaining -= 1
                
        self.turn_elapsed = self.turn_elapsed + 1
        return placements.to_string()

    # Currently checks whether a region has more than six troops placed to attack,
    # or transfers if more than 1 unit is available.
    def attack_transfer(self, time_limit):
        attack_transfers = AttackTransferBuilder(self.name)
        owned_regions = self.map.get_owned_regions(self.name)
        for region in owned_regions:
            neighbors = [region for region in region.neighbors]  # make a copy of references to neighbor regions
            while len(neighbors) > 1:
                target_region = neighbors[MyRandom.randrange(0, len(neighbors))]
                if region.owner != target_region.owner and region.troop_count > 6:
                    attack_transfers.add(region.id, target_region.id, 5)
                    region.troop_count -= 5
                elif region.owner == target_region.owner and region.troop_count > 1:
                    attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                    region.troop_count = 1
                else:
                    neighbors.remove(target_region)
        return attack_transfers.to_string()



class MyRandom(object):
    @staticmethod
    def randrange(r_min, r_max):
        # A pseudo random number generator to replace random.randrange
        #
        # Works with an inclusive left bound and exclusive right bound.
        # E.g. Random.randrange(0, 5) in [0, 1, 2, 3, 4] is always true
        return r_min + int(fmod(pow(clock() + pi, 2), 1.0) * (r_max - r_min))

    @staticmethod
    def shuffle(items):
        # Method to shuffle a list of items
        i = len(items)
        while i > 1:
            i -= 1
            j = MyRandom.randrange(0, i)
            items[j], items[i] = items[i], items[j]
        return items

