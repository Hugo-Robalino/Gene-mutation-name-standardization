import json, random, sys

#Update: val and test sets will draw from the same 30% of possible pos [1,2000]

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
        'type': 'pos',
        'train': [],
        'val': [],
        'test': []}

#creating different set of numbers for the train and (eval and test)
numbers_val_test = random.sample(range(1,2001), int(2000*.3))
numbers_train = list(set(list(range(1,2001))) - set(numbers_val_test))
numbers = {'train' : numbers_train, 'val' : numbers_val_test, 'test' : numbers_val_test}

#building the 'test' dataset first and then the 'train & val'
train_split = int(round(numberOfIterations*.7))
val_test_split = int(round(numberOfIterations-train_split)/2)

def create_subset(split=val_test_split, subset='train'):
  
  for i in range(split):  
  
    random.shuffle(patterns)
    
    for pattern in patterns[:numberOfPatterns]:
      
      version = random.sample(list(vocabulary.keys()), 1)
      sub_vocabulary = vocabulary[version[0]]    
      proteins = random.sample(list(sub_vocabulary.keys()), 2)
      
      PPOS = str(random.choice(numbers[subset]))
      WRES = proteins[0]
      MRES = proteins[1]
      
      hgvs = 'p.' + sub_vocabulary[WRES] + PPOS + sub_vocabulary[MRES]
          
      text = pattern
      text = text.replace('<WRES>', WRES)
      text = text.replace('<MRES>', MRES)
      text = text.replace('<PPOS>', PPOS)

      data[subset].append({'input': text, 'target': hgvs})
      
create_subset(train_split)
create_subset(subset='val')
create_subset(subset='test')

#creating the json file
json_object = json.dumps(data, indent=4)
with open(outJSON, "w") as outfile:
    outfile.write(json_object)