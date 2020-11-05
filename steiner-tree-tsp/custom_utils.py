from itertools import combinations, chain

from networkx.utils import pairwise, not_implemented_for
import networkx as nx

__all__ = ['metric_closure', 'steiner_tree', 'prune_leaves', 'convert_index_to_locations']

def convert_index_to_locations(list_of_indices, list_of_locations):
    return [list_of_locations[i] for i in list_of_indices]


def prune_leaves(car_cycle, dropoff_dictionary):
    #is car_cycle a list of strings or indices?
    #car_cycle_ind = convert_locations_to_indices(car_cycle, list_of_locations) , i think car cycle is already in terms of indices
    pruned_car_cycle_ind = []
    pruned_drop_off_dictionary = {}
    i = 0
    while i < len(car_cycle) - 2:
        middle_element = car_cycle[i]
        if car_cycle[i] == car_cycle[i + 2]:
            pruned_car_cycle_ind.append(car_cycle[i])
            new_val = [car_cycle[i + 1]]
            if middle_element in dropoff_dictionary:
                if middle_element not in pruned_drop_off_dictionary:
                    new_val.extend(dropoff_dictionary.get(middle_element))
                else:
                    new_val.extend(pruned_drop_off_dictionary.get(middle_element))
            pruned_drop_off_dictionary.update({car_cycle[i] : new_val})
            i += 3
        else:
            pruned_car_cycle_ind.append(middle_element)
            if middle_element in dropoff_dictionary:
                if middle_element not in pruned_drop_off_dictionary:
                    pruned_drop_off_dictionary.update({middle_element : dropoff_dictionary.get(middle_element)})
                else:
                    if middle_element not in pruned_drop_off_dictionary.get(middle_element):
                        pruned_drop_off_dictionary.update({middle_element: pruned_drop_off_dictionary.get(middle_element)})
            #no dictionary entry for these
            i += 1
    while i < len(car_cycle):
        ele = car_cycle[i]
        pruned_car_cycle_ind.append((ele))
        if ele in dropoff_dictionary:
            if ele not in pruned_drop_off_dictionary:
                pruned_drop_off_dictionary.update({ele: dropoff_dictionary.get(ele)})
            else:
                if ele not in pruned_drop_off_dictionary.get(ele):
                    pruned_drop_off_dictionary.update({ele: pruned_drop_off_dictionary.get(ele)})
        i += 1
    #for i in range(len(pruned_car_cycle_ind)):          #convert the car_cycle list of indices to list of strings
        #pruned_car_cycle_ind[i] = list_of_locations[i]
    return pruned_car_cycle_ind, pruned_drop_off_dictionary

@not_implemented_for('directed')
def metric_closure(G, weight='weight'):
    """  Return the metric closure of a graph.

    The metric closure of a graph *G* is the complete graph in which each edge
    is weighted by the shortest path distance between the nodes in *G* .

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    NetworkX graph
        Metric closure of the graph `G`.

    """
    M = nx.Graph()

    Gnodes = set(G)

    # check for connected graph while processing first node
    all_paths_iter = nx.all_pairs_dijkstra(G, weight=weight)
    u, (distance, path) = next(all_paths_iter)
    if Gnodes - set(distance):
        msg = "G is not a connected graph. metric_closure is not defined."
        raise nx.NetworkXError(msg)
    Gnodes.remove(u)
    for v in Gnodes:
        M.add_edge(u, v, distance=distance[v], path=path[v])

    # first node done -- now process the rest
    for u, (distance, path) in all_paths_iter:
        Gnodes.remove(u)
        for v in Gnodes:
            M.add_edge(u, v, distance=distance[v], path=path[v])

    return M



@not_implemented_for('multigraph')
@not_implemented_for('directed')
def steiner_tree(G, terminal_nodes, weight='weight'):
    """ Return an approximation to the minimum Steiner tree of a graph.

    Parameters
    ----------
    G : NetworkX graph

    terminal_nodes : list
         A list of terminal nodes for which minimum steiner tree is
         to be found.

    Returns
    -------
    NetworkX graph
        Approximation to the minimum steiner tree of `G` induced by
        `terminal_nodes` .

    Notes
    -----
    Steiner tree can be approximated by computing the minimum spanning
    tree of the subgraph of the metric closure of the graph induced by the
    terminal nodes, where the metric closure of *G* is the complete graph in
    which each edge is weighted by the shortest path distance between the
    nodes in *G* .
    This algorithm produces a tree whose weight is within a (2 - (2 / t))
    factor of the weight of the optimal Steiner tree where *t* is number of
    terminal nodes.

    """
    # M is the subgraph of the metric closure induced by the terminal nodes of
    # G.
    M = metric_closure(G, weight=weight)
    # Use the 'distance' attribute of each edge provided by the metric closure
    # graph.
    H = M.subgraph(terminal_nodes)
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # Create an iterator over each edge in each shortest path; repeats are okay
    edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
    T = G.edge_subgraph(edges)
    return T

