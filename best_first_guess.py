import json
from collections import defaultdict

def guess_eval(guess, answer):
    result = [None, None, None, None, None]  # 2:green, 1:yellow, 0:grey
    potential_yellows = []

    # pass 1 - easy green and greys
    for i, c in enumerate(answer):
        if c == guess[i]:  # green - letters match
            result[i] = "2"
        elif c in (guess[:i] + guess[i+1:]):  # this letter has been guessed somewhere else in the word
            potential_yellows.append(c)  
        
    # pass 2 - yellows
    # done in a seperate pass to avoid situations where the guess has a letter more times than the answer
    # and could potentially get marked as yellow too many times 
    for i, c in enumerate(guess):
        if result[i] is not None:
            continue  # marked this letter on the first pass
        if c in potential_yellows:
            result[i] = "1"  # yellow - letter is in the answer, but somewhere else
            potential_yellows.remove(c)
        else:
            result[i] = "0"  # grey - this letter *is* somewhere else in the word but has already been marked 

    return "".join(result)


with open("all_allowed_wordle_answers.json", "r") as f:
    wordlist = json.load(f)

scores = []
wordlist_length = len(wordlist)
percent = 0
print("0% complete", end="")
for i, guess in enumerate(wordlist):  # try every word as a first guess...
    evals = defaultdict(int)
    for answer in wordlist:  # ...against every other word
        evals[guess_eval(guess, answer)] += 1  # keep track of how many times each result is output

    # lower score is better, since it means each possible result is closer to being equally likely
    # if there's a result that's way more likely than all the others, it's a bad starting word
    # since it doesn't cut the potential words down very much
    score = 0
    for evaluation in evals.values():
        score += (evaluation*evaluation)  
    scores.append((guess, score))

    # code for a progress bar, since it's quite slow
    percent = (i * 100) // wordlist_length
    print(f"\r{percent}% complete  ", end="")

scores = sorted(scores,key =lambda pair:pair[1])
print()
print("Top 10:")
for score in scores[:10]:
    print(f"{score[0]}: {score[1]}")

