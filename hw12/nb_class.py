import pickle
from random import seed, shuffle
from collections import Counter, defaultdict
from scipy import log, argmax
import numpy as np

# 1.0 Corpus Preparation
# 1.0.1 read file
with open('./poems.txt', 'r') as fin:
    data = []
    for line in fin:
        elems = line.strip().split('\t')
        data.append((int(elems[0]), int(elems[1]), [ch for ch in elems[4]]))

print(' >>> len(data)\n', len(data))
print(' >>> data[0]\n', data[0])

# 1.0.2 shuffle data
seed(471)
shuffle(data)

print(' >>> data[0]\n', data[0])

# 1.0.3 split data into train/test sets
boundary = int(len(data) * 0.9)
train = data[:boundary]
test = data[boundary:]


# 1.1 TRAIN
# 1.1.1 logprior
Ndoc = len(train)
Nc = Counter([v[1] for v in train])
logprior = {k: log(v/Ndoc) for k, v in Nc.items()}

print(' >>> Nc\n', Nc)
print(' >>> Ndoc\n', Ndoc)
print(' >>> logprior\n', logprior)

# 1.1.2 log likelihood
bigdoc  = {0:[], 1:[]}
vocabulary = []
for entry in train:
    for ch in entry[2]:
        if ch not in vocabulary:
            vocabulary.append(ch)
        if entry[1] == 0: 
            bigdoc[0].append(ch)
        if entry[1] == 1:
            bigdoc[1].append(ch)

counts = {k: Counter(v) for k, v in bigdoc.items()}

print(' >>> len(vocabulary)\n', len(vocabulary))
print(' >>> vocabulary[:14]\n', vocabulary[:14])
print(' >>> bigdoc[1][:14]\n', bigdoc[1][:14])
print(' >>> bigdoc[0][:14]\n', bigdoc[0][:14])
print(' >>> len(bigdoc[1]), len(bigdoc[0])\n',(len(bigdoc[1]), len(bigdoc[0])))
print(' >>> counts[1].most_common(5)\n', counts[1].most_common(5))
print(' >>> counts[0].most_common(5)\n', counts[0].most_common(5))
print(' >>> len(counts[1]), len(counts[0])\n', (len(counts[1]), len(counts[0])))
print(' >>> counts[1]["想"]\n', counts[1]['想'])
print(' >>> counts[0]["想"]\n', counts[0]['想'])
print(' >>> counts[1]["哀"]\n', counts[1]['哀'])
print(' >>> counts[0]["哀"]\n', counts[0]['哀'])

for ch in vocabulary:
    for cnts in counts.values():
        cnts[ch] += 1 

print(' >>> counts[1].most_common(5)\n', counts[1].most_common(5))
print(' >>> counts[0]["想"]\n', counts[0]['想'])
print(' >>> counts[1]["哀"]\n', counts[1]['哀'])
print(' >>> len(counts[1]), len(counts[0])\n', (len(counts[1]), len(counts[0])))

loglikelihood = {ch: {1: log(counts[1][ch] / (len(bigdoc[1]) + len(counts[1]))),
                      0: log(counts[0][ch] / (len(bigdoc[0])+ len(counts[0])))}
                 for ch in vocabulary}

print(' >>> loglikelihood["乡"]\n', loglikelihood['乡'])
print(' >>> loglikelihood["坐"]\n', loglikelihood['坐'])
print(' >>> loglikelihood["醉"]\n', loglikelihood['醉'])
print(' # 근심 수, 빼어날 수')
print(' >>> loglikelihood["愁"]\n', loglikelihood['愁'])
print(' >>> loglikelihood["秀"]\n', loglikelihood['秀'])

with open('./loglike.pkl', 'wb') as fout:
    pickle.dump(loglikelihood, fout)

# 1.2 EXPERIMENT
# 1.2.1 results
results = {}
for entry in test:
    neg_prob = logprior[0] + np.sum([loglikelihood[ch][0] for ch in entry[2] if ch in vocabulary])
    pos_prob = logprior[1] + np.sum([loglikelihood[ch][1] for ch in entry[2] if ch in vocabulary])
    c = argmax((neg_prob, pos_prob))
    results[entry[0]] = (entry[1], c)

print(' >>> results[111]\n', results[111])
print(' >>> results[144]\n', results[144])
print(' >>> results[14]\n', results[14])
print(' >>> results')
from pprint import pprint
pprint(results)

# 1.3 EVALUATION
# 1.3.1 accuracy
accuracy = len([0 for gt, pred in results.values() if gt == pred]) / len(results)

print(' >>> accuracy\n', accuracy)
print(' >>> accuracy > 0.8\n', accuracy > 0.8)

# 1.3.2 precision / recall
precision_pos = sum(gt and pred for gt, pred in results.values()) / sum(pred for _, pred in results.values())
recall_pos = sum(gt and pred for gt, pred in results.values()) / sum(gt for gt, _ in results.values())
precision_neg = sum(not gt and not pred for gt, pred in results.values()) / sum(not pred for _, pred in results.values())
recall_neg = sum(not gt and not pred for gt, pred in results.values()) / sum(not gt for gt, _ in results.values())

print(' >>> precision_pos\n', precision_pos)
print(' >>> recall_pos\n', recall_pos)
print(' >>> precision_neg\n', precision_neg)
print(' >>> recall_neg\n', recall_neg)

