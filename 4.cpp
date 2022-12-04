#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    ifstream f("4_input.txt");
    int a, b, c, d;
    char h;
    int overlap = 0;
    int full_overlap = 0;

    while (f >> a >> h >> b >> h >> c >> h >> d) {
        if (a <= d && c <= b) {
            ++overlap;
            if (a >= c || b >= d) {
                ++full_overlap;
            }
        }
    }
    cout << "Part 1: " << full_overlap << "\n";
    cout << "Part 2: " << overlap << "\n";
}
