import json, random, sys, math

#This script creates 3 datasubsets, where val and test contain unseen patterns by train

# sys.argv[1] -> file name (e.g. 'instances_pro')
# sys.argv[2] -> number of iterations (e.g. '100')
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

#one subset for training and the other subset for val and test
random.shuffle(patterns)
pattern_train = patterns[150:]
pattern_val_test = patterns[:150]

#dictionary containing the datasets and general info
data = {'description': 'num of random protein pairs (i.e. num of iterations): ' + str(numberOfIterations) + ' & ' +
        'num of random nomenclature patterns: ' + str(numberOfPatterns),
        'info': str(2*numberOfIterations*math.ceil(numberOfPatterns*0.15)+numberOfIterations*math.ceil(numberOfPatterns*0.7)) + ' instances',
        'type': 'patterns',
        'train': [],
        'val': [],
        'test': []}

def create_subset(type='train'):
    
    iterations = .15
    pattern_version = pattern_val_test
    
    if type == 'train':
        iterations = .7
        pattern_version = pattern_train
        
    for i in range(numberOfIterations):
  
        random.shuffle(pattern_version)
    
        for pattern in pattern_version[:int(math.ceil(numberOfPatterns*iterations))]:
      
            version = random.sample(list(vocabulary.keys()), 1)
            sub_vocabulary = vocabulary[version[0]]    
            proteins = random.sample(list(sub_vocabulary.keys()), 2)
            PPOS = str(random.choice(range(1,2001))) #why 2000? -> cause that's the standard number of aminoacids a human DNA has
            WRES = proteins[0]
            MRES = proteins[1]
    
            hgvs = 'p.' + sub_vocabulary[WRES] + PPOS + sub_vocabulary[MRES] 
     
            text = pattern
            text = text.replace('<WRES>', WRES)
            text = text.replace('<MRES>', MRES)
            text = text.replace('<PPOS>', PPOS)

            data[type].append({'input': text, 'target': hgvs})
        
create_subset()
create_subset('val')
create_subset('test')        

#creating the json file
json_object = json.dumps(data, indent=4)
with open(outJSON, "w") as outfile:
    outfile.write(json_object)