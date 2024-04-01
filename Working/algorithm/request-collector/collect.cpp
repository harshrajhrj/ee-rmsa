#include <bits/stdc++.h>
#include <filesystem>
namespace fs = std::filesystem;
#include "request_class.cpp"

/**
 * @brief Collect requests from a given directory
 *
 * @return vector<TreeInputRequestBlock>
 */
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