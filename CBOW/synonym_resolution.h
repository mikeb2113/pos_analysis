#ifndef SYNONYM_RESOLUTION_H
#define SYNONYM_RESOLUTION_H

#include <string>
#include <set>
#include <unordered_map>
#include <vector>

class synonym_resolution {
public:
    synonym_resolution
    (
        std::vector<std::string> text,
        int window_size,
        bool flat = false
    );
    /*synonym_resolution(
        std::vector<std::string> text,
        int window_size,
        bool flat = false
    );*/

    std::string getText() const;
    void set_string(std::string new_text);

    int getWindowSize() const;
    void setWindowSize(int newWindowSize);

    bool getFlat() const;
    void setFlat(bool newFlat);
    void add_to_word_dict(std::vector<std::string> context, std::string input_word);
    void aggregate_prob(std::vector<std::string> context,std::string input_word);
    void generate_probabilities(int window_size);
    std::vector<std::string> split(std::string input);
    std::vector<std::string> word_breakdown();
    std::string get_word(std::vector<std::string> context, int index);
    std::vector<std::string> identify_window(std::vector<std::string> context,int window_size,int index);
    std::string flatten_input(std::vector<std::string> array_of_words,bool flat);
    void append(std::vector<std::string> array, std::string insertion);

private:
    int window_size;
    bool flat;
    std::string text;

    std::unordered_map<
        std::string,
        std::set<std::string>
    > dict;

    std::set<std::string> word_set;
};

#endif