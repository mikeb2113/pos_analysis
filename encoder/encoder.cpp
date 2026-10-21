#include "encoder.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <fstream> // Required for file streams
#include <fcntl.h>      // open
#include <sys/mman.h>   // mmap, munmap
#include <sys/stat.h>   // fstat
#include <unistd.h>     // close
#include <bitset>
#include <vector>
#include <cstdint>
#include <cstring>
encoder::encoder
(

)
    :
    DET{{"a", std::byte{1}}, {"an", std::byte{2}}, {"that", std::byte{3}}, {"the", std::byte{4}}, {"these", std::byte{5}}, {"this", std::byte{6}}, {"those", std::byte{7}}},
    PREP{{"at", std::byte{1}}, {"by", std::byte{2}}, {"for", std::byte{3}}, {"from", std::byte{4}}, {"in", std::byte{5}}, {"into", std::byte{6}}, {"of", std::byte{7}}, {"on", std::byte{8}}, {"onto", std::byte{9}}, {"over", std::byte{10}}, {"to", std::byte{11}}, {"under", std::byte{12}}, {"with", std::byte{13}}},
    CONJ{{"and", std::byte{1}}, {"but", std::byte{2}}, {"or", std::byte{3}}},
    COMP{{"that", std::byte{1}}, {"which", std::byte{2}}, {"who", std::byte{3}}, {"whom", std::byte{4}}},
    MOD{{"can", std::byte{1}}, {"could", std::byte{2}}, {"may", std::byte{3}}, {"might", std::byte{4}}, {"must", std::byte{5}}, {"shall", std::byte{6}}, {"should", std::byte{7}}, {"will", std::byte{8}}, {"would", std::byte{9}}},
    AUX{{"am", std::byte{1}}, {"are", std::byte{2}}, {"be", std::byte{3}}, {"been", std::byte{4}}, {"being", std::byte{5}}, {"did", std::byte{6}}, {"do", std::byte{7}}, {"does", std::byte{8}}, {"had", std::byte{9}}, {"has", std::byte{10}}, {"have", std::byte{11}}, {"is", std::byte{12}}, {"was", std::byte{13}}, {"were", std::byte{14}}},
    EXT_DET{{"a", std::byte{1}}, {"an", std::byte{2}}, {"certain", std::byte{3}}, {"one", std::byte{4}}, {"some", std::byte{5}}, {"somebody", std::byte{6}}, {"someone", std::byte{7}}, {"something", std::byte{8}}, {"somewhere", std::byte{9}}},
    UNI_DET{{"all", std::byte{1}}, {"any", std::byte{2}}, {"each", std::byte{3}}, {"every", std::byte{4}}, {"whatever", std::byte{5}}, {"whichever", std::byte{6}}, {"whoever", std::byte{7}}},
    NEG_QUANT{{"never", std::byte{1}}, {"no", std::byte{2}}, {"nobody", std::byte{3}}, {"none", std::byte{4}}, {"noone", std::byte{5}}, {"nothing", std::byte{6}}, {"nowhere", std::byte{7}}, {"no-one", std::byte{8}}},
