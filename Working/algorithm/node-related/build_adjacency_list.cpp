#include <bits/stdc++.h>
#include "node_block.cpp"

using namespace std;

unordered_map<int, NodeBlock *> GenerateAdjacencyList(int regenerations)
{
    ifstream network("../../network-matrix/paper_24.txt");
    // int no_of_nodes = 6;
    vector<vector<int>> matrix;
    if (network.is_open())
    {
        string my_line;
        while (!network.eof())
        {
            getline(network, my_line);
            vector<int> weights;
            string weight = "";
            for (auto v : my_line)
            {
                if (v != ' ' && v != '\n')
                {
                    weight += v;
                }
                else
                {
                    weights.push_back(stoi(weight));
                    weight = "";
                }
            }
            matrix.push_back(weights);
        }
    }
    unordered_map<int, NodeBlock *> ControlBlock = CreateNodeControlBlock(matrix, regenerations);
    // PrintAdjacencyList(ControlBlock);
    return ControlBlock;
}

void PrintAdjacencyList(unordered_map<int, NodeBlock *> ControlBlock)
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