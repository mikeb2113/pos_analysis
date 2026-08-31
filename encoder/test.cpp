#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog";
    int instruction_counter;
    int offset_placeholder = 1573;
    std::byte sentence_information_builder;
    std::vector<std::byte> bits;
    for(auto word : input.split(" ")){
        instruction_counter++;
        if(code.in_lib(word)){
            std::cout << "A word was found in the dictionary!" << "\n";
            std::cout << word << "\n";

            std::cout <<"bit mask: " << code.find_word(word) << "\n";
            uint16_t bitshift = code.find_word(word);
            std::byte bytes = code.search_word(bitshift,word);
            bits.push_back(bytes);
            std::cout << "binary: "
                << std::bitset<8>(std::to_integer<unsigned int>(bytes))
                << '\n';
        }
        else{
            bits.push_back(std::byte(0b11111111));
        }
    }

    std::byte instruction_number = std::byte(instruction_counter);

    ByteBuilder byteBuilder(instruction_counter,sentence_information_builder);
    return 0;
}