//I think that we should have spaghetti, which is delicious, for supper, and we 
//should have garlic bread too, because I really want to have spaghetti and garlic bread.

    /*
I think that we should have spaghetti, 
which is delicious, for supper, and we 


should have garlic bread too, 
because I really want to have spaghetti and garlic bread.

//I think that we should have spaghetti, which is delicious, for supper, and we should have garlic bread too, because I really want to have spaghetti and garlic bread. I think that we should have spaghetti, which is delicious, for supper, and we should have garlic bread too, because I really want to have spaghetti and garlic bread.
//The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled The quick brown fox jumped over the lazy dog then the dog howled 
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
        //This function returns the total count of instructions to be processed
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
        //This function returns the amount of storage blocks that will be needed to store the given
        //number of instructions
        std::size_t blocks_needed = 1;
        while(clause_count >= 13){
            clause_count = clause_count - 13;
            blocks_needed++;
        }
        return blocks_needed;
    }

    uint16_t encoder::find_word(sz::string_view& input){
        //This finds the byte code for the given word in the list.
        auto it = pos_dict.find(input);

        if(it == pos_dict.end()){
            return 0;
        }
        return it->second; 
    }

    bool encoder::get_encoding_bit(const std::bitset<64>& bits, std::size_t index) {
        //convert from symbolic, human-readable interpretation to literal interpretation
        //(signifigant bit silliness)
        return bits[63 - index];

        //ex:
        //bool first_bit = get_encoding_bit(encoding[0], 0);
        //This can save the first bit stored from the first 64-bit memory block rather than having to put 63 for the
        //first, which can get confusing to read
    }

    //bool encoder::smaller(std::vector<std::bitset<64>> input,std::vector<std::bitset<64>> target){
    bool encoder::smaller(std::vector<std::bitset<64>> input, std::vector<std::bitset<64>> target){
        int input_size = input.size()-1;
        int target_size = target.size()-1;
        //First, see how long the total encoding is
        //If one takes more memory than another - we know which is smaller

        if(input_size < target_size){
            return true;
        }
        else if(target_size<input_size){
            return false;
        }
        //If they occupy an equal amount of memory, we can check the instruction count nibble in the front
        else{
            for(int i = 0; i < 4; i++){
                //Look at each bit in the size nibble.
                //Between the input and target, the first mismatch of a 0 and 1 at matching indices tells us which is larger
                if(input[input_size][63-i]>target[target_size][63-i]){
                    return false;
                }
                else if(input[input_size][63-i]<target[target_size][63-i]){
                    return true;
                }
            }
        }
        return true;
    }

    long long encoder::bitset_to_int(std::bitset<64> input){
        long long result = 0;
        for(int i = 51; i > 0; i--){
            result = result+pow(2,i)*input[i];
        }
        return result;
    }

    int encoder::write_page_file(int start_index, std::string file){
        //Write the start index of each page. Thus, the implicit index of each page can be used
        //to see where each page starts according to the index of the input
        file += "_page";
        std::ofstream outFile(file, std::ios::out | std::ios::binary);

        if (!outFile) {
            std::cerr << "Error opening file for writing!" << std::endl;
            return 1;
        }

        uint16_t write_page = uint16_t(start_index);
        outFile.write(reinterpret_cast<const char *>(&write_page),sizeof(write_page));

       return 0;
    }

    int encoder::write_to_binary(std::array<std::vector<std::bitset<64>>,2> encoding,std::string file)
    {
        // Always verify the file opened successfully

        // 1. Open the file in binary mode
        write_page_file(1,file);
        std::ofstream outFile(file, std::ios::out | std::ios::binary);

        std::vector<std::array<std::bitset<4>,16>> outfile_builder;
        std::bitset<64> builder = generate_header(file);
        std::array<std::bitset<64>,1> intermediate = {builder};

        //std::cout << "printing builder..." << "\n";

        //std::cout << "builder size: " << builder.size() << "\n";

        if (!outFile) {
            std::cerr << "Error opening file for writing!" << std::endl;
            return 1;
        }
        std::cout << "writing..." << "\n";
       for(auto bit : intermediate){
        outFile.write(reinterpret_cast<char *>(&bit),sizeof(bit));
        std::cout << bit;
       }
       std::cout << "\n" << "writing body: " << "\n";
        for(int i = 0; i < encoding.size(); i++){
            for(auto bit : encoding[i]){
                outFile.write(reinterpret_cast<char *>(&bit),sizeof(bit));
                std::cout << bit;
                //std::cout << bit;
            }     
            /*
            for (const auto& bit : encoding) {
                uint64_t value = bit.to_ullong();

                outFile.write(
                    reinterpret_cast<const char*>(&value),
                    sizeof(value)
                );

                std::cout << bit << "\n";
            }
                */
        }
        std::cout << "\n" << "encoding complete! " << "\n";

        return 0;
    }

    int read_page_file(std::string file_name){
        file_name += "_page";
        const char* filepath = file_name.c_str();

        // 1. Open the file descriptor
        int fd = open(filepath, O_RDONLY);
        if (fd == -1) {
            std::perror("Error opening file");
            return 1;
        }

        // 2. Get the size of the file
        struct stat sb;
        if (fstat(fd, &sb) == -1) {
            std::perror("Error getting file size");
            close(fd);
            return 1;
        } 
        size_t fileSize = sb.st_size;
        //std::cout << "file size in pages: " << fileSize << "\n";
        if (fileSize == 0) {
            //std::cout << "File is empty." << std::endl;
            close(fd);
            return 0;
        }

        // 3. Map the file into memory
        // In C++, we must explicitly cast the void* returned by mmap
        char* fileData = static_cast<char*>(mmap(
            nullptr,                // Kernel chooses the address
            fileSize,               // Length of the mapping
            PROT_READ,              // Memory protection: read-only
            MAP_PRIVATE,            // Pages are private to this process
            fd,                     // File descriptor
            0                       // Offset into the file
        ));

        if (fileData == MAP_FAILED) {
            //std::perror("Error with mmap");
            close(fd);
            return 1;
        }

        // 4. The file descriptor can be closed immediately after a successful mmap
        close(fd);

        // 5. Read from the memory-mapped file just like an ordinary array
        // Ensure file contains complete 64-bit records
        if (fileSize % sizeof(uint16_t) != 0) {
            //std::cerr << "Invalid file size!" << std::endl;
            munmap(fileData, fileSize);
            return 1;
        }

        /*
        |==============|
        |id |    target|     
        | 0 |    ALL   |
        | 1 |    POS   |
        | 2 |    WORD  |
        |==============|
        */

        size_t recordCount = fileSize / sizeof(uint16_t);

        //std::cout << "record counts to touch in pages: " << recordCount << "\n";
        std::vector<std::bitset<16>> records;
        records.reserve(recordCount);

        for (size_t i = 0; i < recordCount; ++i) {
            uint16_t value;

            // Copy 8 bytes from mapped memory
            std::memcpy(
                &value,
                fileData + i * sizeof(uint16_t),
                sizeof(uint16_t)
            );
            records.emplace_back(value);
            //std::cout << "value from pages: " <<  value << "\n";
        }
        std::cout << "printing page values: " << "\n";
        for(int i = 0; i < records.size(); i++){
            std::cout << records[i] << "\n";
        }

        return 0;
    }

    std::string encoder::reconstruct_original(int start, int end, int index, sz::string_view& input, std::string file_name){
        std::string output_builder;
        int idx = start;
        int required_bits = end-start+1;

        if(start%4!=0||(end+1)%4!=0){
            std::cout << "error: evidence of data corruption in the binary files!" << "\n";
        }
        
        file_name += "_page";
        const char* filepath = file_name.c_str();

        // 1. Open the file descriptor
        int fd = open(filepath, O_RDONLY);
        if (fd == -1) {
            std::perror("Error opening file");
            return NULL;
        }

        // 2. Get the size of the file
        struct stat sb;
        if (fstat(fd, &sb) == -1) {
            std::perror("Error getting file size");
            close(fd);
            return NULL;
        } 
        size_t fileSize = sb.st_size;
        //std::cout << "file size in pages: " << fileSize << "\n";
        if (fileSize == 0) {
            //std::cout << "File is empty." << std::endl;
            close(fd);
            return NULL;
        }

        // 3. Map the file into memory
        // In C++, we must explicitly cast the void* returned by mmap
        char* fileData = static_cast<char*>(mmap(
            nullptr,                // Kernel chooses the address
            fileSize,               // Length of the mapping
            PROT_READ,              // Memory protection: read-only
            MAP_PRIVATE,            // Pages are private to this process
            fd,                     // File descriptor
            0                       // Offset into the file
        ));

        if (fileData == MAP_FAILED) {
            std::perror("Error with mmap");
            close(fd);
            return NULL;
        }

        // 4. The file descriptor can be closed immediately after a successful mmap
        close(fd);

        // 5. Read from the memory-mapped file just like an ordinary array
        // Ensure file contains complete 64-bit records
        if (fileSize % sizeof(uint16_t) != 0) {
            std::cerr << "Invalid file size!" << std::endl;
            munmap(fileData, fileSize);
            return NULL;
        }

        /*
        |==============|
        |id |    target|     
        | 0 |    ALL   |
        | 1 |    POS   |
        | 2 |    WORD  |
        |==============|
        */

        //size_t recordCount = fileSize / sizeof(uint64_t);
        size_t recordCount = fileSize;

        //std::cout << "record counts to touch in pages: " << recordCount << "\n";
        std::vector<std::bitset<64>> records;
        records.reserve(fileSize);

        for (size_t i = 0; i < recordCount; ++i) {
            uint8_t value;

            // Copy 8 bytes from mapped memory
            std::memcpy(
                &value,
                fileData + i * sizeof(uint8_t),
                sizeof(uint8_t)
            );
            records.emplace_back(value);
            //std::cout << "value from pages: " <<  value << "\n";
            //std::cout << "file data from pages: " <<  fileData << "\n";
        }

        //std::cout << "record test: " << "\n";
        for(auto record:records){
            std::cout << record << "\n";
        }

        //std::cout << "printing records: " << "\n";
        //std::cout << "records size: "  << records.size() << "\n";
        for(int i = 0; i < records.size(); i++){
            std::cout << records[i] << "\n";
        }

        std::bitset<64> byte_array = records[index];
        //std::cout << "relevant array bits: " << "\n";
        //std::cout << "testing byte array: " << "\n";
        for(int i = 0; i < byte_array.size(); i++){
            /*
            for(int i2 = 1; i2 <= 4; i2++){
                //std::cout << byte_array[63-(i+i2)];
                std::cout << 63-(i*(i2)) << "\n";
            }
            */
            //std::cout << byte_array[i] << "\n";
            //std::cout << "size_t test: " << sizeof(byte_array[i]);
            //std::cout << byte_array[i] << "\n";
        }
        while(idx<=end){
            //std::cout << byte_array[idx/4];
            idx++;
        }
        //std::cout << "\n";



        /*
        while(idx<end){
         output_builder+=input[idx];
         idx++;   
        }
         */
        return output_builder;
    }

    std::vector<std::string> encoder::find_text_matches(std::vector<std::array<int,2>> text_coordinates, sz::string_view& input, std::string file_name){
        std::vector<std::string> output_builder;
        for(auto data : text_coordinates){
            //    std::string encoder::reconstruct_original(int start, int end, int index, sz::string_view& input, std::string file_name){
            output_builder.push_back(reconstruct_original(data[0],data[1],0,input,file_name));
        }
        return output_builder;
    }


    int encoder::read_from_binary(std::string file_name, int target, bool include_page_file)
    {
    if(include_page_file){
        read_page_file(file_name);
    }
    int header_size = 4;
    const char* filepath = file_name.c_str();

    // 1. Open the file descriptor
    int fd = open(filepath, O_RDONLY);
    if (fd == -1) {
        std::perror("Error opening file");
        return 1;
    }

    // 2. Get the size of the file
    struct stat sb;
    if (fstat(fd, &sb) == -1) {
        std::perror("Error getting file size");
        close(fd);
        return 1;
    } 
    size_t fileSize = sb.st_size;
    if (fileSize == 0) {
        std::cout << "File is empty." << std::endl;
        close(fd);
        return 0;
    }

    // 3. Map the file into memory
    // In C++, we must explicitly cast the void* returned by mmap
    char* fileData = static_cast<char*>(mmap(
        nullptr,                // Kernel chooses the address
        fileSize,               // Length of the mapping
        PROT_READ,              // Memory protection: read-only
        MAP_PRIVATE,            // Pages are private to this process
        fd,                     // File descriptor
        0                       // Offset into the file
    ));

    std::cout << "Attempting to read from binary file: "
            << file_name << "\n";

    for (size_t i = 0; i + sizeof(std::bitset<64>) <= fileSize;
        i += sizeof(std::bitset<64>)) {

        std::bitset<64> record;

        std::memcpy(&record, fileData + i, sizeof(record));

        std::cout << record << "\n";
    }

    if (fileData == MAP_FAILED) {
        std::perror("Error with mmap");
        close(fd);
        return 1;
    }

    // 4. The file descriptor can be closed immediately after a successful mmap
    close(fd);

    // 5. Read from the memory-mapped file just like an ordinary array
    // Ensure file contains complete 64-bit records
    //std::cout << "file size: " << fileSize*8 << "\n";
    //std::cout << "file size test: " << sizeof(uint64_t) << "\n";
    //std::cout << "divis test: " << (fileSize*8)%sizeof(uint64_t) << "\n";
    /*
    if (((fileSize*8) % sizeof(uint64_t)) != 0) {
        std::cerr << "Invalid file size!" << std::endl;
        munmap(fileData, fileSize);
        return 1;
    }
    */

    size_t recordCount;
/*
    switch (target){
        case(1):
            recordCount = (fileSize / sizeof(uint64_t)/2);
            //std::cout << "detected: POS" << "\n";
            break;
        case(2):
            recordCount = (fileSize / sizeof(uint64_t)/2);
            //std::cout << "detected: WORD" << "\n";
            break;
        case(0):
            recordCount = fileSize / sizeof(uint64_t);
            //std::cout << "detected: ALL" << "\n";
            break;
    }
*/
    switch (target){
        case(1):
            recordCount = (fileSize / sizeof(uint64_t)/2);
            //std::cout << "detected: POS" << "\n";
            break;
        case(2):
            recordCount = (fileSize / sizeof(uint64_t)/2);
            //std::cout << "detected: WORD" << "\n";
            break;
        case(0):
            recordCount = fileSize;
            //std::cout << "detected: ALL" << "\n";
            break;
    }

    //std::cout << "record counts to touch: " << recordCount << "\n";
    std::vector<std::bitset<8>> records;
    records.reserve(recordCount);

    //std::cout << "beginning loop..." << "\n";

    for (size_t i = 0; i < recordCount; ++i) {
        uint16_t value;
        //std::cout << "loading to memory..." << "\n";
        //std::cout << "testing values: " << "\n";
        //std::cout << i << "\n";
        //std::cout << &value << "\n";
        //std::cout << fileData + i * sizeof(uint8_t) << "\n";
        //std::cout << sizeof(uint8_t);
        // Copy 8 bytes from mapped memory
        std::memcpy(
            &value,
            fileData + i * sizeof(uint8_t),
            sizeof(uint8_t)
        );
        //std::cout << "\n" << "data is in memory! " << "\n";
        records.emplace_back(value);
        //std::cout << value << "\n";
    }

    munmap(fileData, fileSize);

    /*
    |==============|
    |id |    target|     
    | 0 |    ALL   |
    | 1 |    POS   |
    | 2 |    WORD  |
    |==============|
    */
    std::cout << "records size: " << records.size() << "\n";
    std::cout << "printing records: " << "\n";
/*
    for (size_t i = 0; i + sizeof(std::bitset<64>) <= fileSize; i += sizeof(std::bitset<64>)) {

        std::bitset<64> record;

        std::memcpy(&record, fileData + i, sizeof(record));

        std::cout << record << "\n";
    }
*/
    for(int i = 0; i < records.size(); i++){
        for(int i2 = 0; i2 < 8; i2++){
            std::cout << records[i][i2];
        }
        //std::cout << records[i] << "\n";
    }
    std::cout << "\n";
    std::cout << "skipping to reocrd 0: " << "\n";
    std::cout << records[0][0] << "\n";
    std::cout << "skipping to reocrd 1: " << "\n";
    std::cout << records[0][1] << "\n";
/*
    std::cout << "skipping to reocrd 0: " << "\n";
    std::cout << records[1][0] << "\n";
    std::cout << "skipping to reocrd 1: " << "\n";
    std::cout << records[1][1] << "\n";
    std::cout << "skipping to reocrd 0: " << "\n";
    std::cout << records[1][2] << "\n";
    std::cout << "skipping to reocrd 1: " << "\n";
    std::cout << records[1][3] << "\n";
    std::cout << "skipping to reocrd 0: " << "\n";
    std::cout << records[1][4] << "\n";
    std::cout << "skipping to reocrd 1: " << "\n";
    std::cout << records[1][5] << "\n";
*/
    std::cout << "returning" << "\n";
    return 0;
    }

    std::vector<std::array<int,2>> encoder::presence(std::vector<std::bitset<64>> input,std::vector<std::bitset<64>> target){
        std::vector<std::array<int,2>> presence;
        std::vector<std::bitset<64>> a;
        std::vector<std::bitset<64>> b;
        std::string file = "test";
        std::bitset<64> header = generate_header(file);
        int header_size = header.size();
        int shift = 12+(header_size*4);
        if(smaller(input,target)){ //First, gurantee a smaller variable: a
            a = input;
            b = target;
        } else{
            a = target;
            b = input;
        }
        int a_size = a.size();
        std::size_t last_index_instructions = pow(2,3)*a[a_size-1][63] + pow(2,2)*a[a_size-1][62] + pow(2,1)*a[a_size-1][61] + pow(2,0)*a[a_size-1][60];
        int min_to_match = last_index_instructions + (13*(a.size()-1));
        //There must be at least min_to_match common nibbles in a row between a1 and b1
        for(int a_byte_array = 0; a_byte_array < a.size(); a_byte_array++){
            std::bitset<64> a1 = a[a_byte_array] << 12; //bitshift a given byte array left 12 
            for(int byte_array = 0; byte_array < b.size(); byte_array++){
                int consecutive_match = 0;
                int starting_index = 0;
                std::bitset<64> b1 = b[byte_array] << 12; //These 1 values will begin with the instructions and 0 out the rest
                for(int i = 0; i < 12; i++){
                    if((a1[63]==0&&a1[63-1]==0&&a1[63-2]==0&&a1[63-3]==0) || (b1[63]==0&&b1[63-1]==0&&b1[63-2]==0&&b1[63-3]==0)){
                        break; 
                    }
                //If we reach zeroed out sections - terminate the byte array early. This will make for 
                //less redundant computations after each shift
                for(int clauses = 0; clauses < min_to_match; clauses++){
                    if(a1[63-(4*clauses)]==b1[63-(4*clauses)]&&a1[63-1-(4*clauses)]==b1[63-1-(4*clauses)]&&a1[63-2-(4*clauses)]==b1[63-2-(4*clauses)]&&a1[63-3-(4*clauses)]==b1[63-3-(4*clauses)]){
                        consecutive_match++;
                        //increment consecutive match on a matching nibble
                        if(consecutive_match==min_to_match){
                            //std::cout << "[" << 12+starting_index << ", " << 11+starting_index+(4*min_to_match) << "] index: " << byte_array << "\n";
                            presence.push_back(std::array<int,2>{12+starting_index,11+starting_index+(4*min_to_match)});
                            consecutive_match = 0;
                            //If we have at least min_to_match matching nibbles in a row, append the start and end
                            //indexes to the output
                        }
                    }
                    else{
                        consecutive_match = 0;
                        //Set to 0 incase there was at least one match, but less than the needed amount
                    }
                }
                    b1 <<= 4;
                    //bitshift only the larger
                    starting_index += 4;
                    //Move the starting index with the shift
                }
            }
        }
        return presence;
        //Return a vector with each matching candidate between the two inputs
    }

    std::array<std::vector<std::bitset<64>>,2> encoder::generate_encoding(sz::string_view& input, std::string name){
        std::vector<std::bitset<64>> pos = generate_POS_encoding(input,true);
        std::vector<std::bitset<64>> concrete = generate_POS_encoding(input,false);
        std::array<std::vector<std::bitset<64>>,2> encoding{pos,concrete};

        if(write_to_binary(encoding,name)==1){
            std::cout << "error: could not write to binary file! Data not persisted!" << "\n";
        } else{
            std::cout << "file saved!" << "\n";
        }
        return encoding;
    }

    std::bitset<64> encoder::generate_header(std::string input){
        sz::string_view file_type = ".txt";
        std::bitset<4> file_byte_array;
        std::bitset<64> header_array;
        if(file_type != ".pdf"){
            header_array = std::bitset<64>(1);
            //If not a visual text format, set file type to 0
        } else{
            header_array = std::bitset<64>(0);
            //If a visual text format, set file type to 1
        }
        return header_array;
    }

    std::vector<std::bitset<64>> encoder::generate_POS_encoding(sz::string_view& input, bool POS_or_concrete){
        //if POS_or_concrete is true, then the encoding will be for the part of speech of the input
        //if false, then the encoding will denote the indexes of the words from their parts of speech

        //This function returns the full encoding in a vector. Each entry in the vector is a 64-bit binary string.
        //Each string begins with an instruction count, followed by 2 more bytes for the reserved slots.
        //the rest of the bytes are for instructions.
        //Note that logically, the instruction count will always evaluate to 13 unless this is the last
        //instruction block. For the last block, it can never be 13. 
        
        //Rather, if the last block contains
        //13 instructions, it will add 1 to the instruction count 
        //to denote 13 instructions + an implicit ending instruction

        int starting_index = 0;
        int index = 0;
        int initial_clause_count = get_clause_count(input);
        int max_blocks = get_storage_blocks(initial_clause_count);
        //Derive the needed memory blocks and the number of instructions we need to save

        std::vector<std::bitset<64>> array;
        sz::basic_string_slice<const char>::split_type view = input.split(" ");
        std::vector<sz::string_view> indexable_view;
        //^We evaluate on a vector instead of the view itself so that we can simply index to access words

        for(auto word : view){
            indexable_view.push_back(word);
        }
        int NP_carryover = 1;
        for(int current_block = 1; current_block <= max_blocks; current_block++){
            std::array<std::bitset<4>,16> segment;
            //save an array of size 16. Each entry is a bitset of 4 for a total of 64 bits of storage
            SentenceInfo info;
            //Save info to store important information

            info = generate_segment(NP_carryover,POS_or_concrete,input,indexable_view,&info,initial_clause_count,current_block, max_blocks,starting_index);
            starting_index = info.ending_index+1;
            segment = info.encoding;
            NP_carryover = info.NP_carryover;
            std::bitset<64> entry(0);
            //initialize entry to 0s. Then update with accurate values from info
            int idx = 63;

            for (const std::bitset<4> nibble : segment) {
                for (int i = 3; i >= 0; --i) {
                    entry[idx--] = nibble[i];
                }
            }
            //Add the 64-bit encoding to the vector
            array.push_back(entry);
        }

        return array;
    }

    encoder::SentenceInfo encoder::generate_segment(int NP_carryover, bool POS_or_concrete, sz::string_view& input, std::vector<sz::string_view> view, SentenceInfo *info,int initial_clause_count, int block, int max_blocks, int starting_index, int iteration, bool in_NP)
    { 
        iteration = block;
        //Consider changing this to return an array.
        //Array index 0, for example, might contain the segment. Index 1 may return an array with starting and ending indices from the input
        //NOTE: The absolute MAX instruction count is 13 when the memory block is non-terminating.
        //Otherwise, the MAX instruction count is 12, because the terminator instruction takes one byte.
        int instructions_remaining;
        int ending_index = starting_index;
        int NPs = 0;
        int NP_id = 1;
        int NP_start = 0;
        int NP_end = 0;
        int page = 0;
        std::vector<std::array<int,2>> NP_list_builder;
        std::vector<int> NP_idxs;
        if(block!=max_blocks){
            instructions_remaining = 13;
        }
        else{
            instructions_remaining = initial_clause_count - (13*(block-1));
        }
        std::array<std::bitset<4>,13> sentence_byte_array = 
            {
                std::bitset<4>(0)
            };

        int idx = 0;
        int words = 0;

        if(iteration <= max_blocks)
        {
            for(int i = starting_index; i < view.size(); i++)
                {
                    if(idx<13){
                    sz::string_view word = view[i];
                    words++;
                    ending_index++;
                    uint16_t bitshift = find_word(word);
                    std::byte bytes;
                    if(POS_or_concrete == true){
                        bytes = std::byte(std::log2((int(bitshift))));
                    } else{
                        bytes = search_word_in_known_lib(int(bitshift),word);

                    }


                    if(in_lib(word))
                    {
                        if(!POS_or_concrete && in_NP){
                            NP_end = i-1;
                            //std::cout << "end: " << NP_end << "\n";
                        }
                        in_NP = false;
                        sentence_byte_array[idx] = std::bitset<4>(int(bytes));
                        idx++;
                    }

                    else
                    {
                        if(!in_NP)
                        {
                            sentence_byte_array[idx] = std::bitset<4>(10); //This word is a part of a Noun Phrase - mark it as such!
                            if(!POS_or_concrete){
                                NPs++;
                                NP_idxs.push_back(idx);
                                NP_start = i;
                                

                                //std::cout << "testing NP values for word: " << view[i] << "\n"; //This is the word
                                //std::cout << "index: " << NP_carryover << "\n"; //This is the NP functor index - which occurance of an NP it is
                                //std::cout << "start: " << NP_start << "\n"; // This is the index in the original text (if treated as an array of strings)
                                NP_list_builder.push_back(std::array<int,2>{NP_carryover,NP_start});
                                //std::cout << "page: " << page << "\n";
                                NP_carryover++;
                            }
                            in_NP = true;
                            idx++;
                        }
                    }
                }
                else{
                    break;
                }
                }
            if(!POS_or_concrete){
                if(in_NP){
                    NP_end = view.size()-1;
                    //std::cout << "end: " << NP_end << "\n";
                }
                for(auto index : NP_idxs){
                    sentence_byte_array[index] = std::bitset<4>(NPs);
                    //If operating on the concrete representation: save the NP value as
                    //The total # of NPs in this encoding. This can allow us to skip repeated 
                    //comparisons down stream
                }
                NPs = 0;
                NP_idxs.clear();
            }
        }
        size_t sentence_size = sentence_byte_array.size();
        ending_index--;

        std::array<int,2> bounds;
        bounds[0] = starting_index;
        bounds[1] = ending_index;

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
                instruction = initial_clause_count-(13*(block-1));
                if(instruction==13){
                    instruction++;
                }
            }
            else{
                instruction = 13;
            }
            //std::cout << std::bitset<4>(instruction) << std::bitset<4>(0) << std::bitset<4>(0) << byteOne << byteTwo << byteThree << byteFour << byteFive << byteSix << byteSeven << byteEight << byteNine << byteTen << byteEleven << byteTwelve << byteThirteen << "\n";
        std::array<std::bitset<4>,16> segment_byte_array = 
            {
                byteThirteen,
                byteTwelve,
                byteEleven,
                byteTen,
                byteNine,
                byteEight,
                byteSeven,
                byteSix,
                byteFive,
                byteFour,
                byteThree,
                byteTwo,
                byteOne,
                std::bitset<4>(0),
                std::bitset<4>(0),
                std::bitset<4>(instruction)

/*
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
*/
            };
            size_t test = segment_byte_array.size();
            //std::cout << byteOne << byteTwo << byteThree << byteFour << byteFive << byteSix << byteSeven << byteEight << byteNine << byteTen << byteEleven <<byteTwelve << byteThirteen << "\n";
            words += (13*(block-1));

            SentenceInfo payload{segment_byte_array,size_t(starting_index),size_t(ending_index),NP_carryover};
            return payload;
    }

    bool encoder::in_lib(sz::string_view& input) {
        //Quick pre-check to see if a given word is present in any library.
        //If not present, return false. If present, return true
        return pos_dict.find(input) != pos_dict.end();
    }

    std::byte encoder::search_word_in_known_lib(int bitshift,sz::string_view word){
        //If we know what library a word belongs in, find the words index in that library.
        //This has no current use, but may be used in the future for decoding back to the original input
        std::string builder;
        for(char c : word){
            if(c >= 'A' && c <= 'Z'){
                c += 'a' - 'A';
            }
            builder += c;
        }
        if(bitshift & 1 << 1){
            std::byte word_byte = DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 2){
            std::byte word_byte = PREP[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 3){
            std::byte word_byte = CONJ[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 4){
            std::byte word_byte = COMP[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 5){
            std::byte word_byte = MOD[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 6){
            std::byte word_byte = AUX[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 7){
            std::byte word_byte = EXT_DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 8){
            std::byte word_byte = UNI_DET[builder];
            return word_byte;
        }
        else if(bitshift & 1 << 9){
            std::byte word_byte = NEG_QUANT[builder];
            return word_byte;
        }
        return std::byte(64);
    }

    bool encoder::equals(std::vector<std::bitset<64>> a, std::vector<std::bitset<64>> b){
        if(a.size()!=b.size()){
            return false;
        }
        int i = 0;
        for(auto bit : a){
            if(a[i] != b[i]){
                return false;
            }
            i++;
        }
        return true;
    }