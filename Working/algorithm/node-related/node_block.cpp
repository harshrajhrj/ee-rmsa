#include <bits/stdc++.h>
#include "node_class.cpp"

unordered_map<int, NodeBlock *> CreateNodeControlBlock(vector<vector<int>> matrix, int regenerations)
{
    unordered_map<int, NodeBlock *> ControlBlock;
    int no_of_nodes = matrix.size();

    /**
     * @brief This loop creates every node block for the given network.
     *
     */
    for (int i = 0; i < no_of_nodes; i++)
    {
        ControlBlock[i + 1] = new NodeBlock(i + 1, regenerations);
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