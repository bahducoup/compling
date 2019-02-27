from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn import metrics

# read data file
with open('./train.txt', 'r') as fin:
    data = [line.strip().split('\t') for line in fin]

# split data set into test(10) / dev(10) / train(80)
boundary = int(len(data) * 0.1)

test = data[:boundary]
dev = data[boundary:boundary*2]
train = data[boundary*2:]

# train set
cat_to_idx = {'hate': 0, 'offensive': 1, 'non-offensive':2}
idx_to_cat = {v: k for k, v in cat_to_idx.items()}

y = [cat_to_idx[item[0]] for item in train]
docs_train = [item[1] for item in train]

vectorizer = CountVectorizer(input='content', lowercase=False)
X = vectorizer.fit_transform(docs_train) #shape: (17600, 32835)

# dev set
def print_dev(vectorizer, clf):
    gold_dev = [cat_to_idx[item[0]] for item in dev]
    docs_dev = [item[1] for item in dev]
    mat_dev = vectorizer.transform(docs_dev)
    predicted_dev = clf.predict(mat_dev)
    
    #print(np.transpose(np.concatenate([[gold_dev], [predicted_dev]])))
    #print(metrics.confusion_matrix(gold_dev, predicted_dev))
    print(f'Accuracy: {np.mean(gold_dev == predicted_dev)}')
    print(metrics.classification_report(gold_dev, predicted_dev))
    print('==========================================================')

# train classifier: Naive Bayes
print('NB yes smoothing')
clf = MultinomialNB()
clf.fit(X, y)
print_dev(vectorizer, clf)

# NaiveBayes without smoothing
print('NB no smoothing')
clf = MultinomialNB(alpha=0)
clf.fit(X, y)
print_dev(vectorizer, clf)

# train classifier: Logistic Regression
print('Logistic Regression')
clf = LogisticRegression()
clf.fit(X, y)
print_dev(vectorizer, clf)

vectorizer2 = CountVectorizer(input='content', lowercase=False, ngram_range=(1, 2))
X2 = vectorizer2.fit_transform(docs_train)

# Naive Bayes
print('NB with bigrams')
clf = MultinomialNB()
clf.fit(X2, y)
print_dev(vectorizer2, clf)

print('LR with bigrams')
clf = LogisticRegression()
clf.fit(X2, y)
print_dev(vectorizer2, clf)

vectorizer3 = CountVectorizer(input='content', lowercase=False, ngram_range=(1, 3))
X3 = vectorizer3.fit_transform(docs_train)
print('NB with trigrams')
clf = MultinomialNB()
clf.fit(X3, y)
print_dev(vectorizer3, clf)

print('LR with trigrams')
clf = LogisticRegression()
clf.fit(X3, y)
print_dev(vectorizer3, clf)


# Best: Logistic Regression with trigrams
gold_test = [cat_to_idx[item[0]] for item in test]
docs_test = [item[1] for item in test]
mat_test = vectorizer3.transform(docs_test)

clf = LogisticRegression()
clf.fit(X3, y)
predicted_test = clf.predict(mat_test)


#print(np.transpose(np.concatenate([[gold_test], [predicted_test]])))
#print(metrics.confusion_matrix(gold_test, predicted_test))
print(f'Accuracy: {np.mean(gold_test==predicted_test)}')
print(metrics.classification_report(gold_test, predicted_test))

import pickle
with open('classifier_김영민.pkl', 'wb') as fout:
    pickle.dump(clf, fout)
