#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog. Then the down howled";
    unsigned instruction_counter = 0;
    int offset_placeholder = 15;
    std::byte sentence_information_builder;
    //std::vector<std::byte> bits;
    std::array<std::byte,4> bits{std::byte(0)};
    unsigned idx = 0;
    std::array<std::bitset<4>,13> sentence_byte_array = 
        {
            std::bitset<4>(0)
        };
    bool in_NP = false;
    for(auto word : input.split(" ")){
        instruction_counter++;
        if(code.in_lib(word)){
            in_NP = false;
            std::cout << "A word was found in the dictionary!" << "\n";
            std::cout << word << "\n";

            std::cout <<"bit mask: " << code.find_word(word) << "\n";
            uint16_t bitshift = code.find_word(word);
            std::byte bytes = code.search_word(bitshift,word);
            bits[idx++] = bytes;
            //flat -1
            sentence_byte_array[13-idx-1] = std::bitset<4>(int(bytes));
            std::cout << "binary: "
                << std::bitset<4>(std::to_integer<unsigned int>(bytes))
                << '\n';
        }
        else{
            if(!in_NP){
                sentence_byte_array[13-idx-1] = std::bitset<4>(9);
            }
            in_NP = true;
            bits[idx++] = std::byte(0);
        }
    }
    std::cout << "instruction num before byte builder:" << instruction_counter << "\n";

    std::byte instruction_number = std::byte(instruction_counter);

    //ByteBuilder byteBuilder(instruction_counter,bits);
    ByteBuilder byteBuilder(instruction_counter,sentence_byte_array);
    return 0;
}