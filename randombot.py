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

from bot import Bot, PlaceArmyBuilder, AttackTransferBuilder
from random import Random


# RandomBot as the name implies does everything by choosing randomly
class RandomBot(Bot):
    def __init__(self, map_weights, heuristic):
        super(RandomBot, self).__init__(map_weights, heuristic)
        self.rand = MyRandom()

    # Choose a random 6 regions from the ones supplied
    # options[0] is time limit
    def pick_starting_regions(self, options):
        options = options[1:]
        shuffled_regions = self.rand.shuffle(options)
        return ' '.join(shuffled_regions[:6])

    # Places up to 2 armies on random regions
    def place_armies(self, time_limit):
        placements = PlaceArmyBuilder(self.name)
        region_index = 0
        troops_remaining = self.available_armies
        owned_regions = self.map.get_owned_regions(self.name)  # returns a copy of references to owned regions
        shuffled_regions = self.rand.shuffle(owned_regions)

        while troops_remaining:
            region = shuffled_regions[region_index]
            if troops_remaining > 1:
                placements.add(region.id, 2)
                region.troop_count += 2
                troops_remaining -= 2
            else:
                placements.add(region.id, 1)
                region.troop_count += 1
                troops_remaining -= 1
            region_index += 1
        return placements.to_string()

    # Currently checks whether a region has more than six troops placed to attack,
    # or transfers if more than 1 unit is available.
    def attack_transfer(self, time_limit):
        attack_transfers = AttackTransferBuilder(self.name)
        owned_regions = self.map.get_owned_regions(self.name)
        for region in owned_regions:
            neighbors = [neighbor for neighbor in region.neighbors]   # make a copy of references to neighbor regions
            while len(neighbors) > 1:
                target_region = neighbors[self.rand.randrange(0, len(neighbors))]
                if region.owner != target_region.owner and region.troop_count > 6:
                    attack_transfers.add(region.id, target_region.id, 5)
                    region.troop_count -= 5
                elif region.owner == target_region.owner and region.troop_count > 1:
                    attack_transfers.add(region.id, target_region.id, region.troop_count - 1)
                    region.troop_count = 1
                else:
                    neighbors.remove(target_region)
        return attack_transfers.to_string()

    @staticmethod
    def print_ids(regions):
        print([region.id for region in regions])


class MyRandom(object):
    def __init__(self):
        self.random = Random()
        self.random.seed()

    def randrange(self, r_min, r_max):
        return self.random.randint(r_min, r_max-1)

    def shuffle(self, items):
        # Method to shuffle a list of items
        i = len(items)
        while i > 1:
            i -= 1
            j = self.randrange(0, i)
            items[j], items[i] = items[i], items[j]
        return items
