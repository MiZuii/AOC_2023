# --------------------------------- FILE OPEN -------------------------------- #
import os
n = int(__file__[-4:-3])
inputf = open(os.path.dirname(__file__) + f"/input{n}.txt", "r")
# -------------------------------- PUZZLE CODE ------------------------------- #

def get_new_ranges(mapd, maps, mapr, ss, sr):
    # returns two lists. First with the updated (max 2) pairs of seeds
    # that were not changed by the new map -> This ranges should go back to seed array
    # Seccond with the updated sets of seeds (max 2) The cannot be changed seccond time
    # by the same map soo they need to have separate list (which will be merged with seeds 
    # at the end)

    # get ranges min and max values
    seeds_min = ss
    seeds_max = ss + sr - 1
    map_min = maps
    map_max = maps + mapr - 1

    map_shift = mapd-maps

    # case 1: whole seeds set is in the map set (equal sets also fall in here)
    if seeds_min >= map_min and seeds_max <= map_max:
        # the whole set gets transformed
        return [], [seeds_min + map_shift, sr]

    # case 2: whole map set is in seeds set (cannot include equal sets but one of the edges can match)
    elif map_min >= seeds_min and map_max <= seeds_max:
        # one fully changed set is created and 1 or 2 not changed sets arise
        
        #fully_changed = [mapd, mapr] - > put directly into return

        unchanged_sets = []

        left_set_start = seeds_min
        left_set_range = seeds_min - map_min

        right_set_start = map_max + 1
        right_set_range = seeds_max - map_max

        if left_set_range > 0:
            unchanged_sets.extend([left_set_start, left_set_range])

        if right_set_range > 0 :
            unchanged_sets.extend([right_set_start, right_set_range])

        return unchanged_sets, [mapd, mapr]

    # case 3: sets are disjoint
    elif map_min > seeds_max or map_max < seeds_min:
        return [ss, sr], []

    # case 4: map is to the left
    elif map_min <= seeds_min and seeds_min <= map_max:
        joint_range = map_max - seeds_min + 1
        return [seeds_min + joint_range, sr - joint_range], [seeds_min + map_shift, joint_range]

    # case 5: map is to the right
    elif seeds_min <= map_min and map_min <= seeds_max:
        joint_range = seeds_max - map_min + 1
        return [seeds_min, sr - joint_range], [seeds_min + sr - joint_range + map_shift, joint_range]


# global variables
seeds = []

# input processing
input = inputf.read().split("\n")
i = 0
while 1:
    if input[i][:5] == 'seeds':
        seeds = list(map(int, input[i][7:].split(" ")))
    if input[i][:5] in ('seed-', 'soil-', 'ferti', 'water', 'light', 'tempe', 'humid'):

        i += 1
        nseeds = []
        while i < len(input) and len(input[i]):
            line_num_set = list(map(int, input[i].split(" ")))

            useeds = []
            # iterate through sets of ranges and update them to the nseeds array
            for ri in range(0, len(seeds), 2):
                g = get_new_ranges(line_num_set[0], line_num_set[1], line_num_set[2], seeds[ri], seeds[ri+1])
                useeds.extend(g[0])
                nseeds.extend(g[1])

            seeds = useeds

            i += 1

        seeds.extend(nseeds)

    i += 1
    if i > len(input):
        break

print(min([seed for i, seed in enumerate(seeds) if i % 2 == 0]))

# -------------------------------- FILE CLOSE -------------------------------- #
inputf.close()