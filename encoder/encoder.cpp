#include "encoder.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
encoder::encoder
(

)
    :
    DET{{std::byte{0},"a"}, {std::byte{1},"an"}, {std::byte{2},"that"}, {std::byte{3},"the"}, {std::byte{4},"these"}, {std::byte{5},"this"}, {std::byte{6},"those"}},
    PREP{{std::byte{0},"at"}, {std::byte{1},"by"}, {std::byte{2},"for"}, {std::byte{3},"from"}, {std::byte{4},"in"}, {std::byte{5},"into"}, {std::byte{6},"of"}, {std::byte{7},"on"}, {std::byte{8},"onto"}, {std::byte{9},"over"}, {std::byte{10},"to"}, {std::byte{11},"under"}, {std::byte{12},"with"}},
    CONJ{{std::byte{0},"and"}, {std::byte{1},"but"}, {std::byte{2},"or"}},
    COMP{{std::byte{0},"that"}, {std::byte{1},"which"}, {std::byte{2},"who"}, {std::byte{3},"whom"}},
    MOD{{std::byte{0},"can"}, {std::byte{1},"could"}, {std::byte{2},"may"}, {std::byte{3},"might"}, {std::byte{4},"must"}, {std::byte{5},"shall"}, {std::byte{6},"should"}, {std::byte{7},"will"}, {std::byte{8},"would"}},
    AUX{{std::byte{0},"am"}, {std::byte{1},"are"}, {std::byte{2},"be"}, {std::byte{3},"been"}, {std::byte{4},"being"}, {std::byte{5},"did"}, {std::byte{6},"do"}, {std::byte{7},"does"}, {std::byte{8},"had"}, {std::byte{9},"has"}, {std::byte{10},"have"}, {std::byte{11},"is"}, {std::byte{12},"was"}, {std::byte{13},"were"}},
    EXT_DET{{std::byte{0},"a"}, {std::byte{1},"an"}, {std::byte{2},"certain"}, {std::byte{3},"one"}, {std::byte{4},"some"}, {std::byte{5},"somebody"}, {std::byte{6},"someone"}, {std::byte{7},"something"}, {std::byte{8},"somewhere"}},
    UNI_DET{{std::byte{0},"all"}, {std::byte{1},"any"}, {std::byte{2},"each"}, {std::byte{3},"every"}, {std::byte{4},"whatever"}, {std::byte{5},"whichever"}, {std::byte{6},"whoever"}},
    NEG_QUANT{{std::byte{0},"never"}, {std::byte{1},"no"}, {std::byte{2},"nobody"}, {std::byte{3},"none"}, {std::byte{4},"noone"}, {std::byte{5},"nothing"}, {std::byte{6},"nowhere"}, {std::byte{7},"no-one"}},

    MISC{},

    MAP{std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}},
    
    pos_dict{
        {"the", 1 << 0}, 
        {"a", 1 << 0 | 1 << 6}, 
        {"an", 1 << 0 | 1 << 6}, 
        {"this", 1 << 0}, 
        {"that", 1 << 0 | 1 << 3}, 
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

        {"that", 1 << 3 | 1 << 0}, 
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

        {"a", 1 << 6 | 1 << 0}, 
        {"an", 1 << 6 | 1 << 0},
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

    std::byte encoder::POS_to_byte(std::string& pos){
        auto it = pos_dict.find()
    }

    sz::string encoder::find_word(std::byte){
        int length = 
    }

    bool encoder::in_lib(sz::string_view& input) {
        return pos_dict.find(input) != pos_dict.end();
    }
/*
if(det):
    return 1
if(prep)
    return 2

    int main(){
        encoder code = encoder();
        for(int i = 0; i < code.DET.size(); i++){
            std::byte key = std::byte(i);
            std::string value = code.DET[key];
            std::cout << value << "\n";
        }
        return 0;
    }
*/

