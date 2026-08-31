#include "encoder.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
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

    MAP{std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}},
    
    pos_dict{
        //Ensure that each POS has bit shifts to identify them!
        {"the", 1 << 0}, 
        {"a", (1 << 0) | (1 << 6)}, 
        {"an", (1 << 0) | (1 << 6)}, 
        {"this", 1 << 0}, 
        {"that", (1 << 0) | (1 << 3)}, 
        {"these", 1 << 0}, 
        {"those", 1 << 0},//id 0-6

        {"of", 1 << 1}, 
        {"in", 1 << 1}, 
        {"on", 1 << 1}, 
        {"at", 1 << 1}, 
        {"over", 1 << 1}, 
        {"under", 1 << 1},
        {"with", 1 << 1}, 
        {"by", 1 << 1}, 
        {"for", 1 << 1}, 
        {"to", 1 << 1}, 
        {"from", 1 << 1}, 
        {"into", 1 << 1}, 
        {"onto", 1 << 1},//id 7-13

        {"and", 1 << 2}, 
        {"or", 1 << 2}, 
        {"but", 1 << 2},//id 14-16

        {"which", 1 << 3}, 
        {"who", 1 << 3}, 
        {"whom", 1 << 3},//id 17-20

        {"can", 1 << 4}, 
        {"could", 1 << 4}, 
        {"will", 1 << 4}, 
        {"would", 1 << 4}, 
        {"shall", 1 << 4}, 
        {"should", 1 << 4}, 
        {"may", 1 << 4}, 
        {"might", 1 << 4}, 
        {"must", 1 << 4},//id 21-29

        {"be", 1 << 5}, 
        {"am", 1 << 5}, 
        {"is", 1 << 5}, 
        {"are", 1 << 5}, 
        {"was", 1 << 5}, 
        {"were", 1 << 5}, 
        {"been", 1 << 5}, 
        {"being", 1 << 5},
        {"have", 1 << 5}, 
        {"has", 1 << 5}, 
        {"had", 1 << 5}, 
        {"do", 1 << 5}, 
        {"does", 1 << 5}, 
        {"did", 1 << 5},//id 30-43

        {"some", 1 << 6},
        {"one", 1 << 6},
        {"somebody", 1 << 6}, 
        {"someone", 1 << 6}, 
        {"something", 1 << 6}, 
        {"somewhere", 1 << 6},
        {"certain", 1 << 6},//id 44-52

        {"every", 1 << 7}, 
        {"each", 1 << 7},
        {"all", 1 << 7}, 
        {"any", 1 << 7},
        {"whoever", 1 << 7}, 
        {"whatever", 1 << 7}, 
        {"whichever", 1 << 7},//id 53-59

        {"no", 1 << 8},
        {"nobody", 1 << 8}, 
        {"noone", 1 << 8}, 
        {"no-one", 1 << 8}, 
        {"none", 1 << 8},
        {"nothing", 1 << 8},
        {"nowhere", 1 << 8},
        {"never", 1 << 8}//id 60-67
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

    uint16_t encoder::find_word(sz::string_view& input){
        auto it = pos_dict.find(input);

        if(it == pos_dict.end()){
            return 0;
        }
        return it->second; //This finds the byte code for the given word in the list.
    }

    bool encoder::in_lib(sz::string_view& input) {
        return pos_dict.find(input) != pos_dict.end();
    }

    std::byte encoder::search_word(int bitshift,sz::string_view word){
        if(bitshift & 1 << 0){
            std::byte word_byte = DET[word];
            return word_byte;
        }
        else if(bitshift & 1 << 1){
            std::byte word_byte = PREP[word];
            return word_byte;
        }
        else if(bitshift & 1 << 2){
            std::byte word_byte = CONJ[word];
            return word_byte;
        }
        else if(bitshift & 1 << 3){
            std::byte word_byte = COMP[word];
            return word_byte;
        }
        else if(bitshift & 1 << 4){
            std::byte word_byte = MOD[word];
            return word_byte;
        }
        else if(bitshift & 1 << 5){
            std::byte word_byte = AUX[word];
            return word_byte;
        }
        else if(bitshift & 1 << 6){
            std::byte word_byte = EXT_DET[word];
            return word_byte;
        }
        else if(bitshift & 1 << 7){
            std::byte word_byte = UNI_DET[word];
            return word_byte;
        }
        else if(bitshift & 1 << 8){
            std::byte word_byte = NEG_QUANT[word];
            return word_byte;
        }
        return std::byte(64);
    }