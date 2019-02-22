from unicodedata import name, lookup

LEADING = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
VOWEL = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
TRAILING = ('',) + tuple('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')

LEADING_to_idx = {v: idx for idx, v in enumerate(LEADING)}
VOWEL_to_idx = {v: idx for idx, v in enumerate(VOWEL)}
TRAILING_to_idx = {v: idx for idx, v in enumerate(TRAILING)}

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

def decompose(syllable):
    try:
        if 'HANGUL SYLLABLE' in name(syllable):
            n_cnt = len(VOWEL) * len(TRAILING)
            t_cnt = len(TRAILING)

            s_ind = ord(syllable) - ord('가')
            l_ind = s_ind // n_cnt
            v_ind = s_ind % n_cnt // t_cnt
            t_ind = s_ind % n_cnt % t_cnt

            jamos = ''
            jamos += LEADING[l_ind]
            jamos += VOWEL[v_ind]
            jamos += TRAILING[t_ind]

            return jamos
        else:
            return syllable
    except TypeError:
        return syllable

def compose(hangul):
    try:
        base = ord('가')
        n_cnt = len(VOWEL) * len(TRAILING)
        t_cnt = len(TRAILING)
        if len(hangul) == 2:
            l, v = hangul
            idx = base + (LEADING_to_idx[l] * n_cnt) + (VOWEL_to_idx[v] * t_cnt)
            return chr(idx)
        elif len(hangul) == 3:
            l, v, t = hangul
            idx = base + (LEADING_to_idx[l] * n_cnt) + (VOWEL_to_idx[v] * t_cnt) + TRAILING_to_idx[t]
            return chr(idx)
        else:
            return hangul
    except:
        return hangul
