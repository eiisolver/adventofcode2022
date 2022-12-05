#include <iostream>
#include <fstream>
#include <list>
#include <vector>

using namespace std;

struct Move {
    int fr, to, n;
};

int main()
{
    ifstream f("5_input.txt");
    list<string> stackStrings;
    vector<Move> moves;
    string s;

    while (getline(f, s)) {
        if (s[1] == '1') {
            getline(f, s);
            break;
        }
        stackStrings.push_front(s);
    }
    int n = (stackStrings.front().size() + 1) / 4;
    Move m;
    while (f >> s >> m.n >> s >> m.fr >> s >> m.to) {
        moves.push_back(m);
    }
    vector<vector<char>> originalStack(n);
    for (auto &line : stackStrings) {
        for (int i = 0; i < n; ++i) {
            char c = line[1 + 4*i];
            if (c != ' ') {
                originalStack[i].push_back(c);
            }
        }
    }
    for (int part = 1; part <= 2; ++part) {
        auto stack = originalStack;
        for (auto &m : moves) {
            auto &src = stack[m.fr - 1];
            auto &dest = stack[m.to - 1];
            if (part == 1) {
                for (int i = 0; i < m.n; ++i) {
                    dest.push_back(src.back());
                    src.pop_back();
                }
            } else {
                auto ix = src.size() - m.n;
                dest.insert(dest.end(), make_move_iterator(src.begin() + ix),
                            make_move_iterator(src.end()));
                src.erase(src.begin() + ix, src.end());
            }
        }
        cout << "Part " << part << ": ";
        for (auto &v: stack) {
            cout << v.back();
        }
        cout << "\n";
    }
}
