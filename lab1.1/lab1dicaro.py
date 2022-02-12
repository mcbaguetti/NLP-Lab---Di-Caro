import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def add_to_dict(dictionary, word):
    """adds a word to a dictionary or if it exists already it increments his value """

    if word not in dictionary.keys():
        dictionary.update({word: 1})
    else:
        dictionary[word] += 1


def divide_by_frequency(dictionary, sum):
    """divides a key dictionary by the sum of all the key's values and return the dictionary"""

    for word in dictionary:
        dictionary[word] /= sum
    return dictionary


def calc_avg(dict):
    """makes the avg of the top n words with the dict's highest percentage"""

    top_words = 3
    total = 0

    keys = sorted(dict, key=dict.get, reverse=True)[:top_words]

    for key in keys:
        total += dict[key]

    similarity = total / top_words

    return similarity


def calc_sim():
    """calculates the similarity of the words for each key word"""

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
            tot_len_sentences = 0
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

                    tot_len_sentences += len(filtered_sentence)

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

    courage_dict = divide_by_frequency(courage_dict, sum(courage_dict.values()))
    paper_dict = divide_by_frequency(paper_dict, sum(paper_dict.values()))
    apprehension_dict = divide_by_frequency(apprehension_dict, sum(apprehension_dict.values()))
    sharpener_dict = divide_by_frequency(sharpener_dict, sum(sharpener_dict.values()))

    courage_sim = calc_avg(courage_dict)
    paper_sim = calc_avg(paper_dict)
    appr_sim = calc_avg(apprehension_dict)
    sharp_sim = calc_avg(sharpener_dict)

    print("The similarity of courage (generic, abstract) is " + str(courage_sim))
    print("The similarity of paper (generic, real) is " + str(paper_sim))
    print("The similarity of apprehension (specific, abstract) is " + str(appr_sim))
    print("The similarity of sharpener (specific, real) is " + str(sharp_sim))


calc_sim()
