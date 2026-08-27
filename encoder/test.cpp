#include "encoder.h"
#include <iostream>

int main(){
    encoder code;
    sz::string_view input = "The quick brown fox jumped over the lazy dog";
    for(auto word : input.split(" ")){
        if(code.in_lib(word)){
            std::cout << "A word was found in the dictionary!" << "\n";
        }
    }
    return 0;
}