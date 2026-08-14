#include "synonym_resolution.h"
#include <iostream>
int main(){
    std::string test1 = "The quick brown fox jumped over the lazy dog";
    std::string test2 = "Marvel vs Capcom";
    std::vector<std::string> input;
    input.push_back(test1);
    input.push_back(test2);
    bool flat = true;
    int window_size = 1;

    synonym_resolution test(input,window_size,flat);
    return 0;
}