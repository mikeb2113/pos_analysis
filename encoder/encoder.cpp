#include "encoder.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
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
//I think that we should have spaghetti, which is delicious, for supper, and we 
//should have garlic bread too, because I really want to have spaghetti and garlic bread.

    /*
I think that we should have spaghetti, 
which is delicious, for supper, and we 


should have garlic bread too, 
because I really want to have spaghetti and garlic bread.
    */
    MISC{},

    MAP
        {
            {std::byte{1}, DET},
            {std::byte{2}, PREP},
            {std::byte{3}, CONJ},
            {std::byte{4}, COMP},
            {std::byte{5}, MOD},
            {std::byte{6}, AUX},
            {std::byte{7}, EXT_DET},
            {std::byte{8}, UNI_DET},
            {std::byte{9}, NEG_QUANT}
            //{std::byte{9}, MISC}
        },
    
    pos_dict{
        //Ensure that each POS has bit shifts to identify them!
        {"the", 1 << 1}, 
        {"a", (1 << 1) | (1 << 7)}, 
        {"an", (1 << 1) | (1 << 7)}, 
        {"this", 1 << 1}, 
        {"that", (1 << 1) | (1 << 4)}, 
        {"these", 1 << 1}, 
        {"those", 1 << 1},//id 0-6

        {"of", 1 << 2}, 
        {"in", 1 << 2}, 
        {"on", 1 << 2}, 
        {"at", 1 << 2}, 
        {"over", 1 << 2}, 
        {"under", 1 << 2},
        {"with", 1 << 2}, 
        {"by", 1 << 2}, 
        {"for", 1 << 2}, 
        {"to", 1 << 2}, 
        {"from", 1 << 2}, 
        {"into", 1 << 2}, 
        {"onto", 1 << 2},//id 7-13

        {"and", 1 << 3}, 
        {"or", 1 << 3}, 
        {"but", 1 << 3},//id 14-16

        {"which", 1 << 4}, 
        {"who", 1 << 4}, 
        {"whom", 1 << 4},//id 17-20

        {"can", 1 << 5}, 
        {"could", 1 << 5}, 
        {"will", 1 << 5}, 
        {"would", 1 << 5}, 
        {"shall", 1 << 5}, 
        {"should", 1 << 5}, 
        {"may", 1 << 5}, 
        {"might", 1 << 5}, 
        {"must", 1 << 5},//id 21-29

        {"be", 1 << 6}, 
        {"am", 1 << 6}, 
        {"is", 1 << 6}, 
        {"are", 1 << 6}, 
        {"was", 1 << 6}, 
        {"were", 1 << 6}, 
        {"been", 1 << 6}, 
        {"being", 1 << 6},
        {"have", 1 << 6}, 
        {"has", 1 << 6}, 
        {"had", 1 << 6}, 
        {"do", 1 << 6}, 
        {"does", 1 << 6}, 
        {"did", 1 << 6},//id 30-43

        {"some", 1 << 7},
        {"one", 1 << 7},
        {"somebody", 1 << 7}, 
        {"someone", 1 << 7}, 
        {"something", 1 << 7}, 
        {"somewhere", 1 << 7},
        {"certain", 1 << 7},//id 44-52

        {"every", 1 << 8}, 
        {"each", 1 << 8},
        {"all", 1 << 8}, 
        {"any", 1 << 8},
        {"whoever", 1 << 8}, 
        {"whatever", 1 << 8}, 
        {"whichever", 1 << 8},//id 53-59

        {"no", 1 << 9},
        {"nobody", 1 << 9}, 
        {"noone", 1 << 9}, 
        {"no-one", 1 << 9}, 
        {"none", 1 << 9},
        {"nothing", 1 << 9},
        {"nowhere", 1 << 9},
        {"never", 1 << 9}//id 60-67
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

    int encoder::get_clause_count(sz::string_view& input){
        ////std::cout << "In clause count function! " << "\n";
        bool in_NP = false;
        int clause_count = 0;
        for(auto word : input.split(" ")){
            if(in_lib(word)){
                clause_count++;
                in_NP = false;
            }

            else{
                if(!in_NP){
                    clause_count++;
                    in_NP = true;
                }
            }
        }
        //std::cout << "There are " << clause_count << " clauses! " << "\n";
        return clause_count;
    }

    std::size_t encoder::get_storage_blocks(int clause_count, int interation, int blocks){
        ////std::cout << "In storage blocks function! " << "\n";
        ////std::cout << "clause count: " << clause_count << "\n";
        std::size_t blocks_needed = 1;
        while(clause_count >= 13){
            clause_count = clause_count - 13;
            blocks_needed++;
        }
        return blocks_needed;
    }

    uint16_t encoder::find_word(sz::string_view& input){
        auto it = pos_dict.find(input);

        if(it == pos_dict.end()){
            return 0;
        }
        return it->second; //This finds the byte code for the given word in the list.
    }

    bool get_encoding_bit(const std::bitset<64>& bits, std::size_t index) {
        //convert from symbolic, human-readable interpretation to literal interpretation
        //(signifigant bit silliness)
        return bits[63 - index];

        //ex:
        //bool first_bit = get_encoding_bit(encoding[0], 0);
        //This can save the first bit stored from the first 64-bit memory block rather than having to put 63 for the
        //first, which can get confusing to read
    }

    std::vector<std::bitset<64>> encoder::generate_encoding(sz::string_view& input){
        int initial_clause_count = get_clause_count(input);
        int max_blocks = get_storage_blocks(initial_clause_count);
        std:: cout << "This input requires " << max_blocks << " memory block(s)!" << "\n";
        std::vector<std::bitset<64>> array;
        sz::basic_string_slice<const char>::split_type view = input.split(" ");
        std::vector<sz::string_view> indexable_view;
        int starting_index = 0;
        /*struct SentenceInfo{
            std::array<std::bitset<4>,16> encoding;
            size_t starting_index;
            size_t ending_index;
        };*/
        for(auto word : view){
            indexable_view.push_back(word);
        }
        //std::cout << "TESTING INPUT VIEW:" << "\n";
        int index = 0;
        for(auto test : view){
            //std::cout << test << "\n";
        }
        for(int current_block = 1; current_block <= max_blocks; current_block++){
            std::array<std::bitset<4>,16> segment;
            size_t test = segment.size();
            //std::cout << "current starting index: " << starting_index << "\n";
            //std::cout << "bytes outside funciton: " << test << "\n";
            SentenceInfo info;
            info = generate_segment(input,indexable_view,&info,initial_clause_count,current_block, max_blocks,starting_index);
            starting_index = info.ending_index+1;
            std::cout << "next starting index: " << starting_index << "\n";
            //std::cout << "next starting index: " << starting_index << "\n";
            segment = info.encoding;
            std::bitset<64> entry(0);
            int idx = 63;
            ////std::cout << "exiting block..." << "\n";
            ////std::cout << "attempting to write to memory... " << "\n";
            for (const std::bitset<4> nibble : segment) {
                //NOTE: there should be 16 nibbles (16*4)
                ////std::cout << "saving nibble..." << "\n";
                for (int i = 3; i >= 0; --i) {
                    entry[idx--] = nibble[i];
                }
            }
            //std::cout << "allocated! " << "\n";
            array.push_back(entry);
            //std::cout << "pushed! " << "\n";
        }

        return array;
    }

    encoder::SentenceInfo encoder::generate_segment(sz::string_view& input, std::vector<sz::string_view> view, SentenceInfo *info,int initial_clause_count, int block, int max_blocks, int starting_index, int iteration, bool in_NP)
    { 
        iteration = block;
        std::cout << "starting index: " << starting_index << "\n";
        std::cout << "in NP: " << in_NP << "\n";
        std::cout << "testing: starting at: " << view[starting_index] << "\n";
        //Consider changing this to return an array.
        //Array index 0, for example, might contain the segment. Index 1 may return an array with starting and ending indices from the input
        
        ////std::cout << "iteration: " << block << "\n";
        ////std::cout << "max blocks: " << max_blocks << "\n";
        //std::cout << "block: " << block << "\n";
        //NOTE: The absolute MAX instruction count is 13 when the memory block is non-terminating.
        //Otherwise, the MAX instruction count is 12, because the terminator instruction takes one byte.
        int instructions_remaining;// = instruction_counter - (13*block);
        int ending_index = starting_index;
        //std::cout << "starting "
        //std::cout << "block: " << block << "\n";
        //std::cout << "max blocks: " << max_blocks << "\n";
        //std::cout << "instructions: " << initial_clause_count << "\n";
        if(block!=max_blocks){
            instructions_remaining = 13;
        }
        else{
            //std::cout << "equal!" << "\n";
            instructions_remaining = abs(13 - abs(initial_clause_count - (13*block)));
        }
        //std::cout << instructions_remaining << "\n";
        std::array<std::bitset<4>,13> sentence_byte_array = 
            {
                std::bitset<4>(0)
            };
        //sz::string prefix_builder;
        //int max = block*13;
        //int idx = max-13;
        int idx = 0;
        int words = 0;

        auto split_range = input.split(" ");
        std::size_t target_index = input.size();
        auto it = std::next(split_range.begin(),target_index);
        //std::cout << "testing iterator..." << *it << "test done!" << "\n";

        if(iteration<= max_blocks)
        {
            //std::cout << "printign words..." << "\n";
            //for(auto word : view)
            for(int i = starting_index; i < view.size(); i++)
                {
                    if(idx<13){
                    sz::string_view word = view[i];
                    //std::cout << word << "\n";
                    words++;
                    ending_index++;
                    //prefix_builder += word;
                    uint16_t bitshift = find_word(word);
                    std::byte bytes = std::byte(std::log2((int(bitshift))));
                    if(in_lib(word))
                    {
                        //instruction_counter++;
                        in_NP = false;

                        sentence_byte_array[idx] = std::bitset<4>(int(bytes));
                        //std::cout << "test: " << int(bytes) << "\n";
                        idx++;
                        std::cout << "\n";
                    }

                    else
                    {
                        if(!in_NP)
                        {
                            ////std::cout << "[NP]";
                            //instruction_counter++;

                            sentence_byte_array[idx] = std::bitset<4>(10); //This word is a part of a Noun Phrase - mark it as such!
                            in_NP = true;
                            idx++; //This index doesn't work - we need to keep going until the NP is escaped!
                            std::cout << "\n";
                            
                        }
                    }
                    std::cout << word << " ";
                }
                else{
                    break;
                }
                }
        }
        size_t sentence_size = sentence_byte_array.size();
        ending_index--;
        std::cout << "\n";
        std::cout << "starting index: ";
        std::cout << starting_index << "\n";
        std::cout << "ending index: " << ending_index << "\n";

        std::array<int,1> bounds;
        bounds[0] = starting_index;
        bounds[1] = ending_index;
        std::cout << "words: " << words << "\n";
        /*
        std::cout << "starting index (bounds): ";
        std::cout << bounds[0] << "\n";
        std::cout << "ending index (bounds): ";
        std::cout << bounds[1] << "\n\n";*/
        //std::cout << "sentence byte array size: " << sentence_size << "\n";
            //sentence_byte_array[idx] = std::bitset<4>(11);
            //^above is the propsed ending bit. We dont need this - this can be 
            //implicitely inferred by the instruction count. Instead, include a 14th
            //count, which signifies 13 instructions + the implicit ending
            //std::cout << "validating instruction counter:" << instruction_counter << "\n";
            std::bitset<4> byteOne = sentence_byte_array[0];
            std::bitset<4> byteTwo = sentence_byte_array[1];
            std::bitset<4> byteThree = sentence_byte_array[2];
            std::bitset<4> byteFour = sentence_byte_array[3];
            std::bitset<4> byteFive = sentence_byte_array[4];
            std::bitset<4> byteSix = sentence_byte_array[5];
            std::bitset<4> byteSeven = sentence_byte_array[6];
            std::bitset<4> byteEight = sentence_byte_array[7];
            std::bitset<4> byteNine = sentence_byte_array[8];
            std::bitset<4> byteTen = sentence_byte_array[9];
            std::bitset<4> byteEleven = sentence_byte_array[10];
            std::bitset<4> byteTwelve = sentence_byte_array[11];
            std::bitset<4> byteThirteen = sentence_byte_array[12];
            int instruction;
            if(block==max_blocks){
                instruction = initial_clause_count-(13*block);
                if(instruction==13){
                    instruction++;
                }
            }
            else{
                instruction = 13;
            }
            //std::cout << "instruction counter test: " << instruction_counter << "\n";
            //std::cout << "encoding thus far: " << "\n";
            //std::cout << std::bitset<4>(instruction) << std::bitset<4>(0) << std::bitset<4>(0) << byteOne << byteTwo << byteThree << byteFour << byteFive << byteSix << byteSeven << byteEight << byteNine << byteTen << byteEleven << byteTwelve << byteThirteen << "\n";
        std::array<std::bitset<4>,16> segment_byte_array = 
            {
                std::bitset<4>(instruction),
                std::bitset<4>(0),
                std::bitset<4>(0),
                byteOne,
                byteTwo,
                byteThree,
                byteFour,
                byteFive,
                byteSix,
                byteSeven,
                byteEight,
                byteNine,
                byteTen,
                byteEleven,
                byteTwelve,
                byteThirteen
            };
            size_t test = segment_byte_array.size();
            std::cout << "\n\n";
            //std::cout << "bytes: " << test << "\n";
            //std::cout << "validating bits:"<< "\n";
            std::cout << byteOne << byteTwo << byteThree << byteFour << byteFive << byteSix << byteSeven << byteEight << byteNine << byteTen << byteEleven <<byteTwelve << byteThirteen << "\n";
            //std::cout << "testing values at indexes:" << "\n";
            //std::cout << segment_byte_array[0] << "\n";
            //std::cout << segment_byte_array[1] << "\n";
            //std::cout << segment_byte_array[2] << "\n";
            //std::cout << segment_byte_array[3] << "\n";
            //std::cout << segment_byte_array[4] << "\n";
            //std::cout << segment_byte_array[5] << "\n";
            //std::cout << segment_byte_array[6] << "\n";
            //std::cout << segment_byte_array[7] << "\n";
            //std::cout << segment_byte_array[8] << "\n";
            //std::cout << segment_byte_array[9] << "\n";
            //std::cout << segment_byte_array[10] << "\n";
            //std::cout << segment_byte_array[11] << "\n";
            //std::cout << segment_byte_array[12] << "\n";
            //std::cout << segment_byte_array[13] << "\n";
            //std::cout << segment_byte_array[14] << "\n";
            //std::cout << segment_byte_array[15] << "\n";
            //std::cout << "Max clause access: 13 " << "\n";
            //std::cout << "Clause accessed: " << idx << "\n";

            //std::cout << "returning...." << "\n";
            words += (13*(block-1));
            //std::cout << "words accessed this pass: " << words << "\n";
            /*struct SentenceInfo{
                std::array<std::bitset<4>,16> encoding;
                size_t starting_index;
                size_t ending_index;
            };*/
            SentenceInfo payload{segment_byte_array,size_t(starting_index),size_t(ending_index)};
            return payload;
    }

    bool encoder::in_lib(sz::string_view& input) {
        return pos_dict.find(input) != pos_dict.end();
    }

    std::byte encoder::search_word_in_known_lib(int bitshift,sz::string_view word){
        std::string builder;
        for(char c : word){
            if(c >= 'A' && c <= 'Z'){
                c += 'a' - 'A';
            }
            builder += c;
        }
        if(bitshift & 1 << 0){
            std::byte word_byte = DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 1){
            std::byte word_byte = PREP[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 2){
            std::byte word_byte = CONJ[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 3){
            std::byte word_byte = COMP[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 4){
            std::byte word_byte = MOD[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 5){
            std::byte word_byte = AUX[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 6){
            std::byte word_byte = EXT_DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 7){
            std::byte word_byte = UNI_DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 8){
            std::byte word_byte = NEG_QUANT[builder];
            return word_byte;
        }
        return std::byte(64);
    }

/*
1101

0000
0000

1010
0100
1010
0101
0110
1010
0100
0110
1010
0010
1010
0011
1010
*/