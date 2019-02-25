import numpy as np

N = 1410000000 # corpus size
# N-gram frequency
ngram_dict = {}
ngram_dict['1'] = {'하늘은': 3520000,
                   '파랗고': 392000,
                   '단풍잎은': 34600,
                   '빨갛고': 339000,
                   '은행잎은': 24300,
                   '노랗고': 359000}

ngram_dict['2'] = {'하늘은 파랗고': 56100,
                   '파랗고 단풍잎은': 23,
                   '단풍잎은 빨갛고': 160,
                   '빨갛고 은행잎은': 85,
                   '은행잎은 노랗고': 198}

ngram_dict['3'] = {'하늘은 파랗고 단풍잎은': 34,
                   '파랗고 단풍잎은 빨갛고': 0,
                   '단풍잎은 빨갛고 은행잎은': 3,
                   '빨갛고 은행잎은 노랗고': 85}

def ngram_prob(ngram, add_k):
    if '<s>' in ngram:
        return ngram_prob(ngram[1:], add_k)
    else:
        n = len(ngram)
        if n == 1:
            print('returning P(%s)' % ngram[0])
            return (ngram_dict[str(n)].get(ngram[0], 0) + add_k) / (N + add_k)
        print('RETURNING P(%s)' % ' '.join(ngram))
        return (ngram_dict[str(n)].get(' '.join(ngram), 0) + add_k) / (ngram_dict[str(n-1)].get(' '.join(ngram[:-1]), 0) + add_k)

def sentence_probability(n, sentence, add_k=1):
    sentence = ['<s>'] * (n-1) + sentence.split(' ')
    prob = 1
    for i in range(0, len(sentence) - n + 1):
        ngram = sentence[i: i + n]
        prob *= ngram_prob(ngram, add_k)
    return prob

if __name__=='__main__':
    sentence = '하늘은 파랗고 단풍잎은 빨갛고 은행잎은 노랗고'
    x = sentence_probability(1, sentence)
    print(x)
