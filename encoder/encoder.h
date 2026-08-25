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
    std::map<std::string,std::byte> DET = 
    {{"the",std::byte{0}}, {"a",std::byte{1}}, {"an",std::byte{2}}, {"this",std::byte{3}}, {"that",std::byte{4}}, {"these",std::byte{5}}, {"those",std::byte{6}}};
    std::map<std::string,std::byte> PREP = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}, std::byte{9}, std::byte{10}, std::byte{11}, std::byte{12}};
    std::map<std::string,std::byte> CONJ = 
    {std::byte{0}, std::byte{1}, std::byte{2}};
    std::map<std::string,std::byte> COMP = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}};
    std::map<std::string,std::byte> MOD = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};
    std::map<std::string,std::byte> AUX = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}, std::byte{9}, std::byte{10}, std::byte{11}, std::byte{12}, std::byte{13}};
    std::map<std::string,std::byte> EXT_DET = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};
    std::map<std::string,std::byte> UNI_DET = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}};
    std::map<std::string,std::byte> NEG_QUANT = 
    {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}};    std::array<std::byte,9> MAP = {std::byte{0}, std::byte{1}, std::byte{2}, std::byte{3}, std::byte{4}, std::byte{5}, std::byte{6}, std::byte{7}, std::byte{8}};
    private:
};

#endif