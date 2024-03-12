#include <bits/stdc++.h>
using namespace std;

/**
 * @brief Node maintains adjacency list of each neighbour
 *
 */
class Node
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
    vector<pair<Node *, int>> adjNodes;

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
    Node(int n, int regenerations)
    {
        this->node = n;
        this->regenerations = regenerations;
    }

    void AssignNeighbour(Node *n, int dist)
    {
        this->adjNodes.push_back({n, dist});
    }
};

unordered_map<int, Node *> CreateNodeControlBlock(vector<vector<int>> matrix, int regenerations)
{
    unordered_map<int, Node *> ControlBlock;
    int no_of_nodes = matrix.size();

    /**
     * @brief This loop creates every node block for the given network.
     *
     */
    for (int i = 0; i < no_of_nodes; i++)
    {
        ControlBlock[i + 1] = new Node(i + 1, regenerations);
    }

    /**
     * @brief This loop assign neighbours of each node for the given network.
     *
     */
    for (int i = 0; i < no_of_nodes; i++)
    {
        for (int j = 0; j < no_of_nodes; j++)
        {
            if (matrix[i][j] != 0)
            {
                /**
                 * @brief For node "i + 1", assign neighbour "j + 1" with cost/distance.
                 *
                 */
                ControlBlock[i + 1]->AssignNeighbour(ControlBlock[j + 1], matrix[i][j]);
            }
        }
    }

    return ControlBlock;
}

void PrintAdjacencyList(unordered_map<int, Node *> ControlBlock)
{
    for (auto [key, value] : ControlBlock)
    {
        cout << "Node: " << key << " Adjacent Nodes: ";
        for (auto v : value->adjNodes)
        {
            cout << "(" << v.first->node << "," << v.second << ") ";
        }
        cout << endl;
    }
}