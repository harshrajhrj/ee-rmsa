#include <bits/stdc++.h>
#define NODES 6

using namespace std;

/**
 * @brief Populate 50 x each in {1,2,3,4,5,6} requests.
 *
 * @return vector<int>
 */
vector<int> NetworkRequests(int scale_factor)
{
    vector<int> reqs;
    for (int i = 1; i <= scale_factor; i++)
    {
        reqs.push_back(50 * i);
    }
    return reqs;
}

/**
 * @brief Populate node name in a set. Ex: 1 2 3 4 ...
 *
 * @return set<int>
 */
set<int> GenerateNodes()
{
    set<int> nodes;
    for (int i = 1; i <= NODES; i++)
    {
        nodes.insert(i);
    }
    return nodes;
}

/**
 * @brief Generates a random node from given set.
 * [Help 1](https://www.techiedelight.com/get-random-value-stl-containers-cpp/)
 * [Help 2](https://stackoverflow.com/questions/3052788/how-to-select-a-random-element-in-stdset)
 * @param nodes
 * @param size
 * @return auto
 */
auto random(set<int> &nodes, size_t size)
{
    auto it = nodes.begin();
    advance(it, size);
    return it;
}

/**
 * @brief Create a Request File object
 *
 * @param d_type
 * @param reqs
 */
void CreateRequestFile(string d_type, int reqs, int d_scale)
{
    int demand = d_scale; // initialized to d_scale
    if (d_type == "LSD")
        demand = d_scale; // 40
    else if (d_type == "MSD")
        demand = d_scale * 2; // 80
    else if (d_type == "HSD")
        demand = d_scale * 3; // 120
    else
    {
        demand = (rand() % 4 + 1) * d_scale; // any of 40, 80, 120 and 160
    }

    string path = "../../requests/" + to_string(reqs) + "_" + d_type + "_" + to_string(NODES) + ".txt";
    fstream file(path, ios::out);

    int i = 0;
    while (i < reqs)
    {
        set<int> nodes = GenerateNodes();
        int source = rand() % 6 + 1;
        for (auto it = nodes.begin(); it != nodes.end(); it++)
        {
            if (*it == source)
            {
                nodes.erase(it);
                break;
            }
        }

        vector<int> dest;
        for (int D = 0; D < 3; D++)
        {
            auto r = rand() % nodes.size();
            auto n = random(nodes, r);
            dest.push_back(*n);
            nodes.erase(n);
        }

        // https://stackoverflow.com/questions/8581832/converting-a-vectorint-to-string
        ostringstream oss;
        // Convert all but the last element to avoid a trailing ","
        copy(dest.begin(), dest.end() - 1, ostream_iterator<int>(oss, ","));

        // Now add the last element with no delimiter
        oss << dest.back();

        if (file)
        {
            file << source << "[" << oss.str() << "]" << demand << endl;
        }

        i++;
    }

    file.close();
}

/**
 * @brief Driver function for generating requets.
 *
 */
void RequestGenerator()
{
    int req_scale_factor;
    cout << "Please enter the rwquest scale factor: ";
    cin >> req_scale_factor;
    vector<int> reqs = NetworkRequests(req_scale_factor);

    int demand_scale_factor;
    cout << "Please enter the demand scale factor: ";
    cin >> demand_scale_factor;

    vector<string> demand = {"LSD", "MSD", "HSD", "VSD"};

    for (auto d : demand)
    {
        for (auto r : reqs)
        {
            CreateRequestFile(d, r, demand_scale_factor);
        }
    }

    cout << "Finished generating requests.";
}

int main()
{
    RequestGenerator();
}