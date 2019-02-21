import string

if __name__=='__main__':
    sentence_in = input('영어 문장> ').strip().lower()
    sentence_in = sentence_in.translate(str.maketrans('', '', string.punctuation))

    freq = {}
    for word in sentence_in.split(' '):
        freq[word] = freq.get(word, 0) + 1

    print(freq)
