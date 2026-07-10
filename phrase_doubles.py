from csir.document import Document
from csir.skeletons import Skeletons
from csir.pdf_extract import pdf_to_text,unstick_library_prefixes
import csir.skeletons
import json


input1 = "The quick brown fox jumped over the lazy dog. Then the dog howled."
input2 = "DSPy modules can be composed in arbitrary pipelines in a define-by-run interface"
input3 = "the clouds hung low over Briar Street"
input4 = "Some of the clouds hung low over Briar Street"
input5 = "The RNA-guided Cas9 nuclease from the microbial clustered regularly interspaced short palindromic repeats (CRISPR) adaptive immune system can be used to facilitate efficient genome engineering in eukaryotic cells by simply specifying a 20-nt targeting sequence within its guide RNA"
input6 = "The quick brown fox jumped over the lazy dog."
input7 = "What makes this approach appealing is its simplicity."
input8 = "I think that John said that Mary believes that"
input9 = "The book₁ that the student₂ was reading in the library₃ that the librarian₄ had recommended to the professor₅ that the dean₆ might have consulted about the policy₇ that the committee₈ approved last month is on the table."
input10 = """
We present a benchmark targeting a novel class of systems: se-
mantic query processing engines. Those systems rely inherently
on generative and reasoning capabilities of state-of-the-art large
language models (LLMs). They extend SQL with semantic operators,
configured by natural language instructions, that are evaluated via
LLMs and enable users to perform various operations on multi-
modal data
"""
TEST_SENTENCES = {
    # 1–10
    "The cat slept on the warm windowsill.",#"slept",
    "A small error in the dataset caused the entire pipeline to fail.",#"caused",
    "The results were analyzed by two independent reviewers.",#"analyzed",
    "The solution can be obtained by applying dynamic programming.",#"obtained",
    "The committee is considering several proposals this week.",#"considering",
    "These proteins bind to RNA in a sequence-specific manner.",#"bind",
    "The experiment was carried out in sterile conditions.",#"carried",
    "In the morning, the children played in the garden.",#"played",
    "The new algorithm made the optimization significantly faster.",#"made",
    "This device allows the user to control the system remotely.",#"allows",

    # 11–20
    "The system failed to initialize due to a missing dependency.",#"failed",
    "The researchers attempted to replicate the findings.",#"attempted",
    "The model seems to outperform traditional baselines.",#"seems",
    "The program was designed to operate autonomously.",#"designed",
    "The students were given detailed instructions before the exam.",#"given",
    "Under high pressure, the material expands rapidly.",#"expands",
    "The observation that the cells divided faster surprised the biologists.",#"surprised",
    "To reduce noise, the system applies a median filter.",#"applies",
    "What did the engineer design last year?",#"design",
    "The data appears to contradict the hypothesis.",#"appears",

    # 21–25 (trickier)
    "There seems to be a problem with the server.",#"seems",
    "It turned out that the samples were contaminated.",#"turned",
    "Only after the experiment ended did the results become clear.",#"become",
    "What makes this approach appealing is its simplicity.",#"makes",
    "The fact that he left early surprised everyone.",#"surprised",
}
json_output = "skeleton_list.json"

pdf = unstick_library_prefixes(pdf_to_text("csir/ColdWar.pdf")[0])
y = Skeletons(pdf,"sentence_mapping.csv")
#with open(json_output, 'w') as outfile:
#    for sentence in y.sentences:
#        json.dump(sentence, outfile)
#        outfile.write("\n")

# Make sure to fix the split function to account for numbers with decimals! ex: 1.1, 3.45, etc

#The above example incorrectly splits "They" and "instructions"

#for sentence in y.sentences:
    # print(sentence)
    # print()