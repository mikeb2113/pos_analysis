#include "synonym_resolution.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stringzilla/stringzilla.hpp>
/*
(
    //std::string_view text,
    std::vector<std::string_view> text,
    int window_size,
    bool flat = false
)
    : window_size(window_size),
      flat(flat)
*/
synonym_resolution::synonym_resolution
(
    std::vector<std::string> input,
    int window_size,
    bool flat
)
    : input(input),
      flat(flat),
      window_size(window_size),
      text(flatten_input(input,flat))
{

    namespace sz = ashvardanian::stringzilla;
    sz::string haystack = "some string";
    sz::string_view needle = sz::string_view(haystack).substr(0, 4);

    this->input = input;
    std::set<std::string_view> word_set;
    chars_to_string();
    //this->text = flatten_input(input,flat);
    generate_probabilities(window_size);
    print_set();
    std::set<std::string_view> set = getSet();
    std::cout << "attempting to print dict..." << "\n";
    for (const auto& outer : dict) {
        std::cout << "Word: " << outer.first << "\n";

        for (const auto& inner : outer.second) {
            std::cout << "  " << inner.first
                    << ": " << inner.second << "\n";
        }
    }
    /*std::cout << "printing input..." << "\n";
    for(int i = 0; i < input.size(); i++){
        std::cout << input[i] << "\n";
    }*/
       //sz::char_set delimiters(" \t\n\r");

    std::cout << "One level deeper..." << "\n";
    for(int i = 0; i < input.size(); i++){
        std::string_view target = input[i];
        std::cout << "target: " << target << "\n";
        for(int i2 = 0; i2 < target.size(); i2++){
        }
    }

    /*for(int i = 0; i < word_set.size(); i++){
        std::cout << word_set[i] << "\n";
    }*/
}

/*template <typename callback_type_, typename predicate_type_>
void synonym_resolution::split(std::string_view_view str, predicate_type_ && is_delimiter, callback_type_ && callback) {
    std::size_t pos = 0;
    while (pos < str.size()) {
        auto const next_pos = std::find_if(str.begin() + pos, str.end(), is_delimiter) - str.begin();
        callback(str.substr(pos, next_pos - pos));
        pos = next_pos == str.size() ? str.size() : next_pos + 1;
    }
}*/
static uint32_t s_AllocCount = 0;
void* operator new(size_t size)
{
    s_AllocCount++;
    std::cout << "Allocating" << size << " bytes\n";
    return malloc(size);
}

void synonym_resolution::print_set()
{
    std::set<std::string_view> set = getSet();
    for(std::_Rb_tree_const_iterator<std::string_view> keyitr = set.begin(); keyitr != set.end(); keyitr++){
        std::cout << *keyitr << "\n";
    }
}

std::vector<std::string> synonym_resolution::getInput()
{
    return this->input;
}

   void synonym_resolution::add_to_dict(std::string_view key_word, std::string_view insert_word,int occurances)
{
    this->dict[key_word][insert_word] = occurances;
}

void synonym_resolution::chars_to_string
(

)
{
    std::vector<std::string> test_container;
    std::string intermediate;
    for(int sentence_num = 0; sentence_num < this->input.size(); sentence_num++){
        //std::cout << "iteration: " << sentence_num << "\n";
        for(int i = 0; i < this->input[sentence_num].size(); i++){
            if(this->input[sentence_num][i] != *" "){
                intermediate += this->input[sentence_num][i];
            }
            else{
                test_container.push_back(intermediate);
                //std::cout << intermediate << "\n";
                intermediate = "";
            }
        }
        if(intermediate != ""){
            test_container.push_back(intermediate);
            //std::cout << intermediate << "\n";
            intermediate = "";
        }
    }
    this->input = test_container;
}

void synonym_resolution::print_all
(

)
{
    for(int i = 0; i < text.size(); i++){
        //std::cout << text[i] << "\n";
    }
}

std::string synonym_resolution::flatten_input
(
    std::vector<std::string> array_of_words,
    bool flat
)
{
    std::string flattened = "";
    if(!flat){
        for(int i = 0; i < array_of_words.size(); i++){ //For array in array of words
            for(int i2 = 0; i2 < array_of_words[i].size(); i2++)
                flattened = flattened + array_of_words[i][i2] + " ";
        }
    }
    else{
        for(int i = 0; i < array_of_words.size(); i++){ //For array in array of words (or word in array)
            flattened = flattened + array_of_words[i] + " ";
        }
    }
    //std::cout << "flattened: " << flattened << "\n";
    return flattened;
}

std::string_view synonym_resolution::getText() const
{
    return text;
}

std::unordered_map<
    std::string_view,
    std::unordered_map<std::string_view, int>
>
    synonym_resolution::get_dict()
{
    return dict;
}

std::set<std::string_view> synonym_resolution::getSet()
{
    return this->word_set;
}

/*void synonym_resolution::set_string(std::string_view new_text)
{
    text = new_text;
}*/

int synonym_resolution::getWindowSize() const
{
    return window_size;
}

void synonym_resolution::setWindowSize(int newWindowSize)
{
    window_size = newWindowSize;
}

bool synonym_resolution::getFlat() const
{
    return flat;
}

