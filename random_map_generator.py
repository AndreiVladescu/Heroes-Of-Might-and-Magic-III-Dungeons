import numpy as np
import random
from os import path
def map_gen():
    map_width = 64
    map_height = 64
    map_matrix = np.zeros([64, 64], dtype = str)
    was_player_generated = False
    mob_count = 16
    h_potion_count = 10
    m_potion_count = 10
    wall_count = 64
    wood_count = 16
    ore_count = 16

    #Generate Map
    for i in range(map_height):
        for j in range(map_width):
            random_item_drop = random.uniform(0, 250)

            if j == 0 or j == map_width - 1 or i == 0 or i == map_height - 1:
                map_matrix[i][j] = '1'
            #elif not was_player_generated and random_item_drop < 50:
            elif wall_count > 0 and random_item_drop < 5:
                map_matrix[i][j] ='1'
                wall_count -= 1
            elif h_potion_count > 0 and random_item_drop <7:
                map_matrix[i][j] = 'H'
                h_potion_count -= 1
            elif m_potion_count > 0 and random_item_drop <9:
                map_matrix[i][j] = 'm'
                m_potion_count -= 1
            elif wood_count > 0 and random_item_drop < 11:
                map_matrix[i][j] = 'w'
                wood_count -= 1
            elif ore_count > 0 and random_item_drop < 13:
                map_matrix[i][j] = 'o'
                ore_count -= 1
            elif mob_count > 0 and random_item_drop < 18:
                map_matrix[i][j] = 'M'
                mob_count -= 1
            else:
                map_matrix[i][j]='.'
            map_matrix[1][1] = 'P'
            map_matrix[62][62] = 'B'
    game_dir = path.dirname(__file__)
    map_dir = path.join(game_dir, 'map')
    map_dir = path.join(map_dir ,'random_map.txt')
    map_file = open(map_dir, 'w')
    line_str = ""
    for i in range(1 , map_height):
        for j in range(1 , map_width):
            line_str = str(line_str) + str(map_matrix[i][j])
        line_str += '\n'
        map_file.write(line_str)
        line_str = '1'
    map_file.close()