#include <bits/stdc++.h>

/**
 * @brief TreeInputRequestBlock class handles request inputs.
 *
 */
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