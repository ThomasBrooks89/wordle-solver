import json
import string

# open the wordlist taken directly from https://www.nytimes.com/games/wordle/index.html
# these are all the words Wordle will accept as answers
with open("all_allowed_wordle_answers.json", "r") as f:
    wordle_allowed = json.load(f)

# open the wordlist taken from https://github.com/ScriptSmith/topwords?tab=readme-ov-file
# this is a list of the top 3 million+ words in the English language, sorted by frequency
topwords = []
with open("words.txt", "r") as f:
    for line in f:
        topwords.append(line.strip())

# we only want 5 letter words
topwords_5 = []
for word in topwords:
    if len(word) == 5:
        candidate = True
        for char in word:
            if char not in string.ascii_letters:
                candidate = False  # only want words with no punctuation
                break
        if candidate:
            topwords_5.append(word)

# we only want words that Wordle will accept as valid inputs
wordle_allowed_set = set(wordle_allowed)
final_wordlist = []
for word in topwords_5:
    if word in wordle_allowed_set:
        final_wordlist.append(word)

# weirdly, there are about a thousand words that wordle accepts 
# but aren't in the massive wordlist I found
# need to get them to add them back
wordlist_set = set(final_wordlist)
missing_words = []
for word in wordle_allowed:
    if word not in wordlist_set:
        missing_words.append(word)
# they mostly seem to be:
# nonsense or obselete: "meffs", "aapas", "sdein" - certain not to be a solution 
# slang: "ahole", "lezza", "loled" - certain not to be a solution
# fairly new tech words - "inbox", "vapes" - actual chance to be a solution

# it's not perfect, but since so many of the missing words are duds
# it seems safe to just append them to the end
final_wordlist += missing_words
with open("sorted_wordlist.json", "w") as f:
    json.dump(final_wordlist, f, indent = 1)

