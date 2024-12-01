# Gene-mutation-name-standardization
The main goal of this project is to translate from gene mutation description in natural language into the HGVS standardized nomenclature. The scope of the project was focused on aminoacid substitutions. 

The following files create the (synthesized) datasets based on the [gene mutation patterns](https://github.com/Erechtheus/GenerateMutationData/blob/main/data/mutationfinder.txt) for the learning step by the model based on [BioBART](https://github.com/GanjinZero/BioBART). The files were created to evaluate the model’s functionality when specific parts of the training data are masked.

| File Name | Experiment | Mask |
| --------- | ---------- | ----------- |
| data_maker_poc.py | Proof of Concept | - |
| data_maker_pos.py | Mutation Position | subset of mutation positions | 
| data_maker_pro.py | Amino Acid Forms | 2 out of the three possible forms |
| data_maker_aminoacid.py | Amino Acid Types | a subset of amino acids |
| data_maker_patterns.py | Description Patterns | a subset of the description patterns |

The usage of the above files require arguments described at the beginning of the files.
