#!/usr/bin/env python3
from collections import Counter

def getWordList():
    wordsFile = '/usr/share/dict/words'

    with open(wordsFile, 'r') as f:
        words = list(f)
        words = {w.strip().lower() for w in words
                 if len(w.strip()) == 5 and w[0].islower()}
        print("Total num words:", len(words))
        return words
    assert False, "Should not come here"

def wordScore(counts, word):
    word = set(word)
    return sum([counts[c] for c in word])

def playTurn():
    while True:
        wordPlayed = input("Enter word played: ")
        hints = input("Enter the hints (xyg): ")
        if len(wordPlayed) != 5 or len(hints) != 5:
            continue
        confirm = input("Confirm y/n?: ")
        if confirm != 'y':
            continue
        return (wordPlayed, hints)

def eliminateWords(words, wordPlayed, hint):
    absentLetters = {c for i,c in enumerate(wordPlayed) if hint[i] == 'x'}
    fullCorrectLetters = {c : i for i,c in enumerate(wordPlayed) if hint[i] == 'g'}
    halfCorrectLetters = {c : i for i,c in enumerate(wordPlayed) if hint[i] == 'y'}
    toDelete = set()
    for word in words:
        if set(word) & absentLetters:
            toDelete.add(word)
        for c, i in fullCorrectLetters.items():
            if word[i] != c:
                toDelete.add(word)
        for c, i in halfCorrectLetters.items():
            if word[i] == c or c not in word:
                toDelete.add(word)
    return words - toDelete

def main():
    words = getWordList()
    counts = Counter()
    for w in words:
        counts.update(w)

    while True:
        # Assign scores
        scores = [(w, wordScore(counts, w)) for w in words]
        scores.sort(key=lambda x: x[1])
        print("Num words: ", len(words))
        print("Top words: ", scores[-10:] if len(scores) >= 10 else scores)
        (wordPlayed, hint) = playTurn()
        words = eliminateWords(words, wordPlayed, hint) 
         
if __name__ == '__main__':
    main()
