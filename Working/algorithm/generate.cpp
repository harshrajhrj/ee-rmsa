#include <bits/stdc++.h>
#define NODES 6

using namespace std;

vector<int> NetworkRequests()
{
    vector<int> reqs;
    for (int i = 1; i <= 6; i++)
    {
        reqs.push_back(50 * i);
    }
    return reqs;
}

set<int> GenerateNodes()
{
    set<int> nodes;
    for (int i = 1; i <= NODES; i++)
    {
        nodes.insert(i);
    }
    return nodes;
}

// https://www.techiedelight.com/get-random-value-stl-containers-cpp/
// https://stackoverflow.com/questions/3052788/how-to-select-a-random-element-in-stdset
auto random(set<int> &nodes, size_t size)
{
    auto it = nodes.begin();
    advance(it, size);
    return it;
}

void CreateRequestFile(string d_type, int reqs)
{
    int demand = 40;
    if (d_type == "LSD")
        demand = 40;
    else if (d_type == "MSD")
        demand = 80;
    else if (d_type == "HSD")
        demand = 120;
    else
    {
        demand = rand() % 4 + 1;
    }

    string path = "../requests/" + to_string(reqs) + "_" + d_type + "_" + to_string(NODES) + ".txt";
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

void RequestGenerator()
{
    vector<string> demand = {"LSD", "MSD", "HSD", "VSD"};
    vector<int> reqs = NetworkRequests();

    for (auto d : demand)
    {
        for (auto r : reqs)
        {
            CreateRequestFile(d, r);
        }
    }

    cout << "Finished generating requests.";
}

int main()
{
    RequestGenerator();
}