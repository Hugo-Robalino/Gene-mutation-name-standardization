from transformers import AutoTokenizer, DataCollatorForSeq2Seq, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from data_process import load_dataset_subsets
from chr_evaluate import char_precisions, char_recalls
import os, sys, random, evaluate, torch, numpy as np

# sys.argv[1] -> dataset file (e.g. 'instances_pro.json')
# sys.argv[2] -> output dir (e.g. 'dir_model')
# sys.argv[3] -> run name for wandb (e.g. 'experiment 1')


os.environ["WANDB_PROJECT"]="gene-data"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
random.seed(1492)

#model to be used Bio-BART
checkpoint = 'GanjinZero/biobart-base'

#use GPU if available
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("DEVICE: " + device)

#initializing tokenizer
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        
#uploading data from json file
#return a DatasetDict object {'train':[], 'val':[], 'test':[]}
data = load_dataset_subsets(sys.argv[1])

#function for preprocessing (tokenizing) all instances (no padding)
def preprocess (data):
    #instances = {'inputs'=[],'targets'=[]}
    model_feed = tokenizer(data['input'], text_target=data['target'], return_tensors='pt', padding=True).to(device)
    return model_feed

#preprocessing all data
tokenized_data = data.map(preprocess, batched=True)

#Creating a batch of instances while dynamically padding them
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=checkpoint)

#function to calculate (edit distance)
metric_edit = evaluate.load('character')
metric_accuracy = evaluate.load('accuracy')
metric_chrf = evaluate.load('chrf')

def compute_metrics(eval_preds):    
    preds, labels = eval_preds
    
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens = True)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens = True)
    
    boolean_preds = np.array(decoded_preds)==np.array(decoded_labels)
    boolean_labels = np.array(decoded_labels)==np.array(decoded_labels)  
    
    result_accuracy = metric_accuracy.compute(predictions = boolean_preds, references = boolean_labels)   
    result_chrf = metric_chrf.compute(references = decoded_labels, predictions = decoded_preds, whitespace=True, char_order=3, beta=1)
    result_edit = metric_edit.compute(references = decoded_labels, predictions = decoded_preds)
    result_precision = char_precisions(references = decoded_labels, predictions = decoded_preds)
    result_recall = char_recalls(references = decoded_labels, predictions = decoded_preds)
    
    result = {'accuracy': result_accuracy['accuracy'],
              'char_F_score': result_chrf['score'],
              'edit_distance' : result_edit['cer_score'],
              'char_precision': result_precision['mean_precision'],
              'char_recall': result_recall['mean_recall']}
    result = {k: round(v, 8) for k, v in result.items()}
    
    return result

#setting up model for trainer
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint).to(device)

#defining trainer's args
training_args = Seq2SeqTrainingArguments(
    output_dir=sys.argv[2],
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    learning_rate=5e-5,
    num_train_epochs= 10,
    save_total_limit=1, #how many checkpoints to save
    metric_for_best_model= 'edit_distance',
    greater_is_better= False,
    load_best_model_at_end= True,
    predict_with_generate= True,
    report_to='wandb',
    evaluation_strategy='steps',
    save_strategy='steps',
    logging_steps=.05,
    save_steps=.05,
    run_name=sys.argv[3]
)

#defining the trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data['train'],
    eval_dataset=tokenized_data['val'],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
evaluation = trainer.evaluate(eval_dataset=tokenized_data['test'], metric_key_prefix='test')
print(evaluation)