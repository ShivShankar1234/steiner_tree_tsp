import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
from custom_utils import *
from prune import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """

    """ Nearest Neighbor/Simulated Annealing Solution """
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    # all_paths = nx.all_shortest_paths(G)
    car_cycle = []
    dropoff_mapping = []
    car_cycle.append(starting_car_location)
    loc_indices = convert_locations_to_indices(list_of_locations, list_of_locations)
    locToIndexDict = {}
    for i in range(len(list_of_locations)):
        locToIndexDict.update({list_of_locations[i]: loc_indices[i]})


    all_pairs_dist = nx.floyd_warshall(G)  # this is a dictionary keyed by source and target

    def get_distance(destination):
        path_dist = (all_pairs_dist.get(locToIndexDict.get(source))).get(locToIndexDict.get(destination))
        # print(path_dist)
        if path_dist == 0:
            return float('inf')
        return path_dist

    unvisited_homes = set(list_of_homes)  # nearest neighbor as initial solution
    if starting_car_location in unvisited_homes:
        unvisited_homes.remove(starting_car_location)
    source = starting_car_location
    while unvisited_homes:
        next_node = min(unvisited_homes, key=get_distance)
        # djikstras a path from source to dest
        shortest_path = nx.shortest_path(G, list_of_locations.index(source), list_of_locations.index(next_node))
        for i in range(len(shortest_path)):
            shortest_path[i] = list_of_locations[shortest_path[i]]
        car_cycle.extend(shortest_path[1:])  # we dont need to append the source twice
        if source in unvisited_homes:
            unvisited_homes.remove(source)
        source = next_node
    shortest_path = nx.shortest_path(G, list_of_locations.index(source), list_of_locations.index(starting_car_location))
    for i in range(len(shortest_path)):
        shortest_path[i] = list_of_locations[shortest_path[i]]
    car_cycle.extend(shortest_path[1:])

    car_cycle = convert_locations_to_indices(car_cycle, list_of_locations)
    list_of_homes_index = convert_locations_to_indices(list_of_homes, list_of_locations)
    dropoff_mapping = {x: [x] for x in list_of_homes_index}
    # this is where we start simulated annealing
    # print(cost_of_solution(G, car_cycle, dropoff_mapping))
    #return car_cycle, dropoff_mapping

    startingCarIndex = convert_locations_to_indices([starting_car_location], list_of_locations)[0]
    dropoff_map = {startingCarIndex: convert_locations_to_indices(list_of_homes, list_of_locations)}

    driveCost, driveMessage = cost_of_solution(G, car_cycle, dropoff_mapping)
    walkCost, walkMessage = cost_of_solution(G,[startingCarIndex], dropoff_map)
    #everybody walk home
    #print("Nearest Neighbor")
    #print(driveMessage)
    #print()
    #print("Walk Back Bitch")
    #print(walkMessage)
    #print()
    #if driveCost > walkCost:
        #return [startingCarIndex], dropoff_map
    #else:
        #return car_cycle, dropoff_mapping

    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    # all_paths = nx.all_shortest_paths(G)
    #car_cycle = []
    dropoff_mapping = []
    #car_cycle.append(startingCarIndex)
    loc_indices = convert_locations_to_indices(list_of_locations, list_of_locations)
    locToIndexDict = {}
    for i in range(len(list_of_locations)):
        locToIndexDict.update({list_of_locations[i]: loc_indices[i]})

    all_pairs_dist = nx.floyd_warshall(G)  # this is a dictionary keyed by source and target
    startingCarIndex = convert_locations_to_indices([starting_car_location], list_of_locations)[0]

    def get_distance(destination):
        path_dist = (all_pairs_dist.get(locToIndexDict.get(source))).get(locToIndexDict.get(destination))
        # print(path_dist)
        if path_dist == 0:
            return float('inf')
        return path_dist

    list_of_homes_index = convert_locations_to_indices(list_of_homes, list_of_locations)
    steinerTree = steiner_tree(G, list_of_homes_index + [startingCarIndex])
    #print("Steiner Tree")
    treeTraversal = list(nx.algorithms.traversal.dfs_preorder_nodes(steinerTree, source=startingCarIndex))
    steinerCarCycle = []
    for i in range(len(treeTraversal)-1):
        start = treeTraversal[i]
        end = treeTraversal[i+1]
        #SteinerTree
        shortest_path = nx.shortest_path(steinerTree, start, end)
        steinerCarCycle.extend(shortest_path[:len(shortest_path)-1])
    #SteinerTree
    lastShortPath = nx.shortest_path(steinerTree, treeTraversal[len(treeTraversal)-1], startingCarIndex)
    steinerCarCycle.extend(lastShortPath)
    dropoff_mapping = {x: [x] for x in list_of_homes_index}
    steinerCost, steinerMessage = cost_of_solution(G, steinerCarCycle, dropoff_mapping)
    #print(steinerMessage)
    #print()

    #I FIXED THIS OKOKOJOHOIBOBKGHGLJK
    #steinerPrunedCycle, steinerPrunedMapping = prune_leaves(steinerCarCycle, dropoff_mapping)
    steinerPrunedCycle, steinerPrunedMapping = pruning_process(steinerCarCycle, list_of_homes_index, startingCarIndex, G)
    steinerPrunedCost, steinerPrunedMessage = cost_of_solution(G, steinerPrunedCycle, steinerPrunedMapping)

    carPrunedCycle, carPrunedMapping = prune_leaves(car_cycle, dropoff_mapping)
    carPrunedCost, carPrunedMessage = cost_of_solution(G, carPrunedCycle, carPrunedMapping)
    #print(steinerPrunedMessage)


    #if min(steinerPrunedCost, walkCost, carPrunedCost) == steinerPrunedCost:
    #print("Min in steiner cost")
    #print(steinerCarCycle)
    #print()
    #print("Pruned Steiner")
    #steinerPrunedCycle, steinerPrunedMapping = prune_leaves(steinerCarCycle, dropoff_mapping)
    #steinerPrunedCost, steinerPrunedMessage = cost_of_solution(G, steinerPrunedCycle, steinerPrunedMapping)
        #print("steiner pruned")
        #print(steinerPrunedMessage)
    #print(steinerPrunedCycle)
        #return steinerPrunedCycle, steinerPrunedMapping
    if min(steinerPrunedCost, walkCost, carPrunedCost) == walkCost:
        print("Min is walkCost")
        return [startingCarIndex], dropoff_map
    else:
        # print("Min in steiner cost")
        # print(steinerCarCycle)
        # print()
        # print("Pruned Steiner")
        # steinerPrunedCycle, steinerPrunedMapping = prune_leaves(steinerCarCycle, dropoff_mapping)
        # steinerPrunedCost, steinerPrunedMessage = cost_of_solution(G, steinerPrunedCycle, steinerPrunedMapping)
        #print("steiner pruned")
        #print(steinerPrunedMessage)
        print(steinerPrunedCycle)
        return steinerPrunedCycle, steinerPrunedMapping
    #else:
        #print("Min is TSP Solution Cost")
        #print(convert_index_to_locations(car_cycle, list_of_locations))
        #print(driveMessage)
        #print("PRuned NN")
        #print(carPrunedMessage)
        #print(convert_index_to_locations(carPrunedCycle, list_of_locations))
        #return carPrunedCycle, carPrunedMapping


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
