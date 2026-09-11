#ifndef SYNONYM_RESOLUTION_H
#define SYNONYM_RESOLUTION_H

#include <string>
#include <set>
#include <unordered_map>
#include <vector>
#include <stringzilla/stringzilla.hpp>
namespace sz = ashvardanian::stringzilla;
class synonym_resolution {
public:
    synonym_resolution
    (
        std::vector<std::string_view> input,
        int window_size,
        bool flat = false
    );
    /*synonym_resolution(
        std::vector<std::string_view> text,
        int window_size,
        bool flat = false
    );*/
    
    sz::string_view getText() const;
    //void set_string(std::string_view new_text);

    int getWindowSize() const;
    void setWindowSize(int newWindowSize);

    bool getFlat() const;
    void setFlat(bool newFlat);
    void add_to_word_dict(std::vector<sz::string_view> context, std::string_view input_word);
    void aggregate_prob(std::vector<sz::string_view> context,std::string_view input_word);
    void generate_probabilities(int window_size);
    //void chars_to_string();
    std::vector<std::string_view> split(std::string_view input);
    std::vector<sz::string_view> word_breakdown(std::vector<std::string_view> array_of_words,bool flat);
    sz::string_view get_word(std::vector<sz::string_view> context, int index);
    std::unordered_map<
        std::string_view,
        std::unordered_map<std::string_view, int>
    > get_dict(); 
    std::vector<sz::string_view> identify_window(std::vector<sz::string_view> context,int window_size,int index);
    //sz::string flatten_input(std::vector<std::string> array_of_words,bool flat);
    //void append(std::vector<std::string_view> array, std::string_view insertion);
    void print_all();
    std::vector<std::string_view> getInput();
    std::set<std::string_view> getSet();
    void add_to_dict(std::string_view key_word, std::string_view insert_word,int occurances);
    void print_set();
    //template <typename callback_type_, typename predicate_type_>
    //void split(std::string_view_view str, predicate_type_ && is_delimiter, callback_type_ && callback);
private:
    int window_size;
    bool flat;
    sz::string_view text;

    /*std::unordered_map<
        std::string_view,
        std::set<std::string_view>
    > dict;*/

std::unordered_map<
        std::string_view,
        std::unordered_map<
            std::string_view, int>
        >           dict;

    std::vector<std::string_view> input;
    std::set<std::string_view> word_set;
};

#endif