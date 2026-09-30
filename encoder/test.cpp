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

    std::cout << "input: " << "\n";
    for (const auto& byte : encoding) {
        std::cout << byte << '\n';
    }
    std::cout << "target: " << "\n";
    for (const auto& byte : target) {
        std::cout << byte << '\n';
    }

    std::cout << "equality check: " << code.equals(encoding, target) << "\n";
    //std::cout << "size check: " << "\n" << code.smaller(encoding,target) << "\n";
    std::vector<std::array<int,2>> presence = code.presence(encoding,target);
    
    std::cout << "indexing: " << "\n";
    for(int i = 0; i < presence.size(); i++){
        std::cout << "index: [" << presence[i][0] << ", " << presence[i][1] << "]" << "\n";
    }
    
    //std::cout << "integer value: " << code.bitset_to_int(encoding[0]) << "\n";
    return 0;
}