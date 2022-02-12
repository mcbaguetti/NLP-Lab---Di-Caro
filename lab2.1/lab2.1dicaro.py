from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


def add_to_dict(dictionary, word):
    """adds a word to a dictionary or if it exists already it increments his value """

    if word not in dictionary.keys():
        dictionary.update({word: 1})
    else:
        dictionary[word] += 1


def add_to_dict2(dictionary, sentence, number):
    """adds a sentence to a dictionary with his value """

    dictionary.update({sentence: number})


def count_frequencies(words_tokenized):
    """given a list of words, it saves them in a dictionary and count them frequencies"""

    freq_dict = {}

    for word in words_tokenized:
        add_to_dict(freq_dict, word)

    return freq_dict


def sort(dictionary):
    """returns the sorted dictionary"""

    new_dict = {}

    for word in sorted(dictionary, key=dictionary.get, reverse=True):
        new_dict.update({word: dictionary[word]})

    return new_dict


def count_sent_freq(sentences, word_freq):
    """given sentences and words frequencies, it returns a dictionary with sentences as a key and a score as a value"""

    sentence_point_dict = {}

    for sentence in sentences:
        sentence_point = 0
        words_tokenized = word_tokenize(str(sentence))

        for word in words_tokenized:
            if word in word_freq:
                sentence_point += word_freq[word]

        sent = ''.join(sentence)
        add_to_dict2(sentence_point_dict, sent, sentence_point)

    return sentence_point_dict


def text_summarization(filename, lazyness):
    """given a file and a lvl of lazyness he finds the best sentences for summarizing a text"""

    list_sentences = []
    list_words = []
    summ = []
    stop_words = set(stopwords.words('english'))
    count = 0

    with open(filename, encoding="utf8") as file:

        first_line = file.readline()
        print(first_line)

        for row in file:
            sentence_tokenized = sent_tokenize(row)

            if len(sentence_tokenized) > 1:
                for single_sentence in sentence_tokenized:
                    list_sentences.append(single_sentence)
            else:
                list_sentences.append(sentence_tokenized)

    for sentence in list_sentences:
        word_tokens = word_tokenize(str(sentence))

        for w in word_tokens:
            if w not in stop_words:
                if w.isalpha():
                    list_words.append(w)

    freq_dict = count_frequencies(list_words)
    sentence_point_dict = count_sent_freq(list_sentences, freq_dict)
    sorted_sentence_point = sort(sentence_point_dict)

    for sentence in sorted_sentence_point:
        if count < lazyness:
            summ.append(sentence)
        count += 1

    for sentence in sentence_point_dict:
        if sentence in summ:
            print(sentence)
            print("\n")


text_summarization("article1.txt", 5)
