#ifndef ENCODER_H
#define ENCODER_H
#include <stdio.h>
#include <array>
#include <map>
class encoder{
    public:
    encoder
    (

    );
    /*
    std::array<std::byte,7> DET = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}};
    std::array<std::byte,13> PREP = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}, std::byte{9}, std::byte{10}, std::byte{11}, std::byte{12}};
    std::array<std::byte,3> CONJ = {std::byte{0}, std::byte{1}, std::byte{2}};
    std::array<std::byte,4> COMP = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}};
    std::array<std::byte,9> MOD = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};
    std::array<std::byte,14> AUX = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}, std::byte{9}, std::byte{10}, std::byte{11}, std::byte{12}, std::byte{13}};
    std::array<std::byte,9> EXT_DET = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};
    std::array<std::byte,7> UNI_DET = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}};
    std::array<std::byte,8> NEG_QUANT = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}};
*/
    std::map<std::byte,std::string> DET = 
    {{std::byte{0},"a"}, {std::byte{1},"an"}, {std::byte{2},"that"}, {std::byte{3},"the"}, {std::byte{4},"these"}, {std::byte{5},"this"}, {std::byte{6},"those"}};
    std::map<std::byte,std::string> PREP = 
    {{std::byte{0},"at"}, {std::byte{1},"by"}, {std::byte{2},"for"}, {std::byte{3},"from"}, {std::byte{4},"in"}, {std::byte{5},"into"}, {std::byte{6},"of"}, {std::byte{7},"on"}, {std::byte{8},"onto"}, {std::byte{9},"over"}, {std::byte{10},"to"}, {std::byte{11},"under"}, {std::byte{12},"with"}};
    std::map<std::byte,std::string> CONJ = 
    {{std::byte{0},"and"}, {std::byte{1},"but"}, {std::byte{2},"or"}};
    std::map<std::byte,std::string> COMP = 
    {{std::byte{0},"that"}, {std::byte{1},"which"}, {std::byte{2},"who"}, {std::byte{3},"whom"}};
    std::map<std::byte,std::string> MOD = 
    {{std::byte{0},"can"}, {std::byte{1},"could"}, {std::byte{2},"may"}, {std::byte{3},"might"}, {std::byte{4},"must"}, {std::byte{5},"shall"}, {std::byte{6},"should"}, {std::byte{7},"will"}, {std::byte{8},"would"}};

    std::map<std::byte,std::string> AUX = 
    {{std::byte{0}}, {std::byte{1}}, {std::byte{2}}, {std::byte{3}}, {std::byte{4}}, {std::byte{5}}, {std::byte{6}}, {std::byte{7}}, {std::byte{8}}, {std::byte{9}}, {std::byte{10}}, {std::byte{11}}, {std::byte{12}}, {std::byte{13}}};

    std::map<std::byte,std::string> EXT_DET = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};

    std::map<std::byte,std::string> UNI_DET = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}};

    std::map<std::byte,std::string> NEG_QUANT = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}};    std::array<std::byte,9> MAP = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};
    private:
};

#endif