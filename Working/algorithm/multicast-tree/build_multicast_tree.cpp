#include <bits/stdc++.h>
#include "../node-related/build_adjacency_list.cpp"
#include "../request-collector/collect.cpp"

using namespace std;

/**
 * @brief Pair of {dist, Node}
 *
 */
typedef pair<int, NodeBlock *> distNode;
/**
 * @brief Pair of {dist, {Node*, {Node *, []Node*}
 *
 */
typedef pair<int, pair<NodeBlock *, pair<NodeBlock *, vector<distNode>>>> distSrcDestNodesPair;
/**
 * @brief Pair of {dist, dist} or {Node, Node}
 *
 */
typedef pair<int, int> dist_node_pair;

/**
 * @brief Finds SSSP for a given node.
 *
 * @param src Source Node
 * @param dest Destinations
 * @param ControlBlock Node Control Block
 * @param treeNodes Nodes that are added to Steiner tree
 * @return pair<int, pair<Node *, pair<Node *, vector<distNode>>>>
 */
distSrcDestNodesPair DijkstraAlgo(NodeBlock *src, vector<int> dest, unordered_map<int, NodeBlock *> ControlBlock, vector<NodeBlock *> treeNodes)
{
    priority_queue<distNode, vector<distNode>, greater<distNode>> keepDestinations;
    vector<int> destinations(ControlBlock.size(), INT_MAX);
    vector<distNode> parents(ControlBlock.size());
    destinations[src->node - 1] = 0;
    keepDestinations.push({0, src});
    parents[src->node - 1] = {0, nullptr};

    while (!keepDestinations.empty())
    {
        NodeBlock *u = keepDestinations.top().second;
        keepDestinations.pop();

        for (auto v : u->adjNodes)
        {
            if (v.second + destinations[u->node - 1] < destinations[v.first->node - 1])
            {
                destinations[v.first->node - 1] = v.second + destinations[u->node - 1];
                parents[v.first->node - 1] = {destinations[v.first->node - 1], u};
                keepDestinations.push({destinations[v.first->node - 1], v.first});
            }
        }
    }

    distNode shortestDestination = {INT_MAX, nullptr};

    for (auto v : dest)
    {
        if (find(treeNodes.begin(), treeNodes.end(), ControlBlock[v]) == treeNodes.end())
        {
            if (destinations[v - 1] < shortestDestination.first)
            {
                shortestDestination = {destinations[v - 1], ControlBlock[v]};
            }
        }
    }

    // Store path from source to destination i.e. src, internmediate and destination nodes.
    vector<distNode> path;
    path.push_back(parents[shortestDestination.second->node - 1]);
    distNode temp = parents[shortestDestination.second->node - 1];
    while (temp.second != src)
    {
        path.push_back(parents[temp.second->node - 1]);
        temp = parents[temp.second->node - 1];
    }

    return {shortestDestination.first, {src, {shortestDestination.second, path}}};
}

/**
 * @brief Generates a multicast tree for each request.
 *
 * @param ControlBlock
 * @param req
 */
void MulticastTree(unordered_map<int, NodeBlock *> ControlBlock, TreeInputRequestBlock req)
{
    vector<NodeBlock *> treeNodes;
    vector<stack<dist_node_pair>> paths(req.dest.size());
    int servedPath = 0;

    // add source to tree
    treeNodes.push_back(ControlBlock[req.src]);

    // For printing purpose, show the user what was the src, dest and demand
    cout << "Source: " << req.src << " Destinations: ";
    for (auto v : req.dest)
    {
        cout << v << " ";
    }
    cout << "Demand: " << req.demand << endl;
    // The result is manipulated following...

    // for each node in steiner tree find shortest destination from destination set
    while (req.dest.size())
    {
        // Holds shortest distance from source to destination
        distSrcDestNodesPair shortestFromTree = {INT_MAX, {nullptr, {nullptr, {}}}};
        for (auto v : treeNodes)
        {
            distSrcDestNodesPair algoResult = DijkstraAlgo(v, req.dest, ControlBlock, treeNodes);
            if (algoResult.first < shortestFromTree.first)
                shortestFromTree = algoResult;
        }

        // Add the destination to the steiner tree
        treeNodes.push_back(shortestFromTree.second.second.first);
        paths[servedPath].push({shortestFromTree.first, shortestFromTree.second.second.first->node});

        // Add intermediate nodes from source to destination
        for (auto v : shortestFromTree.second.second.second)
        {
            paths[servedPath].push({v.first, v.second->node});
            if (v.second != nullptr && find(treeNodes.begin(), treeNodes.end(), v.second) == treeNodes.end())
            {
                treeNodes.push_back(v.second);
            }
        }

        // <--- Start: Print intermediate paths --->
        // for (auto v : shortestFromTree.second.second.second)
        // {
        //     cout << v.first << " ";
        //     v.second == nullptr ? cout << "null" : cout << v.second->node;
        //     cout << endl;
        // }
        // <--- End: Print intermediate paths --->
        // paths.push({shortestFromTree.second.first->node, shortestFromTree.second.second.first->node});

        // Remove the destination from "dest" which is added to the steiner tree
        auto it = find(req.dest.begin(), req.dest.end(), shortestFromTree.second.second.first->node);
        req.dest.erase(it);
        servedPath++;
    }
    cout << "Tree: " << endl;
    for (auto v : paths)
    {
        cout << "(";
        while (!v.empty())
        {
            cout << v.top().second;
            v.size() > 1 ? cout << " -> " : cout << "";
            v.pop();
        }
        cout << ") " << endl;
    }
}

/**
 * @brief Algorithm 1
 *
 */
void BuildTree()
{
    int regenerations;
    cout << "Please enter the number of regenerations: ";
    cin >> regenerations;
    // Step 1: Create adjacency list
    unordered_map<int, NodeBlock *> ControlBlock = GenerateAdjacencyList(regenerations);
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