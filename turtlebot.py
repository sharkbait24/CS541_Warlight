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
from randombot import MyRandom
from bot import Bot, PlaceArmyBuilder, AttackTransferBuilder, PickStartingBuilder
from const import PLACE_ARMIES, ATTACK_TRANSFER, NO_MOVES
from regionsorter import Sorter


# TurtleBot decides to attack enemy positions over spreading army out to nutrual
# territory
class TurtleBot(Bot):
    def __init__(self, map_weights, heuristic):
        super(TurtleBot, self).__init__(map_weights, heuristic)

    # Choose a  the region with lowest adjacent regions to start
    # options[0] is time limit
    def pick_starting_regions(self, options):
        option = self.parse_pick_starting_regions(options)
        ordered_regions = Sorter.sorting(option, self, False) # false means ascending order
        builder = PickStartingBuilder()
        builder.add_all(ordered_regions[:6])
        return builder.to_string()

    # Places up to 2 armies on random regions
    def place_armies(self, time_limit):
        placements = PlaceArmyBuilder(self.name)
        troops_remaining = self.available_armies
        owned, neighbors, outliers = self.map.split_last_update(self.name)
        
        super_set = set()
        for region in owned:
            super_set.add(region.super_region)

        super_set = list(super_set)
        super_list = []
        for x in super_set:
            x_owned = len(x.regions)-len(Map.get_owned_in_list(x.regions, self.name))
            super_list.append((x, x_owned))
        super_list.sort(key=lambda super_region: super_region[1])

        if self.turn_elapsed == 1:
            owned = Sorter.sorting(owned, self, False)
            best = owned[0]
            placements.add(best.id, troops_remaining)
            troops_remaining = 0

        while troops_remaining:
            for x in super_list:
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

