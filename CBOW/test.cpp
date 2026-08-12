#include "synonym_resolution.h"
int main(){
    std::string test = "The quick brown fox jumped over the lazy dog";
    bool flat = true;
    int window_size = 1;
    /*
    std::vector<std::string> text,
    int window_size,
    bool flat
    */
    const synonym_resolution& synonyms = new synonym_resolution (test,window_size,flat);
    return 0;
}