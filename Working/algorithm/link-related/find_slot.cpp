#include <bits/stdc++.h>
using namespace std;

void FindSlots()
{
    vector<int> v{4, 5, 6, 6, 444};

    cout << *max_element(v.begin(), v.end());
}

int main() {
    FindSlots();
}