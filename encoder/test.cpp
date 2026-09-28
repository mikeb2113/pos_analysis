#include "encoder.hpp"
#include <iostream>
#include <bitset>
#include <string>
#include <vector>
#include <stringzilla/memory.h>
using namespace std;
int main() {
    encoder code;

    std::string terminal_input;

    sz::string_view example = "The USSR";
    std::vector<std::bitset<64>> target = 
    code.generate_encoding(example);

    std::cout << "Input a string to search by: ";
    std::getline(std::cin, terminal_input);

    sz::string_view input(terminal_input);

    std::vector<std::bitset<64>> encoding =
        code.generate_encoding(input);

    for (const auto& byte : encoding) {
        std::cout << byte << '\n';
    }

    std::cout << "equality check: " << code.equals(encoding, target) << "\n";
    std::cout << "size check: " << "\n" << code.smaller(encoding,target) << "\n";
    code.presence(encoding,target);
    return 0;
}