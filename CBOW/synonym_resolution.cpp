#include "synonym_resolution.h"
#include <iostream>

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
    std::vector<std::string> text,
    int window_size,
    bool flat
)
{
    std::set<std::string> word_set;
    std::string flat_text = flatten_input(text,flat);
    generate_probabilities(window_size);
/*
        self.dict = {}
        self.word_set = set()

        self.text = self.flatten_input(text,flat)
        self.generate_probabilities(window_size)
*/

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
    return flattened;
}

std::string synonym_resolution::getText() const
{
    return text;
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
for(int i = 0; i < context.size(); i++){
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
    std::vector<std::string> context = word_breakdown();
    int length = context.size();
    int active = 0;

    while(active < length){
        std::string word = get_word(context,active);
        std::vector<std::string> window = identify_window(context,window_size,active);
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
            append(window,context[active_index]);
        }
        active_index++;
    }
    return window;
}
void synonym_resolution::append(std::vector<std::string> array, std::string insertion){
    int endidx = array.size();
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
    std::vector<std::string> split_string = split(text);
    std::vector<std::string> context;
    for(int i = 0; i < split_string.size(); i++){
        if(split_string[i].size() != 0){
            //int endidx = context.size();
            //context[endidx] = split_string[i];
            append(context,split_string[i]);
        }
    }
    return context;
}

std::vector<std::string> synonym_resolution::split
(
    std::string input
)
{
    std::string builder;
    std::vector<std::string> output;
    for(int i = 0; i < input.size(); i++){
        if(input[i] != *" "){
            builder[i] = input[i];
        }
        else{
            //int endidx = output.size();
            //output[endidx] = builder;
            append(output,builder);
            builder = "";
        }
    }
    return output;
}