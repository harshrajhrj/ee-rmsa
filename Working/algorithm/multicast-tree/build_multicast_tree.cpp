#include <bits/stdc++.h>
#include <filesystem>
namespace fs = std::filesystem;
#include "../adjacency-list/build_adjacency_list.cpp"

using namespace std;

class TreeInputRequestBlock
{
public:
    /**
     * @brief Source
     *
     */
    int src;
    /**
     * @brief Set of destinations
     *
     */
    vector<int> dest;
    /**
     * @brief Request demand (bandwidth in Gbps)
     *
     */
    int demand;

    /**
     * @brief Construct a new Tree Input Request Block object
     *
     * @param req_literal
     */
    TreeInputRequestBlock(string req_literal)
    {
        // <--- InputHandlers --->

        string token = "";
        bool src_check = true;
        bool dest_check = false;

        for (auto v : req_literal)
        {
            if (v == '[')
            {
                this->src = stoi(token);
                token = "";
                dest_check = true;
                src_check = false;
            }
            else if (v == ']')
            {
                this->dest.push_back(stoi(token));
                token = "";
                dest_check = false;
            }
            else if (src_check)
            {
                token += v;
            }
            else if (dest_check)
            {
                if (v != ',')
                {
                    token += v;
                }
                else
                {
                    this->dest.push_back(stoi(token));
                    token = "";
                }
            }
            else
            {
                token += v;
            }
        }
        this->demand = stoi(token);
        token = "";
    }
};

vector<TreeInputRequestBlock> CollectRequests()
{
    string path = "../../requests";
    vector<TreeInputRequestBlock> requests;

    /**
     * @brief Construct a new for object. Collect files from a directory
     *
     * @param fs::directory_iterator
     */
    for (const auto &entry : fs::directory_iterator(path))
    {

        fstream file(entry.path(), ios::in);
        if (file)
        {
            string new_line;
            while (!file.eof())
            {
                getline(file, new_line);
                if (!new_line.size())
                    continue;

                // <--- Start: inputs to the steiner tree --->

                TreeInputRequestBlock req_block(new_line);

                // <--- Start: inputs to the steiner tree --->

                // <--- Start: Debugging purpose --->
                // cout << new_line << " Source: " << req_block.src << " Destinations: ";
                // for (auto v : req_block.dest)
                // {
                //     cout << v << " ";
                // }
                // cout << "Demand: " << req_block.demand << endl;
                // <--- End: Debugging purpose --->
                requests.push_back(req_block);
            }
        }
        file.close();
    }
    return requests;
}

pair<int, pair<Node *, Node *>> DijkstraAlgo(Node *src, vector<int> dest, unordered_map<int, Node *> ControlBlock, vector<Node *> treeNodes)
{
    priority_queue<pair<int, Node *>, vector<pair<int, Node *>>, greater<pair<int, Node *>>> keepDestinations;
    vector<int> destinations(ControlBlock.size(), INT_MAX);
    destinations[src->node - 1] = 0;
    keepDestinations.push({0, src});

    while (!keepDestinations.empty())
    {
        Node *u = keepDestinations.top().second;
        keepDestinations.pop();

        for (auto v : u->adjNodes)
        {
            if (v.second + destinations[u->node - 1] < destinations[v.first->node - 1])
            {
                destinations[v.first->node - 1] = v.second + destinations[u->node - 1];
                keepDestinations.push({destinations[v.first->node - 1], v.first});
            }
        }
    }

    priority_queue<pair<int, Node *>, vector<pair<int, Node *>>, greater<pair<int, Node *>>> shortestDestination;

    for (auto v : dest)
    {
        if (find(treeNodes.begin(), treeNodes.end(), ControlBlock[v]) == treeNodes.end())
        {
            shortestDestination.push({destinations[v - 1], ControlBlock[v]});
        }
    }

    return {shortestDestination.top().first, {src, shortestDestination.top().second}};
}

void MulticastTree(unordered_map<int, Node *> ControlBlock, TreeInputRequestBlock req)
{
    vector<Node *> treeNodes;
    queue<pair<int, int>> paths;

    // add source to tree
    treeNodes.push_back(ControlBlock[req.src]);

    // for each node in steiner tree find shortest destination from destination set
    while (treeNodes.size() != req.dest.size() + 1)
    {
        // min heap
        priority_queue<pair<int, pair<Node *, Node *>>, vector<pair<int, pair<Node *, Node *>>>, greater<pair<int, pair<Node *, Node *>>>> shortestFromTree;
        for (auto v : treeNodes)
        {
            shortestFromTree.push(DijkstraAlgo(v, req.dest, ControlBlock, treeNodes));
        }
        treeNodes.push_back(shortestFromTree.top().second.second);
        paths.push({shortestFromTree.top().second.first->node, shortestFromTree.top().second.second->node});
    }

    cout << "Tree: ";
    while (!paths.empty())
    {
        cout << "(" << paths.front().first << " -> " << paths.front().second << ") ";
        paths.pop();
    }
    cout << endl;
}

void BuildTree()
{
    // Step 1: Create adjacency list
    unordered_map<int, Node *> ControlBlock = GenerateAdjacencyList();
    PrintAdjacencyList(ControlBlock);

    // Step 2: Collect requests
    vector<TreeInputRequestBlock> requests = CollectRequests();

    // Step 3.1: Multicast routing tree construction
    int slots = 13; // pre defined

    // serve each request
    for (auto v : requests)
    {
        MulticastTree(ControlBlock, v);
    }
}

/**
 * @brief Driver function
 *
 * @return int
 */
int main()
{
    BuildTree();
}