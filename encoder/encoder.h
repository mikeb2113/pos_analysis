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
struct CaseInsensitiveHash {
    std::size_t operator()(sz::string_view s) const noexcept {
        std::size_t hash = 0;

        for (unsigned char c : s) {
            if (c >= 'A' && c <= 'Z')
                c += 'a' - 'A';

            hash = hash * 31 + c;
        }

        return hash;
    }
};

struct CaseInsensitiveEqual {
    bool operator()(sz::string_view a, sz::string_view b) const noexcept {
        if (a.size() != b.size())
            return false;

        for (std::size_t i = 0; i < a.size(); ++i) {
            unsigned char ca = a[i];
            unsigned char cb = b[i];

            if (ca >= 'A' && ca <= 'Z')
                ca += 'a' - 'A';

            if (cb >= 'A' && cb <= 'Z')
                cb += 'a' - 'A';

            if (ca != cb)
                return false;
        }

        return true;
    }
};

struct ByteBuilder {

};

class encoder{
    public:
    encoder
    (

    );
    
    std::map<sz::string_view,std::byte> DET;
    std::map<sz::string_view,std::byte> PREP;
    std::map<sz::string_view,std::byte> CONJ;
    std::map<sz::string_view,std::byte> COMP;
    std::map<sz::string_view,std::byte> MOD;
    std::map<sz::string_view,std::byte> AUX;
    std::map<sz::string_view,std::byte> EXT_DET;
    std::map<sz::string_view,std::byte> UNI_DET;
    std::map<sz::string_view,std::byte> NEG_QUANT;    
    std::unordered_map<
        sz::string_view,
        uint16_t,
        CaseInsensitiveHash,
        CaseInsensitiveEqual
    > pos_dict;
    std::unordered_set<sz::string_view> MISC;

    std::array<std::byte,9> MAP;

    std::unordered_set<std::string> pos_names;

    bool in_lib(sz::string_view& input);
    uint16_t find_word(sz::string_view& input);
    std::byte POS_to_byte(std::string& pos);
    std::byte search_word(int bitshift,sz::string_view word);
    std::byte find_lib(sz::string_view word);

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