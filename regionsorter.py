

class Sorter(object):
    @staticmethod
    def sorting(references, bot, descending):
        regions = {}
        #get weight values for regions
        for i in references:
            regions[i] = bot.map_weights.region_weight[i.id]
       
         
        regions_by_weight = [[key, value] for key, value in regions.items()]
        regions_by_weight.sort(key=lambda region: region[1], reverse=descending)
    
        #print(regions_by_weight)

        ordered_regions = []
        for region in regions_by_weight :
            ordered_regions.append(region[0])
       
    
        return ordered_regions
        

