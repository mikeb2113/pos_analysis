#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
#include <cmath>
int main(){
    encoder code;
    sz::string_view dog = "The quick brown fox jumped over the lazy dog";
    sz::string_view input = "The quick brown fox jumped over the lazy dog Then the down howled";
    sz::string_view input2 = "the of and which can be some every no";
    sz::string_view input3 = "Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo ";
    sz::string_view input4 = "I think that we should have spaghetti, which is delicious, for supper, and we should have garlic bread too, because I really want to have spaghetti and garlic bread.";

    std::vector<std::bitset<64>> encoding = code.generate_encoding(dog);
        std::cout << "printing byte representation..." << "\n";
        for(auto byte : encoding){
            std::cout << byte;
        }
        std::cout << "\n";
    return 0;
}