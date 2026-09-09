#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog Then the down howled";
    unsigned instruction_counter = 0;
    int offset_placeholder = 15;
    std::byte sentence_information_builder;
    //std::vector<std::byte> bits;
    //std::array<std::byte,4> bits{std::byte(0)};
    unsigned idx = 0;
    std::array<std::bitset<4>,13> sentence_byte_array = 
        {
            std::bitset<4>(0)
        };
    bool in_NP = false;
    for(auto word : input.split(" ")){

        uint16_t bitshift = code.find_word(word);
        std::byte bytes = std::byte(int(bitshift)-1);
        std::cout << "word: " << word << "\n" << "POS index: " << int(bytes) << "\n";

        if(code.in_lib(word)){
            instruction_counter++;
            in_NP = false;
            //std::cout << "A word was found in the dictionary!" << "\n";
            //std::cout << word << "\n";

            //std::byte bytes = code.search_word_in_known_lib(bitshift,word);

            //bits[idx++] = bytes;
            //flat -1
            sentence_byte_array[idx] = std::bitset<4>(int(bytes));
            std::cout << "entry size: " << code.MAP[bytes].size() << "\n";
            //std::cout << "binary: "
            //    << std::bitset<4>(std::to_integer<unsigned int>(bytes))
            //    << '\n';
            idx++;
        }
        else{
            //uint16_t bitshift = code.find_word(word);
            //std::byte bytes = code.search_word(bitshift,word);
            //std::cout << "Word is not in dictionary!" << "\n" << "value: " << int(bytes) << "\n";
            if(!in_NP){
                std::cout << "[NP]";
                instruction_counter++;
                sentence_byte_array[idx] = std::bitset<4>(9); //This word is a part of a Noun Phrase - mark it as such!
                in_NP = true;
                idx++;
            }
            //bits[idx++] = std::byte(0);
        }
    }
    std::cout << "instruction num before byte builder:" << instruction_counter << "\n";

    std::byte instruction_number = std::byte(instruction_counter);

    //ByteBuilder byteBuilder(instruction_counter,bits);
    ByteBuilder byteBuilder(instruction_counter,sentence_byte_array);
    return 0;
}

/*
0111

0000
0000

0000
1001
0000
0000
0000
0001
0000
1001
0000
0000
0000
1001
0000
*/