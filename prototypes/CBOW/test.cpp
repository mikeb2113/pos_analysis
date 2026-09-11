#include "synonym_resolution.h"
#include <iostream>
#include <stringzilla/stringzilla.hpp>

int main(){
    std::string_view test1 = "The quick brown fox jumped over the lazy dog";
    std::string_view test2 = "Marvel vs Capcom";
    std::vector<std::string_view> input;
    input.push_back(test1);
    input.push_back(test2);
    bool flat = true;
    int window_size = 1;

    synonym_resolution test(input,window_size,flat);

    namespace sz = ashvardanian::stringzilla;

    sz::string_view text = "The quick brown fox jumped over the lazy dog";

    for (sz::string_view word : text.split("\r\n")) {
        if (!word.empty()) {
            std::cout << word << '\n';
        }
    }

    //std::cout << "Object created!" << "\n";
    //std::cout << "Validating text..." << "\n";
    /*std::vector<std::string> output = test.getInput();
    //std::cout << output.size();
    for(int i = 0; i < output.size(); i++){
        //std::cout << output[i] << "\n";
    }*/
    //std::cout << "dictionary validation: " << "\n";
/*std::unordered_map<
        std::string_view,
        std::unordered_map<std::string_view, int>
    > dictionary = test.get_dict();
    std::set<std::string_view> test_word_set = test.getSet();*/

    /*for(std::_Rb_tree_const_iterator<std::string_view> keyitr = test_word_set.begin(); keyitr != test_word_set.end(); keyitr++){
        //std::vector<std::string_view> arr = dictionary[*keyitr];
        std::cout << "Key: " << *keyitr << "\n";
        std::cout << "Values: " << "\n";
        std::vector<std::string_view> localKeyItr = dictionary[*keyitr];
        for(int i = 0; i < localKeyItr.size(); i++){
            std::cout << localKeyItr[i] << "\n";
        }
        //std::cout << *keyitr << "\n";
        //*keyitr relates to the word in the set. This can eb used to access the keys in the dictionary
        std::cout << "\n";
    }*/
    return 0;
}