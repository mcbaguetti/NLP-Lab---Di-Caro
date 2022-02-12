import re
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk


def add_to_dict(dictionary, word):
    """adds a word to a dictionary or if it exists already it increments his value """

    if word not in dictionary.keys():
        dictionary.update({word: 1})
    else:
        dictionary[word] += 1


def sort(dictionary):
    """returns the sorted a dictionary"""

    new_dict = {}

    for word in sorted(dictionary, key=dictionary.get, reverse=True):
        new_dict.update({word: dictionary[word]})

    return new_dict


def find_sentence(word):
    """given a word, it returns the first sentence with the word"""
    words_to_analyze = 4

    with open('lab1.csv') as csv_file:
        next(csv_file)
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        for column in range(words_to_analyze + 1):
            if column != 0:
                for row in csv_reader:
                    for sentence in row:
                        if re.search(word, sentence):
                            return sentence


def choose_synset(word, sentence, set_synset):
    """chooses the right synset of the word"""

    final_syns = lesk(sentence, word, synsets=set_synset)

    #final_syns = simple_lesk(sentence, word)
    return final_syns


def search_correlation(hypo_list, diff_list):
    """searches the correlation between the differentia list and the hyponyms' definitions"""

    correlated_hypo = []

    for hypo in hypo_list:
        hypo_def = hypo.definition()
        for word in diff_list:
            if re.search(word, hypo_def):
                correlated_hypo.append(hypo)

    return correlated_hypo


def find_genus_diff(dictionary):
    """given a dictionary, it finds the more precise synsets with the genus/differentia principle"""

    genus_word = 3
    diff_word = 10
    count = 0
    genus_list = []
    diff_list = []
    final_hypo = []

    for word in dictionary:
        if genus_word > count:
            genus_list.append(word)

        elif diff_word > count:
            diff_list.append(word)

        else:
            break

        count += 1

    for genus in genus_list:
        set_synset = wn.synsets(genus)
        # print(genus)
        # print(set_synset)

        if not set_synset:
            print(str(genus) + " synset not found")
            continue

        else:
            sentence = find_sentence(genus)
            synset = choose_synset(genus, sentence, set_synset)
            # print(synset)
            hypo = synset.hyponyms()
            # print(hypo)

            if hypo:
                final_hypo.append(search_correlation(hypo, diff_list))

            else:
                print(str(synset) + " hyponym not found")

    return final_hypo


def process_sentences():
    """processes sentences, saves them in their dictionaries and given definitions search for a word"""

    courage_dict = {}
    paper_dict = {}
    apprehension_dict = {}
    sharpener_dict = {}
    words_to_analyze = 4
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    with open('lab1.csv') as csv_file:
        next(csv_file)
        csv_reader = list(csv.reader(csv_file, delimiter=','))

        for column in range(words_to_analyze + 1):
            if column != 0:
                for row in csv_reader:
                    """deals with the sentences, tokenizes, lemmatizes, eliminates stop words and punctuation """
                    sentence = row[column].lower()
                    word_tokens = word_tokenize(sentence)
                    filtered_sentence = []

                    for w in word_tokens:
                        if w not in stop_words:
                            if w.isalpha():
                                filtered_sentence.append(w)

                    for filtered_word in filtered_sentence:
                        final_word = lemmatizer.lemmatize(filtered_word)

                        if column == 1:
                            add_to_dict(courage_dict, final_word)
                        elif column == 2:
                            add_to_dict(paper_dict, final_word)
                        elif column == 3:
                            add_to_dict(apprehension_dict, final_word)
                        else:
                            add_to_dict(sharpener_dict, final_word)

        courage_dict_sorted = sort(courage_dict)
        paper_dict_sorted = sort(paper_dict)
        apprehension_dict_sorted = sort(apprehension_dict)
        sharpener_dict_sorted = sort(sharpener_dict)

        hypo_c = find_genus_diff(courage_dict_sorted)
        hypo_p = find_genus_diff(paper_dict_sorted)
        hypo_a = find_genus_diff(apprehension_dict_sorted)
        hypo_s = find_genus_diff(sharpener_dict_sorted)

        print("\n\n")
        print("from Courage definitions: ")
        print(hypo_c)
        print("\n")
        print("from Paper definitions: ")
        print(hypo_p)
        print("\n")
        print("from Apprehension definitions: ")
        print(hypo_a)
        print("\n")
        print("from Sharpener definitions: ")
        print(hypo_s)


process_sentences()
