import json
import string
import streamlit as st

def update_based_on_guess(word, colours):
    for i in range(5):
        if colours[i] == "green":
            st.session_state.green_letters[i] = word[i]
            st.session_state.greens.add(word[i])

    # yellows then greys need to be done seperately, since a green or yellow letter guessed twice
    # could show up as grey if it's only in the word once
    for i in range(5): 
        if colours[i] == "yellow":
            st.session_state.yellow_letters[i].add(word[i])
            st.session_state.yellows.add(word[i])
    for i in range(5):
        if colours[i] == "grey":
            if word[i] not in st.session_state.yellows and word[i] not in st.session_state.greens:
                st.session_state.letters.discard(word[i])
             

def find_possible_words():
    updated_words = []
    for word in st.session_state.words:
        word_is_possibility = True
        for i, letter in enumerate(word):

            if st.session_state.green_letters[i] and st.session_state.green_letters[i] != letter:
                word_is_possibility = False
                break  # if letter is green, recommendations need to have the same letter in the same spot

            if letter not in st.session_state.letters:
                word_is_possibility = False
                break  # letter is grey, cannot be in this word

            if letter in st.session_state.yellow_letters[i]:
                word_is_possibility = False
                break  # yellow letters needs to be in the word, just not in this position

        # make sure that all letters previously found to be yellow are in this word
        if word_is_possibility:
            for yellow in st.session_state.yellows:
                if yellow not in word:
                    word_is_possibility = False
                    break
            if word_is_possibility:
                updated_words.append(word)
    return updated_words
    

def percent_of_certainty(len_suggestions):
    # return a string that tell the user how sure the script is that the 5 suggestions are going to be correct
    if len_suggestions > 500:
        return "0% "
    
    certainty = (min(1, (5 / len_suggestions)) * 100)
    if certainty >= 100: 
        return "*100%* "
    certainty = int(certainty)
    return f"{str(certainty)}% "


def assign_letter_scores(words):
    # see how often each letter appears
    # higher frequency letters have higher priority when looking for probe words
    letter_scores = {letter:0 for letter in "abcdefghijklmnopqrstuvwxyz"}
    endpoint = len(words) // 2  # only do the front half of the list cos realistically, the back half is 99% garbage
    for i, word in enumerate(words[:endpoint]):
        for letter in word:
            if i < 3000:  # bonus to the most common words
                letter_scores[letter] += 15
            else:
                letter_scores[letter] += 10
    print(letter_scores)
    return letter_scores


def find_probe_word():
    # return the word that has the highest 'score'
    # score is based on how often yet-unseen letters are seen in the overall wordlist
    best_score, best_word = 0, None
    for word in words:
        score = 0
        word_set = set(word)  # remove duplicate letters
        for letter in word_set:
            if letter in st.session_state.letters and letter not in st.session_state.greens and letter not in st.session_state.yellows:
                score += st.session_state.letter_scores[letter]
        if score > best_score:
            best_score = score
            best_word = word
    return best_word


#word = input("Word: ")
#feedback = input("g for green, y for yellow, . for grey: ")
#update_based_on_guess(word, feedback)
#print(f"Guess recommendations: {find_possible_words()}")
#print()


# boilerplate
with open("sorted_wordlist.json", "r") as f:
    words = json.load(f) 

if "letters" not in st.session_state:
    st.session_state.letters = {x for x in string.ascii_lowercase}
    st.session_state.green_letters = {0: None, 1: None, 2: None, 3: None, 4: None}
    st.session_state.yellow_letters = {0: set(), 1: set(), 2: set(), 3: set(), 4: set()}
    st.session_state.yellows = set()
    st.session_state.greens = set()
    st.session_state.words = words
    st.session_state.letter_scores = assign_letter_scores(st.session_state.words)
    

st.title("WORDLE!")

with st.sidebar:
    if st.button("Reset", key="reset"):
        st.session_state.letters = {x for x in string.ascii_lowercase}
        st.session_state.green_letters = {0: None, 1: None, 2: None, 3: None, 4: None}
        st.session_state.yellow_letters = {0: set(), 1: set(), 2: set(), 3: set(), 4: set()}
        st.session_state.yellows = set()
        st.session_state.greens = set()
        st.session_state.words = words  
        st.session_state.letter_scores = assign_letter_scores(st.session_state.words)
        st.rerun()

    st.write("Your remaining letters:")
    st.write(f"{sorted(list(st.session_state.letters))}")
    st.write(f"Your current word: {st.session_state.green_letters[0] if st.session_state.green_letters[0] else '_'} {st.session_state.green_letters[1] if st.session_state.green_letters[1] else '_'} {st.session_state.green_letters[2] if st.session_state.green_letters[2] else '_'} {st.session_state.green_letters[3] if st.session_state.green_letters[3] else '_'} {st.session_state.green_letters[4] if st.session_state.green_letters[4] else '_'}")
    st.write(f"Remaining word possibilites: {len(st.session_state.words)}")


# user inputting their word and colours
user_input_word = st.text_input("What word did you try?")
user_input_word = user_input_word.lower()

st.write("What colours were the letters?")
cols = st.columns(5)
options = ["grey", "yellow", "green"]
square = {"grey": "⬛", "yellow": "🟨", "green": "🟩",}

for i, col in enumerate(cols):
    with col:
        st.selectbox("", options, key=f"letter_{i}")
        st.write(square[st.session_state[f"letter_{i}"]] * 6)

colours = [st.session_state[f"letter_{i}"] for i in range(5)]


# showing the word suggestions to the user
if st.button("Give me words!", disabled=len(user_input_word) != 5):
    update_based_on_guess(user_input_word, colours)
    
    st.divider()
    st.session_state.words = find_possible_words()  # update wordlist with new letter information
    st.session_state.letter_scores = assign_letter_scores(st.session_state.words)  # update letter scores based on remaining words

col1, col2, col3 = st.columns((2,1,2))
certainty = percent_of_certainty(len(st.session_state.words))

with col1:
    if certainty == "0% ":
        st.header("Not enough data to recommend words yet")
    else:
        st.header(f"{certainty} sure that it's one of these:")
        for word in st.session_state.words[:5]:
            st.subheader(word)
with col3:
    if certainty != "*100%* ":  # only show the probe word when the true answer hasn't been found
        st.header("To increase certainty, maybe try:")
        st.session_state.probe_word = find_probe_word()
        st.subheader(st.session_state.probe_word)

        
