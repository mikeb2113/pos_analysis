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
#include <bitset>

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

struct ByteBuilder 
{
        ByteBuilder
        (
            unsigned instruction_num,
            std::array<std::bitset<4>,13> sentence_info
        )
        {
            {

            };
        std::bitset<4> reserved_bytes = 0;
        std::cout << "testing builder init..." << "\n";
        std::cout << "\n";
        std::cout << "instruction num after byte builder: " << instruction_num << "\n";
        std::bitset<4> instruction_bytes = instruction_num;
        std::array<std::bitset<4>,16> byte_array = 
            {
                instruction_bytes,
                reserved_bytes,
                reserved_bytes,
                sentence_info[0],
                sentence_info[1],
                sentence_info[2],
                sentence_info[3],
                sentence_info[4],
                sentence_info[5],
                sentence_info[6],
                sentence_info[7],
                sentence_info[8],
                sentence_info[9],
                sentence_info[10],
                sentence_info[11],
                sentence_info[12]
                //sentence_info
            };
        std::cout << "\n" << "final string: " << "\n";
       for(auto byte : byte_array){
        std::cout << std::bitset<4>(byte);
       } 
        std::cout << "\n";
    };

        size_t space = 0;

        /*
        OLD
        ========BYTE INSTRUCTION============================================
        bytes 0-1                       | idx 0-8   | size: 8   bits/2 bytes
        bytes 2-5 next block offset     | idx 9-24  | size: 16  bits/4 bytes
        bytes 6-7 reserved              | idx 25-32 | size: 8   bits/2 bytes
        bytes 8-63 sentence info        | idx 33-63 | size: 32  bits/8 bytes
        ====================================================================


        NEW
        |========BYTE INSTRUCTION===================================================================================================================
        |byte 0 instruction count        | idx 0-3   | size: 4   bits/1 byte - Offers quick comparator before longer processing. Useful later      |
        |Offset - N/A    Offset removed - encoding is fixed length. This can be derived                                                            |
        |bytes 1-2 reserved              | idx 4-11  | size: 8   bits/2 bytes                                                                      |
        |bytes 3-63 sentence info        | idx 12-63 | size: 52  bits/13 bytes                                                                     |
        |===========================================================================================================================================
        */

    std::array<std::byte,4> get_byte_array_8
    (
        int num
    )
    {
        std::array<std::byte,4> instruction_byte_array;
        std::byte conversion = std::byte(num);
        for(int i = 0; i < 8; i++){
            bool bit_is_one = (conversion & std::byte {1 << i}) != std::byte{0};
            if(bit_is_one){
                instruction_byte_array[i] = std::byte{1};
            }
            else{
                instruction_byte_array[i] = std::byte{0};
            }
        }
        return instruction_byte_array;
    };

    std::array<std::byte,16> get_byte_array_16
    (
        int num
    )
    {
        std::array<std::byte,16> instruction_byte_array;
        std::byte conversion = std::byte(num);
        for(int i = 0; i < 16; i++){
            bool bit_is_one = (conversion & std::byte {1 << i}) != std::byte{0};
            if(bit_is_one){
                instruction_byte_array[i] = std::byte{1};
            }
            else{
                instruction_byte_array[i] = std::byte{0};
            }
        }
        return instruction_byte_array;
    };

    std::array<std::byte,52> get_byte_array_52
    (
        int num
    )
    {
        std::array<std::byte,52> instruction_byte_array;
        std::byte conversion = std::byte(num);
        for(int i = 0; i < 52; i++){
            bool bit_is_one = (conversion & std::byte {1 << i}) != std::byte{0};
            if(bit_is_one){
                instruction_byte_array[i] = std::byte{1};
            }
            else{
                instruction_byte_array[i] = std::byte{0};
            }
        }
        return instruction_byte_array;
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

    //std::array<std::byte,10> MAP;
    std::map<
        std::byte,
        std::map<sz::string_view,std::byte>
        > MAP;

    std::unordered_set<std::string> pos_names;

    bool in_lib(sz::string_view& input);
    uint16_t find_word(sz::string_view& input);
    std::byte POS_to_byte(std::string& pos);
    std::byte search_word_in_known_lib(int bitshift,sz::string_view word);
    std::byte find_lib(sz::string_view word);

    enum class POS : uint16_t {
        DET       = 1 << 1,
        PREP      = 1 << 2,
        CONJ      = 1 << 3,
        COMP      = 1 << 4,
        MOD       = 1 << 5,
        AUX       = 1 << 6,
        EXT_DET   = 1 << 7,
        UNI_DET   = 1 << 8,
        NEG_QUANT = 1 << 9,
        NP        = 1 << 10,
        END       = 1 << 11
    };

    private:
};

#endif