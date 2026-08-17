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



    /*std::string text = test.getText();
    for(int i = 0; i < text.size(); i++){
        std::cout << text[i] << "\n";
    }
    std::cout << "Test run 1 complete!" << "\n";
    std::cout << "Test run 2:" << "\n";
    std::string test_value_1 = "this";
    std::string test_value_2 = "is";
    std::string test_value_3 = "a";
    std::string test_value_4 = "test";
    std::vector<std::string> test_input;
    test_input.push_back(test_value_1);
    test_input.push_back(test_value_2);
    test_input.push_back(test_value_3);
    test_input.push_back(test_value_4);
    for(int i = 0; i < test_input.size(); i++){
        std::cout << test_input[i] << "\n";
    }*/


    
    std::unordered_map<
        std::string,//key

        /*
        std::unordered_map< 
        std::set<std::string>,
        int
        >
        */
        std::vector<std::string>
    > global_dictionary;

    std::unordered_map<
        std::string,
        int
        >   local_values;
    std::cout << "validating dictionary..." << "\n";



    /*
  std::unordered_map<
    std::string,
    int
    > test_map = {};
    int occurances = test_map["fox"];
    std::cout << "fox occurances: " << occurances << "\n";
*/


    //std::cout << dictionary["fox"]["jumped"] << "\n";
    /*for(auto itr = begin(dictionary); itr != end(dictionary); ++itr){
        std::cout << itr << "\n";
    }*/
    return 0;
}