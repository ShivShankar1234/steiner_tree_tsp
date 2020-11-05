from custom_utils import *
import networkx as nx

def get_steiner_sol(list_of_homes_index, startingCarIndex, G):     # must pass in list of homes indices and startingCarIndex!
    steinerTree = steiner_tree(G, list_of_homes_index + [startingCarIndex])
    #print("Steiner Tree")
    treeTraversal = list(nx.algorithms.traversal.dfs_preorder_nodes(steinerTree, source=startingCarIndex))
    steinerCarCycle = []
    for i in range(len(treeTraversal)-1):
        start = treeTraversal[i]
        end = treeTraversal[i+1]
        #SteinerTree
        shortest_path = nx.shortest_path(steinerTree, start, end)       #change steinerTree to G ?
        steinerCarCycle.extend(shortest_path[:len(shortest_path)-1])
    #SteinerTree
    lastShortPath = nx.shortest_path(steinerTree, treeTraversal[len(treeTraversal)-1], startingCarIndex)
    steinerCarCycle.extend(lastShortPath)
    dropoff_mapping = {x: [x] for x in list_of_homes_index}
    return steinerCarCycle, dropoff_mapping

def find_prune_vertices(car_cycle):
    remove_from_car_cycle = []
    add_to_dropoff_dictionary = {}
    i = 0
    while i < len(car_cycle) - 2:
        if car_cycle[i] == car_cycle[i + 2]:
            other_vert = car_cycle[i]
            leaf = car_cycle[i+1]
            if leaf not in remove_from_car_cycle:
                remove_from_car_cycle.append(leaf)
                if other_vert not in add_to_dropoff_dictionary:
                    add_to_dropoff_dictionary.update({other_vert : leaf})
                else:
                    add_to_dropoff_dictionary.udpate({other_vert : (add_to_dropoff_dictionary.get(other_vert)).extend(leaf)})
            i += 3
        else:
            i += 1
    return remove_from_car_cycle, add_to_dropoff_dictionary


def prune_steiner(remove_from_car_cycle, add_to_dropoff_dictionary, list_of_homes_index, startingCarIndex, G):
    #run steiner on the new list of homes
    #remove the remove_from_car_cycle from the list of list_of_homes_index and run steiner_tree
    list_of_homes_index.remove(remove_from_car_cycle)
    new_cc, new_dd = get_steiner_sol(list_of_homes_index, startingCarIndex, G)
    for k in add_to_dropoff_dictionary:
        newVal = new_dd.get(k)
        newVal.extend(add_to_dropoff_dictionary.get(k))
        new_dd.update({k : newVal})
    return new_cc, new_dd


def pruning_process(steinerCarCycle, list_of_homes_index, startingCarIndex, G):
    remove_from_cc, add_to_dd = find_prune_vertices(steinerCarCycle)
    return prune_steiner(remove_from_cc, add_to_dd, list_of_homes_index, startingCarIndex, G)
    #take care of all of the helper functions in one function



