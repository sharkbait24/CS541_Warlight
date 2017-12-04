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

from bot import Bot, PlaceArmyBuilder, AttackTransferBuilder, PickStartingBuilder
from map import Map
from math import factorial
from regionsorter import Sorter


# TurtleBot decides to attack enemy positions over spreading army out to nutrual
# territory
class TurtleBot(Bot):
    def __init__(self, map_weights, heuristic):
        super(TurtleBot, self).__init__(map_weights, heuristic)

    # Choose the region with lowest adjacent regions to start
    # options[0] is time limit
    def pick_starting_regions(self, options):
        option = self.parse_pick_starting_regions(options)
        ordered_regions = Sorter.sorting(option, self, False) # false means ascending order
        builder = PickStartingBuilder()
        builder.add_all(ordered_regions[:6])
        return builder.to_string()

    # Places armies by prioritizing regions next to unowned regions, in super regions turtlebot controls.
    def place_armies(self, time_limit):
        placements = PlaceArmyBuilder(self.name)
        troops_remaining = self.available_armies
        owned, neighbors, outliers = self.map.split_last_update(self.name)
        
        super_set = set()
        for region in owned:
            super_set.add(region.super_region)

        super_set = list(super_set)
        super_list = list()
        for x in super_set:
            unowned = len(x.regions) - len(Map.get_owned_in_list(x.regions, self.name))
            super_list.append((x, unowned))
        super_list.sort(key=lambda super_region: super_region[1])

        if self.turn_elapsed == 1:
            owned = Sorter.sorting(owned, self, False)
            best = owned[0]
            placements.add(best.id, troops_remaining)
            troops_remaining = 0

        while troops_remaining:
            for x in super_list:
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

        super_region = dict()
        for key, value in self.map.super_regions.items():
            unowned = len(value.regions) - len(Map.get_owned_in_list(value.regions, self.name))
            super_region[value.id] = unowned

        in_danger = dict()
        prioritize = []
        # Setting up priority values for attacking unowned regions
        for region in owned_regions:
            edge_weight = len(region.neighbors)
            unowned = super_region[region.super_region.id]
            for neighbor in region.neighbors:
                if neighbor.owner != self.name:
                    # if neighbor.owner in self.opponents:
                    danger = unowned * edge_weight * (1 - capture_chance(neighbor, region))
                    in_danger[region.id] = in_danger.get(region.id, 1) * danger

                    edges = len(neighbor.neighbors)
                    not_own = super_region[neighbor.super_region.id]
                    priority = not_own * edges * (1 - capture_chance(region, neighbor))
                    if neighbor.is_on_super_region_border:
                        priority = priority * 0.5
                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": region.troop_count - 1,
                        "priority": priority,
                    })

                    no_attack = not_own * edges * 0.5
                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": 0,
                        "priority": no_attack,
                    })

        # Setting priority values for transferring to an owned region
        for region in owned_regions:
            for neighbor in region.neighbors:
                if neighbor.owner == self.name:
                    edge_weight = len(neighbor.neighbors)
                    unowned = super_region[neighbor.super_region.id]
                    priority = 2 * unowned * edge_weight * in_danger.get(neighbor.id, 10)
                    if unowned == 0:
                        priority = 10 * edge_weight * in_danger.get(neighbor.id, 10)
                    prioritize.append({
                        "region": region,
                        "neighbor": neighbor,
                        "troops": region.troop_count - 1,
                        "priority": priority,
                    })
        prioritize.sort(key=lambda to_move: to_move["priority"])

        for move in prioritize:
            if move["region"].troop_count > 1:
                if move["troops"] > 1:
                    attack_transfers.add(move["region"].id, move["neighbor"].id, move["troops"])
                move["region"].troop_count = 1

        return attack_transfers.to_string()


# Calculates the cdf for each army destroying AT MOST each enemy army.
# (1 - capture_chance) gives probability of killing AT LEAST all the enemies armies.
def capture_chance(region, neighbor):
    n = region.troop_count
    k = neighbor.troop_count
    p = 0.6
    sum = 0

    while k < n:
        sum += (factorial(n)/(factorial(k)*factorial(n-k))) * p**k * (1 - p)**(n-k)
        k += 1
    return sum


