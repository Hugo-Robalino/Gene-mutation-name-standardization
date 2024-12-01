import json, random, sys

#This script creates 3 datasubsets, where val and test contain unseen aminoacids by train

# sys.argv[1] -> file name (e.g. 'instances_pro')
# sys.argv[2] -> number of iterations (e.g. '100') SUGGESTION: better use multiples of 20
# sys.argv[3] -> number of patterns (e.g. '497') WARNING: at most 497

outJSON = sys.argv[1] + '.json'

random.seed(1492)

#setting constant values
numberOfIterations = int(sys.argv[2]) #int 
numberOfPatterns = int(sys.argv[3]) #int

vocabulary = \
{
 1:
 {'A': 'Ala',
  'R': 'Arg',
  'N': 'Asn',
  'D': 'Asp',
  'C': 'Cys',
  'Q': 'Gln',
  'E': 'Glu',
  'G': 'Gly',
  'H': 'His',
  'I': 'Ile',
  'L': 'Leu',
  'K': 'Lys',
  'M': 'Met',
  'F': 'Phe',
  'P': 'Pro',
  'S': 'Ser',
  'T': 'Thr',
  'W': 'Trp',
  'Y': 'Tyr',
  'V': 'Val'},
 2: 
 {'Alanine': 'Ala',
  'Argenine': 'Arg',
  'Asparagine': 'Asn',
  'Aspartic acid': 'Asp', #Aspartate?
  'Cysteine': 'Cys',
  'Glutamine': 'Gln',
  'Glutamic acid': 'Glu', #Glutamate?
  'Glycine': 'Gly',
  'Histidine': 'His',
  'Isoleucine': 'Ile',
  'Leucine': 'Leu',
  'Lysine': 'Lys',
  'Methionine': 'Met',
  'Phenylalanine': 'Phe',
  'Proline': 'Pro',
  'Serine': 'Ser',
  'Threonine': 'Thr',
  'Tryptophane': 'Trp',
  'Tyrosine': 'Tyr',
  'Valine': 'Val'},
 3:
 {'Ala': 'Ala',
  'Arg': 'Arg',
  'Asn': 'Asn',
  'Asp': 'Asp',
  'Cys': 'Cys',
  'Gln': 'Gln',
  'Glu': 'Glu',
  'Gly': 'Gly',
  'His': 'His',
  'Ile': 'Ile',
  'Leu': 'Leu',
  'Lys': 'Lys',
  'Met': 'Met',
  'Phe': 'Phe',
  'Pro': 'Pro',
  'Ser': 'Ser',
  'Thr': 'Thr',
  'Trp': 'Trp',
  'Tyr': 'Tyr',
  'Val': 'Val'}
}

#creating a mapping dict for support
vocab_map = \
{'Alanine': 'A',
  'Argenine': 'R',
  'Asparagine': 'N',
  'Aspartic acid': 'D', #Aspartate?
  'Cysteine': 'C',
  'Glutamine': 'Q',
  'Glutamic acid': 'E', #Glutamate?
  'Glycine': 'G',
  'Histidine': 'H',
  'Isoleucine': 'I',
  'Leucine': 'L',
  'Lysine': 'K',
  'Methionine': 'M',
  'Phenylalanine': 'F',
  'Proline': 'P',
  'Serine': 'S',
  'Threonine': 'T',
  'Tryptophane': 'W',
  'Tyrosine': 'Y',
  'Valine': 'V'}

with open('patterns.txt') as file:
    content = file.readlines()[:]

#choose only simple patterns (i.e. one pair of proteins and one position)
patterns = [x[:-1] for x in content if (x.count('<POS>') == 0 and x.count('<RES>') == 0)]

if numberOfPatterns > len(patterns):
  raise TypeError('Number of patterns must be lower than ' + str(len(patterns)))

#dictionary containing the datasets and general info
data = {'description': 'num of random protein pairs (i.e. num of iterations): ' + str(numberOfIterations) + ' & ' +
        'num of random nomenclature patterns: ' + str(numberOfPatterns),
        'info': str(numberOfIterations*numberOfPatterns) + ' instances',
        'type': 'aminoacid',
        'train': [],
        'val': [],
        'test': []}

#creating 2 different sub_dict, for train and val_test

amino_acid_subset = random.sample(list(vocabulary[2].keys()), 6) #6 cause that's 30% of 20 (amino acids)

train_vocab = {1:{}, 2:{}, 3:{}}
val_test_vocab = {1:{}, 2:{}, 3:{}}

for amino_acid in vocabulary[2].keys():
  map_1 = vocab_map[amino_acid]
  map_3 = vocabulary[2][amino_acid]
  if amino_acid in amino_acid_subset:
    val_test_vocab[1][map_1] = map_3
    val_test_vocab[2][amino_acid] = map_3
    val_test_vocab[3][map_3] = map_3
  else:
    train_vocab[1][map_1] = map_3
    train_vocab[2][amino_acid] = map_3
    train_vocab[3][map_3] = map_3 

#building the 3 different data subsets

train_split = int(round(numberOfIterations*.7))
val_test_split = int(round(numberOfIterations-train_split)/2)

def create_subset(name='train', split=val_test_split):
  
  for i in range(split):  
  
    random.shuffle(patterns)
    
    for pattern in patterns[:numberOfPatterns]:
      
      if name == 'train':
        dictionary = train_vocab
      else:
        dictionary = val_test_vocab
      
      version = random.sample(list(vocabulary.keys()), 1)
      sub_vocabulary = dictionary[version[0]]  
      proteins = random.sample(list(sub_vocabulary.keys()),2)
      PPOS = str(random.choice(range(1,2001)))
      WRES = proteins[0]
      MRES = proteins[1]
      
      hgvs = 'p.' + sub_vocabulary[WRES] + PPOS + sub_vocabulary[MRES]
          
      text = pattern
      text = text.replace('<WRES>', WRES)
      text = text.replace('<MRES>', MRES)
      text = text.replace('<PPOS>', PPOS)

      data[name].append({'input': text, 'target': hgvs})
      
create_subset(split=train_split)
create_subset('val')
create_subset('test')

#creating the json file
json_object = json.dumps(data, indent=4)
with open(outJSON, "w") as outfile:
    outfile.write(json_object)