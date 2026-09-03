#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog";
    int instruction_counter = 0;
    int offset_placeholder = 15;
    std::byte sentence_information_builder;
    //std::vector<std::byte> bits;
    std::array<std::byte,8> bits{std::byte(0)};
    int idx = 0;
    for(auto word : input.split(" ")){
        instruction_counter++;
        if(code.in_lib(word)){
            std::cout << "A word was found in the dictionary!" << "\n";
            std::cout << word << "\n";

            std::cout <<"bit mask: " << code.find_word(word) << "\n";
            uint16_t bitshift = code.find_word(word);
            std::byte bytes = code.search_word(bitshift,word);
            bits[idx++] = bytes;
            std::cout << "binary: "
                << std::bitset<8>(std::to_integer<unsigned int>(bytes))
                << '\n';
        }
        else{
            bits[idx++] = std::byte(0);
        }
    }
    std::cout << "instruction num before byte builder:" << instruction_counter << "\n";

    std::byte instruction_number = std::byte(instruction_counter);

    ByteBuilder byteBuilder(instruction_counter,bits);
    return 0;
}