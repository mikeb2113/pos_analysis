# CSIR Encoder

An experimental fixed width encoding system to capture the syntactic structure of text

## Overview

Many natural language processing techniques couple syntax with semantics, or infer syntactic information from learned semantic patterns. This is effective for many tasks, but for others may introduce unneeded complexity where the desired information is primarily structural.

CSIR investigates an alternative: analyze syntax independently first, then determine whether semantic analysis is necessary for the task at hand.

## How It Works

1) A small library containing common linguistic functors is saved. These include:
* Determiners
* Prepositions
* Conjunctions
* Compositions
* Modifiers
* Auxiliaries
* Existential determiners
* Universal determiners
* Negative quantifiers
 
2) A textual input is given to the program
   
3) Syntactic data is saved into 64-bit fixed-width memory locations that do not consider the concrete definitions of words
   
4) A planned second, variable width encoding will be generated. This will save a sequence of the largest possible noun phrases bounded between two functors.
   
5) This compact, fixed width layer can then be analyzed to identify parts of a text that are syntactically similar.

## Encoding Architecture

This representation assumes the following allocations in a 64-bit representation:

Bits 0-3 -> The count of instructions in this memory block

Bits 4-11 -> Reserved for future use

Bits 12-63 -> Saves numbers representing the different functors considered by this encoding system

The instruction count of an input is saved for the purpose of later equality checks by syntax. If the instruction count is different, we can assume that the texts are not syntactically identical without further analysis.

This encoding system considers 12 different inputs for each nibble in the encoding. 9 for the functors in the library, 1 to denote a noun phrase, 1 to denote the end of an input, and 1 to denote blank space where there is no more textual data.

This encoding is meant to work on two layers. One to simply look at structure devoid of meaning, and another to reconstruct the original text representation. To facilitate this, several tables are created to map words and functors.

Note that functors are 1-indexed so that 0s can be assumed to be empty space.

### Instruction Set

| Binary | Meaning |
|--------|---------|
| `0000` | Empty / unused |
| `0001` | Determiner |
| `0010` | Preposition |
| `0011` | Conjunction |
| `0100` | Composition |
| `0101` | Modifier |
| `0110` | Auxiliary |
| `0111` | Existential Determiner |
| `1000` | Universal Determiner |
| `1001` | Negative Quantifier |
| `1010` | Noun Phrase |
| `1011` | End of Input |
| `1100–1111` | Reserved |

Another table exists to map words to their functors. In this table, strings are keys to byte values. These tables are omitted for brevity.

## Example

Input:
"The quick brown fox jumped over the lazy dog. Then the dog howled."

Structural representation:
DET → NP → PREP → DET → NP → DET → NP → END

Instruction count:
7

64-bit Layer 1 block:
```text
0111 | 00000000 | 0001 1010 0010 0001 1010 0001 1010 1011 0000 0000 0000 0000 0000
count | reserved | instructions
```

## Design Goals

- Compact representation of text.

- Fast lookup.

- Deterministic representation of syntax.

- Reusable processing. Persist structural encodings so that preprocessing may only need to be performed once for a given input.

- Decouple syntax from semantics. Distinguish “What is being said” from “How is it being said.”

- Efficient comparison of textual syntactic data.

## Implementation

### C++17

C++ was chosen to provide precise control over memory representation and
efficient bit-level operations. Low overhead is a primary design
consideration for the encoding system.

### StringZilla

StringZilla provides lightweight string views and text manipulation
without creating unnecessary copies of the original input.

### CMake

CMake manages project configuration, C++ version requirements, and
external dependencies such as StringZilla.

## Project Status

CSIR is currently an experimental research prototype. Layer 1 structural encoding is functional, provided that the input may be represented without having to extend beyond the allowed 64-bit memory space.

Currently implemented:

- The syntactic layer is generated, assuming the instruction count does not exceed the encoding’s maximum count. This maximum count is equal to 13, or 12 if the given memory block must include an end-of-input instruction.

Planned:

- Variable-width encoding to save the concrete values of noun phrases.
- 
- Encoding that can move to the next memory block when exceeding the maximum count.
- 
- Compiler system that can process the binary values.
- 
- Statistical analysis to identify recurring patterns in a text.
- 
- Labeling of noun-phrases to identify relationships in a text.

## Motivation / Research

Imagine this: you’re looking through your documents and you know that about a month ago you wrote a draft letter to a business associate. You forgot its name, but you remember the letter ended in a 3 line sign-off. As a human, you may skim through the documents, looking for documents that have the proper sign-off lines. LLMs may excel at such analysis, but the computational costs associated with model training or LLM calls may not be worthwhile for a given task.

The structure of a text may offer useful logical shortcuts that can be exploited for information gathering. 

The questions this project sets out to answer are these: 

1) Can inexpensive structural filtering eliminate obvious irrelevant candidates before more computationally expensive analysis is performed?
   
2) If concrete definitions are ignored in preprocessing, can patterns and relationships be predicted before more expensive computational tasks?

## License

No open-source license has currently been granted for this project.
All rights reserved.
