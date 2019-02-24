# -*- coding: utf-8 -*-
# title: eliza.py
# course: Language and Computer
# author(s): Suzi Park
# date created: 2018-10-29
# description: ELIZA

import re, random

def respond(message):
    # preprocessing
    message = message.upper()
    message = re.sub(r'\s+', ' ', message)
    
    # generalization
    if re.match(r".*\bALL\b.*", message):
        return 'IN WHAT WAY'
    elif re.match(r".*\bALWAYS\b.*", message):
        return 'CAN YOU THINK OF A SPECIFIC EXAMPLE'
    
    # "I'm sad"
    match = re.match(r".*\bI(?: AM|'M|’M) (DEPRESSED|SAD|SICK|UNHAPPY)\b.*", message)
    if match:
        sad = match.group(1)
        responses = [
            f"I AM SORRY TO HEAR THAT YOU ARE {sad}",
            f"WHY DO YOU THINK YOU ARE {sad}",
            f"DO YOU THINK COMING HERE WILL HELP YOU NOT BE {sad}"
        ]
        return random.choice(responses)
    
    # 'desire'
    match = re.match(r".*\bI (WANT|DESIRE|NEED)\b ([\w ]+)", message)
    if match:
        thing = match.group(2)
        responses = [
            f"WHAT WOULD IT MEAN TO YOU IF YOU GOT {thing}",
            f"WHY DO YOU WANT {thing}",
            f"SUPPOSE YOU GOT {thing} SOON?",
            f"WHAT WOULD GETTING {thing} MEAN TO YOU?",
            f"WHAT DOES WANTING {thing} HAVE TO DO WITH THIS DISCUSSION?"
        ]
        return random.choice(responses)
    # 'like'
    match = re.match(r".*('M|AM|'RE|ARE|'S|IS) LIKE (.*)", message)
    if match:
        responses = [
            "IN WHAT WAY?",
            "WHAT RESEMBLANCE DO YOU SEE?",
            "WHAT DOES THAT SIMILARITY SUGGEST TO YOU?",
            "WHAT OTHER CONNECTIONS DO YOU SEE?",
            "WHAT DO YOU SUPPOSE THAT RESEMBLANCE MEANS?"
        ]
        return random.choice(responses)

    # "my"
    match = re.match(r".*\bMY (\w*)\b([^.]*)", message)
    if match:
        family = ['FATHER', 'MOTHER', 'BROTHER', 'SISTER']
        if match.group(1) in family:
            responses = [
                f"TELL ME MORE ABOUT YOUR FAMILY",
                f"YOUR {match.group(1)}",
                f"WHAT ELSE COMES TO MIND WHEN YOU THINK OF YOUR {match.group(1)}"
            ]
            if match.group(2):
                response = f"WHO ELSE IN YOUR FAMILY {match.group(2).strip()}?"
                response = re.sub(r'\bME\b', 'YOU', response)
                responses.append(response)
            return random.choice(responses)
        else:
            response = f'YOUR {match.group(1)} {match.group(2).strip()}'
            response = re.sub(r'\bME\b', 'YOU', response)
            response = re.sub(r'\bMY(SELF)?\b', r'YOUR\1', response)
            return response
    # "You are"
    match = re.match(r".*YOU ARE (.*).", message)
    if match:
        sub_match = re.match(r"(.*) (BUT|AND|OR).*", match.group(1))
        if sub_match:
            what = re.sub('ME', 'YOU', sub_match.group(1)).strip()
        else:
            what = re.sub('ME', 'YOU', match.group(1)).strip()
        responses = [
            f"WHAT MAKES YOU THINK I AM {what}?",
            f"DOES IT PLEASE YOU TO BELIEVE I AM {what}?",
        ]
        return random.choice(responses)
    
    # "You * me"
    match = re.match(r".*\bYOU (.*) ME.*", message)
    if match:
        responses = [
            f"WHY DO YOU THINK I {match.group(1)} YOU?",
            f"REALLY, I {match.group(1)} YOU?",
            f"YOU LIKE TO THINK I {match.group(1)} YOU -- DON'T YOU?",
            f"DO YOU WISH TO BELIEVE I {match.group(1)} YOU?"
        ]
        return random.choice(responses)
    # no keyword
    responses = [
        "PLEASE GO ON",
        "WHAT DOES THAT SUGGEST TO YOU",
        "I'M NOT SURE I UNDERSTAND YOU FULLY"
    ]
    return random.choice(responses)


if __name__ == '__main__':
    print('PLEASE TELL ME YOUR PROBLEM')
    with open('./eliza.txt', 'r') as fin:
        for i, msg in enumerate(fin.readlines()):
            if i % 2:
                continue
            if msg in ('', 'quit'):
                print('GOODBYE')
                break
            msg = msg.strip()
            print('> %s' % msg)
            print(respond(msg))
