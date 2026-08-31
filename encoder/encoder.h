#ifndef ENCODER_H
#define ENCODER_H
#include <stdio.h>
#include <iostream>
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
    public:
    std::array<std::byte,64> byte_array;
        ByteBuilder
        (
            int instruction_num,
            std::byte sentence_info
        )
        {
        int offset_placeholder = 1573;
        std::byte reserved{0b11001100};
        std::byte offset = std::byte(offset_placeholder);
        std::cout << "testing builder init..." << "\n";
        for(int i = 0; i < byte_array.size(); i++){
            std::cout << 
            std::bitset<1>(std::to_integer<unsigned int>(byte_array[i]));
        }
        std::cout << "\n";
        set_reserve(reserved);
        for(int i = 0; i < byte_array.size(); i++){
            std::cout << 
            std::bitset<1>(std::to_integer<unsigned int>(byte_array[i]));
        }
        std::cout << "\n";

        std::array<std::byte,64> byte_array = 
            {
                static_cast<std::byte>(instruction_num),
                static_cast<std::byte>(offset),
                static_cast<std::byte>(reserved),
                static_cast<std::byte>(sentence_info)
            };
        };

        size_t space = 0;

        /*
        ========BYTE INSTRUCTION============================================
        bytes 0-1                       | idx 0-8   | size: 8   bits/2 bytes
        bytes 2-5 next block offset     | idx 9-24  | size: 16  bits/4 bytes
        bytes 6-7 reserved              | idx 25-32 | size: 8   bits/2 bytes
        bytes 8-63 sentence info        | idx 33-63 | size: 32  bits/8 bytes
        ====================================================================
        */

        void set_reserve
        (
            std::byte new_reserve
        )
        {
            std::array<std::byte,4> bit;
            for(int i = 0; i < 8; i++){
                byte_array[i+25] = new_reserve;
            }
        };
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