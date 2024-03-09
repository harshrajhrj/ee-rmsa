#include <bits/stdc++.h>
#include <filesystem>
namespace fs = std::filesystem;
#include "../adjacency-list/build_adjacency_list.cpp"

using namespace std;

void BuildTree()
{
    // unordered_map<int, Node *> ControlBlock = GenerateAdjacencyList();

    string path = "../../requests";

    for (const auto &entry : fs::directory_iterator(path))
    {
        // cout << entry.path() << endl;
        
        fstream file(entry.path(), ios::in);
        if (file)
        {
            string new_line;
            while (!file.eof())
            {
                getline(file, new_line);
                cout << new_line << endl;
            }
        }
        file.close();
    }
}

int main()
{
    BuildTree();
}