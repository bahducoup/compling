def numeral(string):
    res = ''
    for ch in string:
        if ch in '0123456789':
            res += ch
    if res:
        return int(res)

def count_by_genre(filename):
    genres = ['빈도', '개수', '교재', '교과', '교양',
              '문학', '신문', '잡지', '대본', '구어', '기타']
    with open(filename, 'r') as f_in:
        count = {}
        for line in f_in:
            tkns = line.strip().split('\t')
            count[tkns[1]] = dict(zip(genres, [numeral(tkn) for tkn in tkns[2:]]))
    return count

def print_magazines(count):
    for k, v in count.items():
        if v['잡지'] and v['잡지'] > 50:
            print('%s %d' % (k, v['잡지']))

def serialize(count):
    with open('./counts_00000.pkl', 'wb') as f_out:
        import pickle
        f_out.write(pickle.dumps(count))

if __name__=='__main__':
    fname = './proper_nouns.txt'
    count = count_by_genre(fname)
    print_magazines(count)
    serialize(count)
