from collections import Counter
import numpy as np

def get_character_ngrams(text, n=1):
    """
    Generate character n-grams from a given text.
    
    Args:
        text (str): The input text.
        n (int): The n-gram length.
        
    Returns:
        Counter: A Counter object with n-grams and their counts.
    """
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return Counter(ngrams)

def char_precisions(references, predictions, max_n=3):
    """
    Calculate character-level precision for n-grams up to max_n across multiple references and hypotheses.
    
    Args:
        references (list of str): The list of reference strings.
        hypotheses (list of str): The list of hypothesis strings.
        max_n (int): The maximum n-gram length.
        
    Returns:
        list of float, float: List of precision scores for each pair and the average precision score.
    """
    precisions = []
    for reference, hypothesis in zip(references, predictions):
        precisions_for_pair = []
        for n in range(1, max_n + 1):
            ref_ngrams = get_character_ngrams(reference, n)
            hyp_ngrams = get_character_ngrams(hypothesis, n)
            matches = sum(min(ref_ngrams[gram], hyp_ngrams[gram]) for gram in hyp_ngrams)
            total = sum(hyp_ngrams.values())
            precision = matches / total if total > 0 else 0
            precisions_for_pair.append(precision)
        precisions.append(np.mean(precisions_for_pair))
    average_precision = np.mean(precisions)
    return {'scores': precisions, 'mean_precision': average_precision}

def char_recalls(references, predictions, max_n=3):
    """
    Calculate character-level recall for n-grams up to max_n across multiple references and hypotheses.
    
    Args:
        references (list of str): The list of reference strings.
        hypotheses (list of str): The list of hypothesis strings.
        max_n (int): The maximum n-gram length.
        
    Returns:
        list of float, float: List of recall scores for each pair and the average recall score.
    """
    recalls = []
    for reference, hypothesis in zip(references, predictions):
        recalls_for_pair = []
        for n in range(1, max_n + 1):
            ref_ngrams = get_character_ngrams(reference, n)
            hyp_ngrams = get_character_ngrams(hypothesis, n)
            matches = sum(min(ref_ngrams[gram], hyp_ngrams[gram]) for gram in hyp_ngrams)
            total = sum(ref_ngrams.values())
            recall = matches / total if total > 0 else 0
            recalls_for_pair.append(recall)
        recalls.append(np.mean(recalls_for_pair))
    average_recall = np.mean(recalls)
    return {'scores': recalls, 'mean_recall': average_recall}