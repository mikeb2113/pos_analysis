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

    MAP{std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}},
    
    pos_dict{
        "the", "a", "an", "this", "that", "these", "those","of", "in", "on", "at", "over", "under", 
        "with", "by", "for", "to", "from", "into", "onto","and", "or", "but","that", "which", "who", 
        "whom","can", "could", "will", "would", "shall", "should", "may", "might", "must",
        "be", "am", "is", "are", "was", "were", "been", "being","have", "has", "had",
        "do", "does", "did","a", "an","some","one","somebody", "someone", "something", "somewhere",
        "certain","every", "each","all", "any","whoever", "whatever", "whichever","no",
        "nobody", "noone", "no-one", "none","nothing","nowhere","never"
    }
{

};
    bool encoder::in_lib(sz::string_view& input) {
        return pos_dict.find(input) != pos_dict.end();
    }
/*
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

