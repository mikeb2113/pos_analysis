#include "encoder.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
encoder::encoder
(

)
{

}

int main(){
    encoder code = encoder();
    for(int i = 0; i < code.DET.size(); i++){
        std::cout << int(code.DET[i]) << "\n";
    }
    return 0;
}