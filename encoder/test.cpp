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

    std::array<std::vector<std::bitset<64>>,2> target = 
    code.generate_encoding(example,"target");

    std::cout << "Input a string to search by: ";
    std::getline(std::cin, terminal_input);

    sz::string_view input(terminal_input);

    std::array<std::vector<std::bitset<64>>,2> encoding =
        code.generate_encoding(input,"terminal");
    
    std::cout << "input: " << "\n";
    for(int i = 0; i < encoding.size(); i++){
        if(i == 0){
            std::cout << "part of speech encoding: " << "\n";
        } else{
            std::cout << "concrete encoding: " << "\n";
        }
        for (const auto& byte : encoding[i]) {
            std::cout << byte << '\n';
        }
        std::cout << "\n";
    }

    std::array<std::string,2> sources = {"terminal","target"};

    std::cout << "target: " << "\n";
    for(int i = 0; i < target.size(); i++){
        if(i == 0){
            std::cout << "part of speech encoding: " << "\n";
        } else{
            std::cout << "concrete encoding: " << "\n";
        }
        for (const auto& byte : target[i]) {
            std::cout << byte << '\n';
        }
        std::cout << "\n";
    }

    std::cout << "equality check: " << code.equals(encoding[0], target[0]) << "\n";
    //std::cout << "size check: " << "\n" << code.smaller(encoding,target) << "\n";
    std::vector<std::array<int,2>> presence = code.presence(encoding[0],target[0]);

    //std::string source = "data.bin";
    for(auto source : sources){
        if(code.read_from_binary(source,0) == 1){
            std::cout << "error: could not read file from memory! " << "\n";
        } else{
            std::cout << "file successfully read from memory!" << "\n";
        }
    }



    //std::cout << "indexing: " << "\n";
    /*
    for(int i = 0; i < presence.size(); i++){
        std::cout << "index: [" << presence[i][0] << ", " << presence[i][1] << "]" << "\n";
    }
    */
    //std::cout << "integer value: " << code.bitset_to_int(encoding[0]) << "\n";
    return 0;
}