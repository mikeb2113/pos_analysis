#include "encoder.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
encoder::encoder
(

)
    :
    DET{{"a", std::byte{0}}, {"an", std::byte{1}}, {"that", std::byte{2}}, {"the", std::byte{3}}, {"these", std::byte{4}}, {"this", std::byte{5}}, {"those", std::byte{6}}},
    PREP{{"at", std::byte{0}}, {"by", std::byte{1}}, {"for", std::byte{2}}, {"from", std::byte{3}}, {"in", std::byte{4}}, {"into", std::byte{5}}, {"of", std::byte{6}}, {"on", std::byte{7}}, {"onto", std::byte{8}}, {"over", std::byte{9}}, {"to", std::byte{10}}, {"under", std::byte{11}}, {"with", std::byte{12}}},
    CONJ{{"and", std::byte{0}}, {"but", std::byte{1}}, {"or", std::byte{2}}},
    COMP{{"that", std::byte{0}}, {"which", std::byte{1}}, {"who", std::byte{2}}, {"whom", std::byte{3}}},
    MOD{{"can", std::byte{0}}, {"could", std::byte{1}}, {"may", std::byte{2}}, {"might", std::byte{3}}, {"must", std::byte{4}}, {"shall", std::byte{5}}, {"should", std::byte{6}}, {"will", std::byte{7}}, {"would", std::byte{8}}},
    AUX{{"am", std::byte{0}}, {"are", std::byte{1}}, {"be", std::byte{2}}, {"been", std::byte{3}}, {"being", std::byte{4}}, {"did", std::byte{5}}, {"do", std::byte{6}}, {"does", std::byte{7}}, {"had", std::byte{8}}, {"has", std::byte{9}}, {"have", std::byte{10}}, {"is", std::byte{11}}, {"was", std::byte{12}}, {"were", std::byte{13}}},
    EXT_DET{{"a", std::byte{0}}, {"an", std::byte{1}}, {"certain", std::byte{2}}, {"one", std::byte{3}}, {"some", std::byte{4}}, {"somebody", std::byte{5}}, {"someone", std::byte{6}}, {"something", std::byte{7}}, {"somewhere", std::byte{8}}},
    UNI_DET{{"all", std::byte{0}}, {"any", std::byte{1}}, {"each", std::byte{2}}, {"every", std::byte{3}}, {"whatever", std::byte{4}}, {"whichever", std::byte{5}}, {"whoever", std::byte{6}}},
    NEG_QUANT{{"never", std::byte{0}}, {"no", std::byte{1}}, {"nobody", std::byte{2}}, {"none", std::byte{3}}, {"noone", std::byte{4}}, {"nothing", std::byte{5}}, {"nowhere", std::byte{6}}, {"no-one", std::byte{7}}},

    MISC{},

    MAP
        {
            {std::byte{1}, DET},
            {std::byte{2}, PREP},
            {std::byte{3}, CONJ},
            {std::byte{4}, COMP},
            {std::byte{5}, MOD},
            {std::byte{6}, AUX},
            {std::byte{7}, EXT_DET},
            {std::byte{8}, UNI_DET},
            {std::byte{9}, NEG_QUANT}
            //{std::byte{9}, MISC}
        },
    
    pos_dict{
        //Ensure that each POS has bit shifts to identify them!
        {"the", 1 << 1}, 
        {"a", (1 << 1) | (1 << 7)}, 
        {"an", (1 << 1) | (1 << 7)}, 
        {"this", 1 << 1}, 
        {"that", (1 << 1) | (1 << 4)}, 
        {"these", 1 << 1}, 
        {"those", 1 << 1},//id 0-6

        {"of", 1 << 2}, 
        {"in", 1 << 2}, 
        {"on", 1 << 2}, 
        {"at", 1 << 2}, 
        {"over", 1 << 2}, 
        {"under", 1 << 2},
        {"with", 1 << 2}, 
        {"by", 1 << 2}, 
        {"for", 1 << 2}, 
        {"to", 1 << 2}, 
        {"from", 1 << 2}, 
        {"into", 1 << 2}, 
        {"onto", 1 << 2},//id 7-13

        {"and", 1 << 3}, 
        {"or", 1 << 3}, 
        {"but", 1 << 3},//id 14-16

        {"which", 1 << 4}, 
        {"who", 1 << 4}, 
        {"whom", 1 << 4},//id 17-20

        {"can", 1 << 5}, 
        {"could", 1 << 5}, 
        {"will", 1 << 5}, 
        {"would", 1 << 5}, 
        {"shall", 1 << 5}, 
        {"should", 1 << 5}, 
        {"may", 1 << 5}, 
        {"might", 1 << 5}, 
        {"must", 1 << 5},//id 21-29

        {"be", 1 << 6}, 
        {"am", 1 << 6}, 
        {"is", 1 << 6}, 
        {"are", 1 << 6}, 
        {"was", 1 << 6}, 
        {"were", 1 << 6}, 
        {"been", 1 << 6}, 
        {"being", 1 << 6},
        {"have", 1 << 6}, 
        {"has", 1 << 6}, 
        {"had", 1 << 6}, 
        {"do", 1 << 6}, 
        {"does", 1 << 6}, 
        {"did", 1 << 6},//id 30-43

        {"some", 1 << 7},
        {"one", 1 << 7},
        {"somebody", 1 << 7}, 
        {"someone", 1 << 7}, 
        {"something", 1 << 7}, 
        {"somewhere", 1 << 7},
        {"certain", 1 << 7},//id 44-52

        {"every", 1 << 8}, 
        {"each", 1 << 8},
        {"all", 1 << 8}, 
        {"any", 1 << 8},
        {"whoever", 1 << 8}, 
        {"whatever", 1 << 8}, 
        {"whichever", 1 << 8},//id 53-59

        {"no", 1 << 9},
        {"nobody", 1 << 9}, 
        {"noone", 1 << 9}, 
        {"no-one", 1 << 9}, 
        {"none", 1 << 9},
        {"nothing", 1 << 9},
        {"nowhere", 1 << 9},
        {"never", 1 << 9}//id 60-67
    },

    pos_names{
        "DET",
        "PREP",
        "CONJ",
        "COMP",
        "MOD",
        "AUX",
        "EXT_DET",
        "UNI_DET",
        "NEG_QUANT",

        "MISC"
    }
{

};

    int encoder::get_clause_count(sz::string_view& input){
        bool in_NP = false;
        int clause_count = 0;
        for(auto word : input.split(" ")){
            if(in_lib(word)){
                clause_count++;
                in_NP = false;
            }

            else{
                if(!in_NP){
                    clause_count++;
                    in_NP = true;
                }
            }
        }
        return clause_count;
    }

    std::size_t encoder::get_storage_blocks(sz::string_view& input){
        int clause_count = get_clause_count(input);
        std::size_t blocks = 1;
        while(clause_count >= 13){
            clause_count = clause_count - 13;
            blocks++;
        }
        return blocks;
    }

    uint16_t encoder::find_word(sz::string_view& input){
        auto it = pos_dict.find(input);

        if(it == pos_dict.end()){
            return 0;
        }
        return it->second; //This finds the byte code for the given word in the list.
    }

    std::vector<std::bitset<64>> encoder::generate_encoding(sz::string_view& input){
        int blocks = get_storage_blocks(input);
        std::vector<std::bitset<64>> array(blocks);
    }

    std::array<std::bitset<4>,13> encoder::generate_segment(sz::string_view& input, sz::string_view prefix, int blocks = 1, int iteration = 0, int instruction_counter = 0, bool in_NP = false){ 
        //NOTE: The absolute MAX instruction count is 13 when the memory block is non-terminating.
        //Otherwise, the MAX instruction count is 12, because the terminator instruction takes one byte.

        std::array<std::bitset<4>,13> sentence_byte_array = 
            {
                std::bitset<4>(0)
            };
        int idx = 0;
        sz::string prefix_builder;

        if(iteration< blocks)
        {
            while(idx<13)
            {
                for(auto word : input.split(" "))
                {
                    prefix_builder += word;
                    uint16_t bitshift = find_word(word);
                    std::byte bytes = std::byte(std::log2((int(bitshift))));
                    //std::cout << "word: " << word << "\n" << "POS index: " << int(bytes) << "\n";

                    if(in_lib(word))
                    {
                        instruction_counter++;
                        in_NP = false;

                        //std::byte bytes = code.search_word_in_known_lib(bitshift,word);

                        sentence_byte_array[idx] = std::bitset<4>(int(bytes));
                        //std::cout << "entry size: " << code.MAP[bytes].size() << "\n";
                        idx++;
                    }

                    else
                    {
                        if(!in_NP)
                        {
                            //std::cout << "[NP]";
                            instruction_counter++;
                            sentence_byte_array[idx] = std::bitset<4>(10); //This word is a part of a Noun Phrase - mark it as such!
                            in_NP = true;
                            idx++;
                        }
                    }
                }
            }
        }
        else if (iteration==blocks)
        {
            while(idx<12)
            {
                for(auto word : input.split(" "))
                {
                    uint16_t bitshift = find_word(word);
                    std::byte bytes = std::byte(std::log2((int(bitshift))));
                    //std::cout << "word: " << word << "\n" << "POS index: " << int(bytes) << "\n";

                    if(in_lib(word))
                    {
                        instruction_counter++;
                        in_NP = false;

                        //std::byte bytes = code.search_word_in_known_lib(bitshift,word);

                        sentence_byte_array[idx] = std::bitset<4>(int(bytes));
                        //std::cout << "entry size: " << code.MAP[bytes].size() << "\n";
                        idx++;
                    }

                    else
                    {
                        if(!in_NP)
                        {
                            //std::cout << "[NP]";
                            instruction_counter++;
                            sentence_byte_array[idx] = std::bitset<4>(10); //This word is a part of a Noun Phrase - mark it as such!
                            in_NP = true;
                            idx++;
                        }
                    }
                }
            } 
            sentence_byte_array[idx] = std::bitset<4>(11);
        }

    }

    bool encoder::in_lib(sz::string_view& input) {
        return pos_dict.find(input) != pos_dict.end();
    }

    std::byte encoder::search_word_in_known_lib(int bitshift,sz::string_view word){
        std::string builder;
        for(char c : word){
            if(c >= 'A' && c <= 'Z'){
                c += 'a' - 'A';
            }
            builder += c;
        }
        if(bitshift & 1 << 0){
            std::byte word_byte = DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 1){
            std::byte word_byte = PREP[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 2){
            std::byte word_byte = CONJ[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 3){
            std::byte word_byte = COMP[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 4){
            std::byte word_byte = MOD[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 5){
            std::byte word_byte = AUX[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 6){
            std::byte word_byte = EXT_DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 7){
            std::byte word_byte = UNI_DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 8){
            std::byte word_byte = NEG_QUANT[builder];
            return word_byte;
        }
        return std::byte(64);
    }