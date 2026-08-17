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
    std::cout << "Object created!" << "\n";
    std::cout << "Validating text..." << "\n";
    std::vector<std::string> output = test.getInput();
    std::cout << output.size();
    for(int i = 0; i < output.size(); i++){
        std::cout << output[i] << "\n";
    }
    std::cout << "dictionary validation: " << "\n";
    std::unordered_map<
        std::string,
        std::set<std::string>
    > dictionary = test.get_dict();
    std::set<std::string> test_word_set = test.getSet();
    for(std::_Rb_tree_const_iterator<std::string> itr = test_word_set.begin(); itr != test_word_set.end(); itr++){
        std::cout << *itr << "\n";
    }
    return 0;
}