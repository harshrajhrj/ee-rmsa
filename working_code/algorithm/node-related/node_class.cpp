#include <bits/stdc++.h>
using namespace std;

/**
 * @brief Node maintains adjacency list of each neighbour
 *
 */
class NodeBlock
{
public:
    /**
     * @brief Node name Ex : node "1".
     *
     */
    int node;

    /**
     * @brief List of Adjacent nodes.
     *
     */
    vector<pair<NodeBlock *, int>> adjNodes;

    /**
     * @brief No of available regenerations
     *
     */
    int regenerations;

    

    /**
     * @brief Construct a new Node object
     *
     * @param n Node name. Ex : node "1"
     */
    NodeBlock(int n, int regenerations)
    {
        this->node = n;
        this->regenerations = regenerations;
    }

    void AssignNeighbour(NodeBlock *n, int dist)
    {
        this->adjNodes.push_back({n, dist});
    }
};