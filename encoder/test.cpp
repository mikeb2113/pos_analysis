#include "encoder.h"
#include <iostream>
#include <bitset>
#include <stringzilla/memory.h>
#include <cmath>
int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog Then the down howled";
    sz::string_view input2 = "the of and which can be some every no";
    sz::string_view input3 = "Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo Buffalo ";
    sz::string_view input4 = "I think that we should have spaghetti, which is delicious, for supper, and we should have garlic bread too, because I really want to have spaghetti and garlic bread.";
    unsigned instruction_counter = 0;
    int offset_placeholder = 15;
    std::byte sentence_information_builder;
    unsigned idx = 0;
    std::array<std::bitset<4>,13> sentence_byte_array = 
        {
            std::bitset<4>(0)
        };
    bool in_NP = false;
    //We may have a max of 13 instructions. Note that at some point, we must include an ending instruction!
    //Before analysis, we must know how many instructions are present
    //we will know how much space to allocate using the following mechanism:
    //recursively do: instruction_count - 13 until instruction count is < 13 (Not equal to - we need to ending byte!)
    //The amount of subtractions needed is the amount of 64-bit spaces required.
    //For input4, we will need 2 64-bit spaces.
    //int clause_count = code.get_clause_count(input4);
    int blocks = code.get_storage_blocks(input4);
    std::cout << "Storage required: " << blocks << "\n";
    for(auto word : input4.split(" ")){

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
    sentence_byte_array[idx] = std::bitset<4>(11);
    idx++;
    std::cout << "instruction num before byte builder:" << instruction_counter << "\n";

    std::byte instruction_number = std::byte(instruction_counter);

    ByteBuilder byteBuilder(instruction_counter,sentence_byte_array);
    return 0;
}

/*
0111

0000
0000

0001
1010
0010
0001
1010
0001
1010
1011
0000
0000
0000
0000
0000
*/