#include "synonym_resolution.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
/*
(
    //const std::string& text,
    std::vector<std::string> text,
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
{
    //std::cout << "Instantiating object..." << "\n";
    std::set<std::string> word_set;
    //std::cout << "Flattening input..." << "\n";
    this->text = flatten_input(input,flat);
    //std::cout << "Generating probabilities..." << "\n";
    //std::cout << "window size: " << window_size << "\n";
    //Correct up to here
    generate_probabilities(window_size);
    //std::cout << "Instantiation complete!" << "\n";
/*
        self.dict = {}
        self.word_set = set()

        self.text = self.flatten_input(text,flat)
        self.generate_probabilities(window_size)
*/

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
            for(int i2 = 0; i2 < array_of_words[i].size()-1; i2++)
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

std::string synonym_resolution::getText() const
{
    return text;
}

std::unordered_map<
        std::string,
        std::set<std::string>
        >
    synonym_resolution::get_dict()
{
    return dict;
}

void synonym_resolution::set_string(std::string new_text)
{
    text = new_text;
}

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

void synonym_resolution::add_to_word_dict(
    std::vector<std::string> context, 
    std::string input_word
)
{
std::set<std::string> local_set;//Local set of words
std::unordered_map<
    std::string,
    int
    > local_dict; //Local dictionary of words

if (!(word_set.find(input_word) != word_set.end())){ //If word is not already in the word set
    word_set.insert(input_word); //Insert into the global set if word is not already there
}
for(int i = 0; i < context.size()-1; i++){
    if(!(local_set.find(input_word) != local_set.end())){ //If the input word is not already in the local set
        local_set.insert(input_word);//Put the word into the local set
        local_dict[input_word] = 1; //this is the word's first instance in this dictionary. Set it's initial value to 1
    }
    else{
        local_dict[input_word]++; //The word is already in the dictionary - increment it by 1
    }
}
}

void synonym_resolution::aggregate_prob
(
    std::vector<std::string> context,
    std::string input_word
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
    std::vector<std::string> context = word_breakdown();
    for(int i = 0; i < context.size()-1; i++){
        //std::cout << context[i] << "\n";
    }
    //std::cout << "context complete" << "\n";
    int length = context.size()-1;
    int active = 0;

    //std::cout << "Getting probabilities..." << "\n";
    while(active < length){
        std::string word = get_word(context,active);
        //std::cout << "current word = " << word << "\n";
        std::vector<std::string> window = identify_window(context,window_size,active);
        //std::cout << "Window:" << "\n";
        for(int i = 0; i < window.size(); i++){
            //std::cout << window[i] << "\n";
        }
        //std::cout << "Attempting to add to global dict..." << "\n";
        aggregate_prob(window,word);
        active++;
    }
}

std::vector<std::string> synonym_resolution::identify_window
(
    std::vector<std::string> context,
    int window_size,
    int index
)
{
    int words_goal = 2*window_size+1;
    int left = index-window_size;
    int right = index+window_size;
    int active_index = left;
    std::string word = "";
    std::vector<std::string> window;
    int max = context.size()-1;
    while(active_index < right){
        if(active_index == index){
            active_index++;
            right++;
        }
        if(active_index>=max){
            return window;
        }
        if(active_index>=0){
            //int endidx = window.size()-1;
            window.push_back(context[active_index]);
            //append(window,context[active_index]);
        }
        active_index++;
    }
    return window;
}
void synonym_resolution::append(std::vector<std::string> array, std::string insertion){
    int endidx = array.size()-1;
    array[endidx] = insertion;
}

std::string synonym_resolution::get_word
(
    std::vector<std::string> context,
    int index
)
{
    return context[index];
}

std::vector<std::string> synonym_resolution::word_breakdown
(

)
{
    //std::cout << "Validating initial input data: text:" << "\n";
    //std::string input = text;
    ////std::cout << input << "\n";
    std::vector<std::string> split_string = split(this->text);
    //std::cout << "text post-split:" << "\n";
    for(int i = 0; i < split_string.size()-1; i++){
        //std::cout << split_string[i] << "\n";
    }
    //std::cout << "filling context:" << "\n";
    std::vector<std::string> context;
    for(int i = 0; i < split_string.size()-1; i++){
        if(split_string[i].size()-1 != 0){
            //int endidx = context.size()-1;
            //context[endidx] = split_string[i];
            //append(context,split_string[i]);
            context.push_back(split_string[i]);
        }
    }
    //std::cout << "context filled!" << "\n";
    //std::cout << "Proof:" << "\n";
    for(int i = 0; i < context.size()-1; i++){
        //std::cout << context[i] << "\n";
    }
    return context;
}

std::vector<std::string> synonym_resolution::split
(
    std::string input
)
{
    //std::cout << "Input initial state: \n";
    //std::cout << input << "\n";
    //std::cout << "Splitting input..." << "\n";
    std::string builder;
    std::vector<std::string> output;
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
            //int endidx = output.size()-1;
            //output[endidx] = builder;
            //append(output,builder);
            //std::cout << "Pushing to output:" << "\n";
            output.push_back(builder);
            builder = "";
        }
    }
    //std::cout << "result:" << "\n";
    for(int i = 0; i < output.size()-1; i++){
        //std::cout << output[i] << "\n";
    }
    return output;
}