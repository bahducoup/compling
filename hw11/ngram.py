import numpy as np

# corpus size
N = 1410000000

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
            prob = (ngram_dict[str(n)].get(ngram[0], 0) + add_k) / (N + len(ngram_dict[str(n)]) * add_k)
            print('P(%s): %.32f' % (ngram[0], prob))
            return prob
        prob = (ngram_dict[str(n)].get(' '.join(ngram), 0) + add_k) / (ngram_dict[str(n-1)].get(' '.join(ngram[:-1]), 0) + add_k)
        print('P(%s): %.32f' % (' '.join(ngram), prob))
        return prob

def sentence_probability(n, sentence, add_k=0):
    sentence = ['<s>'] * (n-1) + sentence.split(' ')
    prob = 1
    for i in range(0, len(sentence) - n + 1):
        ngram = sentence[i: i + n]
        prob *= ngram_prob(ngram, add_k)
    return prob

def perplexity(probability, sentence):
    k = len(sentence.split(' '))
    return probability ** (-1/k)

def trigram_interpolation(sentence, weights):
    print('weights: %s\n' % str(weights))
    sentence = ['<s>'] * 2 + sentence.split(' ')
    prob = 1
    for i in range(0, len(sentence) - 2):
        tri, bi, uni = sentence[i:i+3], sentence[i+1:i+3], sentence[i+2:i+3]
        model_probs = ngram_prob(tri, 0), ngram_prob(bi, 0), ngram_prob(uni, 0)
        print('weighted probability of %s: %.32f\n' % (" ".join(tri), np.sum([p*w for p, w in zip(model_probs, weights)])))
        prob *= np.sum([p*w for p, w in zip(model_probs, weights)])
    return prob

if __name__=='__main__':
    sentence = '하늘은 파랗고 단풍잎은 빨갛고 은행잎은 노랗고'
    print('=======================================================')
    unigram_prob = sentence_probability(1, sentence)
    print('\n>> UNIGRAM:')
    print('         PROBABILITY:', unigram_prob)
    print('         PERPLEXITY:', perplexity(unigram_prob, sentence))
    print('=======================================================')
    bigram_prob = sentence_probability(2, sentence)
    print('\n>> BIGRAM:')
    print('         PROBABILITY:', bigram_prob)
    print('         PERPLEXITY:', perplexity(bigram_prob, sentence))
    print('=======================================================')
    trigram_prob = sentence_probability(3, sentence)
    print('\n>> TRIGRAM:')
    print('         PROBABILITY:', trigram_prob)
    print('         PERPLEXITY:', perplexity(trigram_prob, sentence))
    print('=======================================================')
    trigram_itp = trigram_interpolation(sentence, (0.5, 0.3, 0.2))
    print('\n>> TRIGRAM INTERPOLATION:')
    print('         PROBABILITY:', trigram_itp)
    print('         PERPLEXITY:', perplexity(trigram_itp, sentence))
    print('=======================================================')
    trigram_itp = trigram_interpolation(sentence, (0.7, 0.2, 0.1))
    print('\n>> TRIGRAM INTERPOLATION:')
    print('         PROBABILITY:', trigram_itp)
    print('         PERPLEXITY:', perplexity(trigram_itp, sentence))

