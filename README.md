# Wordle solver (Streamlit)

A simple and crude Wordle solver built with Streamlit.
Also comes with a script that can take a wordlist that is sorted by word frequency, and scrub it so it only includes words that Wordle will allow


## To run:

Needs Streamlit to run the solver script (main.py)
```pip install streamlit```
To run - 
```streamlit run main.py```


## Wordlist Files

The solver needs a `sorted_wordlist.json` file to function
The repo includes one, but you can make a new one (if you have another list of words sorted by word frequency you want to use, or if Wordle updates their list of valid guess words, or both) using the `word_filterer.py` script

For this script you'll need a big sorted list of words called `words.txt`
I use the one from https://github.com/ScriptSmith/topwords?tab=readme-ov-file  - big thanks to Adam Smith 

You'll also need a list of valid Wordle words. I scraped the word list from the site on 11th Feb 2026 (included in this repo) and it is very comprehensive, but there are guides available to help you scrape yourself if you want the most up-to-date version.

Lists of common English words, such as those used by Wordle, are commonly considered public domain.
This package is provided without claims of authorship or warranty of any kind.