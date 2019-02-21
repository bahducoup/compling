from unicodedata import name

def ishangul(string):
    for ch in string:
        if 'HANGUL' in name(ch):
            continue
        else:
            return False
    return True

def hasbatchim(syllable):
    syllable_name = name(syllable)
    if 'HANGUL' not in syllable_name:
        return
    vowels = ['a', 'e', 'i', 'o', 'u']
    return syllable_name[-1].lower() not in vowels

def get_ga(hangul):
    hb = hasbatchim(hangul[-1])
    if hb != None:
        if hb:
            return '이'
        else:
            return '가'
    else:
        return

if __name__=='__main__':
    l1 = ['파이썬', 'Python', '파이썬3']
    l2 = ['P', '파', '이', '썬']
    l3 = ['수박', '복숭아']

    for word in l1:
        print("ishangul('%s') :: %s" % (word, ishangul(word)))
    print()
    for syllable in l2:
        print("hasbatchim('%s') :: %s" % (syllable, hasbatchim(syllable)))
    print()
    for word in l3:
        print('%s%s 달다.' % (word, get_ga(word)))
