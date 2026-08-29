#include "encoder.h"
#include <iostream>
#include <bitset>

int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog";
    for(auto word : input.split(" ")){
        if(code.in_lib(word)){
            std::cout << "A word was found in the dictionary!" << "\n";
            std::cout << word << "\n";
            std::cout <<"bit mask: " << code.find_word(word) << "\n";
            uint16_t bitshift = code.find_word(word);
            std::byte bytes = code.search_word(bitshift,word);
            std::cout << "binary: "
                << std::bitset<8>(std::to_integer<unsigned int>(bytes))
                << '\n';
        }
    }
    return 0;
}