void synonym_resolution::setFlat(bool newFlat)
{
    flat = newFlat;
}

void synonym_resolution::add_to_word_dict
(
    std::vector<std::string_view> context, 
    std::string_view input_word
)
{
std::set<std::string_view> local_set;//Local set of words
/*std::unordered_map<
    std::string_view,
    int
    > local_dict; //Local dictionary of words*/

if (!(word_set.find(input_word) != word_set.end())){ //If word is not already in the word set
    word_set.insert(input_word); //Insert into the global set if word is not already there
}
/*for(int i = 0; i < context.size(); i++){
    if(!(local_set.find(input_word) != local_set.end())){ //If the input word is not already in the local set
        local_set.insert(input_word);//Put the word into the local set
        local_dict[input_word] = 1; //this is the word's first instance in this dictionary. Set it's initial value to 1
    }
    else{
        local_dict[input_word]++; //The word is already in the dictionary - increment it by 1
    }
}*/
//Go back and find a way to do this with no additional memory allocations!
}

void synonym_resolution::aggregate_prob
(
    std::vector<std::string_view> context,
    std::string_view input_word
)
{
    add_to_word_dict(context,input_word);
}

void synonym_resolution::generate_probabilities(
    int window_size
)
{
    //std::cout << "Beginning probabilities function" << "\n";
    //std::cout << "First, validating input data:" << "\n";
    //std::cout << "assigning context:" << "\n";
    std::vector<std::string_view> context = word_breakdown();
    for(int i = 0; i < context.size(); i++){
        //std::cout << context[i] << "\n";
    }
    //std::cout << "context complete" << "\n";
    int length = context.size();
    int active = 0;

    //std::cout << "Getting probabilities..." << "\n";
    while(active < length){
        std::string_view word = get_word(context,active);
        //std::cout << "current word = " << word << "\n";
        std::vector<std::string_view> window = identify_window(context,window_size,active);
        //std::cout << "Window:" << "\n";
        for(int i = 0; i < window.size(); i++){
            //std::cout << window[i] << "\n";
        }
        //std::cout << "Attempting to add to global dict..." << "\n";
        aggregate_prob(window,word);
        active++;
    }
}

std::vector<std::string_view> synonym_resolution::identify_window
(
    std::vector<std::string_view> context,
    int window_size,
    int index
)
{
    int words_goal = 2*window_size+1;
    int left = index-window_size;
    int right = index+window_size;
    int active_index = left;
    std::string_view word = "";
    std::vector<std::string_view> window;
    int max = context.size();
    while(active_index < right){
        if(active_index == index){
            active_index++;
            right++;
        }
        if(active_index>=max){
            return window;
        }
        if(active_index>=0){
            //int endidx = window.size();
            window.push_back(context[active_index]);
            //append(window,context[active_index]);
        }
        active_index++;
    }
    return window;
}
/*void synonym_resolution::append(std::vector<std::string_view> array, std::string_view insertion){
    int endidx = array.size();
    array[endidx] = insertion;
}*/

std::string_view synonym_resolution::get_word
(
    std::vector<std::string_view> context,
    int index
)
{
    return context[index];
}

std::vector<std::string_view> synonym_resolution::word_breakdown
(

)
{
    //std::cout << "Validating initial input data: text:" << "\n";
    //std::string_view input = text;
    ////std::cout << input << "\n";
    std::vector<std::string_view> split_string = split(this->text);
    //std::cout << "text post-split:" << "\n";
    for(int i = 0; i < split_string.size(); i++){
        //std::cout << split_string[i] << "\n";
    }
    //std::cout << "filling context:" << "\n";
    std::vector<std::string_view> context;
    for(int i = 0; i < split_string.size(); i++){
        if(split_string[i].size() != 0){
            //int endidx = context.size();
            //context[endidx] = split_string[i];
            //append(context,split_string[i]);
            context.push_back(split_string[i]);
        }
    }
    //std::cout << "context filled!" << "\n";
    //std::cout << "Proof:" << "\n";
    for(int i = 0; i < context.size(); i++){
        //std::cout << context[i] << "\n";
    }
    return context;
}

std::vector<std::string_view> synonym_resolution::split
(
    std::string_view input
)
{
    //std::cout << "Input initial state: \n";
    //std::cout << input << "\n";
    //std::cout << "Splitting input..." << "\n";
    std::string builder;
    std::vector<std::string_view> output;
    //std::cout << "First, checking size of input..." << "\n";
    int size = input.size();
    //std::cout << size << "\n";
    for(int i = 0; i < input.size(); i++){
        if(input[i] != *" "){
            //builder[i] = input[i];
            //std::cout << "Pushing to builder:" << "\n";
            //std::cout << &input[i] << "\n";
            builder.push_back(input[i]);
        }
        else{
            //int endidx = output.size();
            //output[endidx] = builder;
            //append(output,builder);
            //std::cout << "Pushing to output:" << "\n";
            output.push_back(builder);
            builder = "";
        }
    }
    //std::cout << "result:" << "\n";
    for(int i = 0; i < output.size(); i++){
        //std::cout << output[i] << "\n";
    }
    return output;
}