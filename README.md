# steiner_tree_tsp
A TSP Approximation Using LP  Reduction to the Minimum Steiner Tree Problem


We reduce the problem of the Travelling Salesman with Pickup and Delivery (TSPPD) to the Metric TSP. This involves generating an minimum spanning tree over each of the homes (vertices), running a DFS traversal of T, and then removing the repeated vertices from the traversal, if possible.

This approach involves generating a MST through a subset of vertices (the homes). In other words we are looking to find the Minimum Steiner Tree that contains the TA’s homes. We can achieve a 2-approximate algorithm for the Minimum Steiner Tree by using an MST that exclusively contains TA homes (there is a networkx function for this).

Thus our driving path will be the non-repeating DFS traversal of this MST followed by taking the shortest path between the last node in the traversal, and the source node. Note that in this approach, we will be dropping each TA off at their house, so the walking cost will be zero.
This will work well if the graph is fairly dense because this may allow a path that involves driving to multiple TA homes one after another without driving back over the same edges. In this way, walking would be inefficient as we can drive along a path with multiple homes along it and drop each TA at their house along the way.

To incorporate walking, we will employ clustering. we will start by using a clustering algorithm to cluster the location vertices into k clusters with centers: c1, c2, ... ck . We can then run the Floyd-Warshall algorithm to find the shortest path between all pairs of vertices and store them in a matrix M[][], where M[i][j] is the shortest path distance from any vertex vi to vj. First we will use this to create a clustering dictionary, D, which pairs each vertex to its nearest vertex center (i.e. D[ci] will yield a list of vertices in the cluster centered at ci). We will then run the algorithm from approach 1, but we will use the set of cluster centers as the subset that the Steiner Tree must pass through (rather than the set of TA homes).

Thus our driving path will be the non-repeating DFS traversal of this MST followed by taking the shortest path between the last node in the traversal, and the source node. Note that in this approach, we will be driving to each cluster center. At each cluster center ci, we drop off the delivery man given by our dictionary D[ci] , each of whom will walk to their respective home.

This approach will work better in sparse graphs, in which driving a TA directly home may result in driving over the same edge twice. To avoid this, we can cluster the homes and simply drive through the cluster centers where we drop of deliveymen to drop off packages of people who live nearby.
