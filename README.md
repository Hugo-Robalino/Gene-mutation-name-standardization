# Gene-mutation-name-standardization
The main goal of this project is to translate from gene mutation description in natural language into the HGVS standardized nomenclature. The scope of the project was focused on aminoacid substitutions.

The following files create the (synthesized) datasets for the learning step by the model based on [BioBART](https://github.com/GanjinZero/BioBART):
| File Name | Experiment |
| --------- | ---------- |
| data_maker_poc.py | Proof of Concept |
| data_maker_pos.py | Mutation Position |
| data_maker_pro.py | Amino Acid Forms |
| data_maker_aminoacid.py | Amino Acid Types |
| data_maker_patterns.py | Description Patterns |

