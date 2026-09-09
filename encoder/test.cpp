#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
#include <cmath>
int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog Then the down howled";
    sz::string_view input2 = "the of and which can be some every no";
    unsigned instruction_counter = 0;
    int offset_placeholder = 15;
    std::byte sentence_information_builder;
    unsigned idx = 0;
    std::array<std::bitset<4>,13> sentence_byte_array = 
        {
            std::bitset<4>(0)
        };
    bool in_NP = false;
    for(auto word : input.split(" ")){

        uint16_t bitshift = code.find_word(word);
        std::byte bytes = std::byte(std::log2((int(bitshift))));
        std::cout << "word: " << word << "\n" << "POS index: " << int(bytes) << "\n";

        if(code.in_lib(word)){
            instruction_counter++;
            in_NP = false;

            //std::byte bytes = code.search_word_in_known_lib(bitshift,word);

            sentence_byte_array[idx] = std::bitset<4>(int(bytes));
            std::cout << "entry size: " << code.MAP[bytes].size() << "\n";
            idx++;
        }

        else{
            if(!in_NP){
                std::cout << "[NP]";
                instruction_counter++;
                sentence_byte_array[idx] = std::bitset<4>(10); //This word is a part of a Noun Phrase - mark it as such!
                in_NP = true;
                idx++;
            }
        }
    }
    std::cout << "instruction num before byte builder:" << instruction_counter << "\n";

    std::byte instruction_number = std::byte(instruction_counter);

    ByteBuilder byteBuilder(instruction_counter,sentence_byte_array);
    return 0;
}

/*
1001

0000
0000

0001
0010
0011
0100
0101
0110
0111
1000
1001
0000
0000
0000
0000
*/