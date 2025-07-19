#define BW 12.5

/**
 * @brief Function to find required frequency slots in a link
 *
 * @param demand in Gbps
 * @param distance in KM
 * @return int freq_slots
 */
int FindSlots(int demand, int distance)
{
    int SE = 1;
    if (distance <= 500)
        SE = 4;
    else if (distance <= 1000)
        SE = 3;
    else if (distance <= 2000)
        SE = 2;
    else
        SE = 1;

    int freq_slots = ceil(demand / (BW * SE));

    return freq_slots;
}
