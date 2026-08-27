#ifndef ENCODER_H
#define ENCODER_H
#include <stdio.h>
#include <array>
#include <map>
#include <unordered_set>
#include <string>
#include <stringzilla/stringzilla.hpp>
namespace sz = ashvardanian::stringzilla;
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
    
    std::map<std::byte,sz::string> DET;
    std::map<std::byte,sz::string> PREP;
    std::map<std::byte,sz::string> CONJ;
    std::map<std::byte,sz::string> COMP;
    std::map<std::byte,sz::string> MOD;
    std::map<std::byte,sz::string> AUX;
    std::map<std::byte,sz::string> EXT_DET;
    std::map<std::byte,sz::string> UNI_DET;
    std::map<std::byte,sz::string> NEG_QUANT;    
    std::unordered_set<sz::string_view, uint16_t> pos_dict;
    std::unordered_set<sz::string> MISC;

    std::array<std::byte,9> MAP;

    std::unordered_set<std::string> pos_names;

    bool in_lib(sz::string_view& input);
    sz::string encoder::find_word(std::byte);
    std::byte encoder::POS_to_byte(std::string& pos);

    enum class POS : uint16_t {
        DET       = 1 << 0,
        PREP      = 1 << 1,
        CONJ      = 1 << 2,
        COMP      = 1 << 3,
        MOD       = 1 << 4,
        AUX       = 1 << 5,
        EXT_DET   = 1 << 6,
        UNI_DET   = 1 << 7,
        NEG_QUANT = 1 << 8
    };

    private:
};

#endif