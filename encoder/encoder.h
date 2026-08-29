#ifndef ENCODER_H
#define ENCODER_H
#include <stdio.h>
#include <array>
#include <map>
#include <unordered_set>
#include <unordered_map>
#include <string>
#include <stringzilla/stringzilla.hpp>
namespace sz = ashvardanian::stringzilla;
class encoder{
    public:
    encoder
    (

    );
    
    std::map<std::byte,sz::string> DET;
    std::map<std::byte,sz::string> PREP;
    std::map<std::byte,sz::string> CONJ;
    std::map<std::byte,sz::string> COMP;
    std::map<std::byte,sz::string> MOD;
    std::map<std::byte,sz::string> AUX;
    std::map<std::byte,sz::string> EXT_DET;
    std::map<std::byte,sz::string> UNI_DET;
    std::map<std::byte,sz::string> NEG_QUANT;    
    std::unordered_map<sz::string_view, uint16_t> pos_dict;
    std::unordered_set<sz::string> MISC;

    std::array<std::byte,9> MAP;

    std::unordered_set<std::string> pos_names;

    bool in_lib(sz::string_view& input);
    uint16_t find_word(sz::string_view& input);
    std::byte POS_to_byte(std::string& pos);
    std::byte search_word(int bitshift,sz::string_view word);

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