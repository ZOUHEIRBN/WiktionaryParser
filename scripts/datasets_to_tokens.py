import json
import random
random.seed(222)
from collections import Counter
from .utils import *

def convert_to_tokens(dataset_name=None):
    results = builder.get_dataset(dataset_name=dataset_name)

    k = "dataset_name"  # The key for stratification

    k_counts = set(entry[k] for entry in results)
    sample_size = 5

    stratified_samples = []
    for unique_k in k_counts:
        entries_with_k = [entry for entry in results if entry.get(k) == unique_k]
        if len(entries_with_k) >= sample_size:
            entries_with_k = random.sample(entries_with_k, sample_size)
            # entries_with_k = entries_with_k[:2]


        for entry in entries_with_k:
            prepped_text = dataset_2_tokens_prep(entry.get('text'))
            # tokens = nltk.word_tokenize(prepped_text)
            entry['tokens'] = Counter(prepped_text)
            stratified_samples.append(entry)

    return stratified_samples

def get_global_token_counts(tokenized_texts):
    global_tokens = {}
    for i in range(len(tokenized_texts)):
        tokens = tokenized_texts[i]['tokens']
        for tok in tokens:
            global_tokens[tok] = global_tokens.get(tok, 0) + tokens[tok]

    global_tokens = [{
        "token": tok,
        "frequency": n
    } for tok, n in global_tokens.items()]
    global_tokens = sorted(global_tokens, key=lambda x: x.get("frequency", 0))
    return global_tokens

# stratified_samples = main()
# with open('dsInfo.json', 'w', encoding="utf8") as f:
#     f.write(json.dumps(stratified_samples, indent=4, ensure_ascii=False))
