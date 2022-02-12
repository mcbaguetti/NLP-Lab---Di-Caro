import csv
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk import WordNetLemmatizer


def add_to_dict(dictionary, word):
    """adds a word to a dictionary or if it exists already it increments his value """

    if word not in dictionary.keys():
        dictionary.update({word: 1})
    else:
        dictionary[word] += 1


def add_to_nested_dict(dictionary, concept, feature, frequency):
    """adds a concept, feature and frequency to a nested dictionary"""

    if concept not in dictionary.keys():
        dictionary.update({concept: {feature: frequency}})
    else:
        dictionary[concept].update({feature: frequency})


def add_to_final_dict(dictionary, definition):
    """adds a definition for every word if it isn't already added"""

    if definition not in dictionary['property_norms']:
        dictionary['property_norms'].append(definition)


def find_pnorms(file_name):
    """finds words with the property norms and their frequencies"""

    pnorms_dict = {}
    concept = 2
    feature = 3
    frequency = 4

    with open(file_name) as csv_file:
        next(csv_file)
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        for row in csv_reader:
            add_to_nested_dict(pnorms_dict, row[concept], row[feature], row[frequency])

    return pnorms_dict


def lesk(word, sentence):
    sense = ''
    max_overlap = -1

    # Si cicla su ogni possibile synset della parola
    for synset in wn.synsets(word):

        # Si trasforma in un set di token ogni definizione di ogni synset
        synset_definition = set(synset.definition().split())
        #print(f"{synset} \n Definizione del synset: {synset_definition}\n" )

        # Si cicla su ogni esempio disponibile per il synset
        for example in synset.examples():

            # Si aggiorna la definizione aggiungendone gli esempi
            synset_definition.update(example.split())
            #print(f"{synset} \n Definizione: {synset_definition} \n Esempio: {example}\n")
        # Con le definizioni arricchite dagli esempi si valuta quante parole si incrociano con il contesto
        overlap = len(sentence and synset_definition)

        # La definizione con più overlapping sarà l'output
        if overlap > max_overlap:
            sense = synset
            max_overlap = overlap

    return sense


def choose_synset(word, nested_dict):
    """returns the right synset for a word"""

    syns_dict = {}
    #print(word)

    for sentence in nested_dict:
        c_sent = word_tokenize(word + ' ' + sentence)
        final_syns = lesk(word, c_sent)
        add_to_dict(syns_dict, final_syns)
        #print(c_sent)
        #print(final_syns)

    #max_def = max(syns_dict, key=syns_dict.get)
    #print(max_def.definition())

    return max(syns_dict, key=syns_dict.get)


def process_synset(synset):
    """returns the synset without stopwords, punctuations"""

    processed = []
    desired_tag = ['NN', 'JJ', 'JJR', 'JJS', 'NNS', 'NNPS', 'NNP', 'VBG', 'VBN', 'VB', 'VBD', 'VBP', 'VBZ']
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = list(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    tokens = tokenizer.tokenize(synset.definition())
    removed_stopwords = [w for w in tokens if w not in stop_words]
    word_tagged = pos_tag(removed_stopwords)
    for word in word_tagged:
        if word[1] in desired_tag:
            processed.append(lemmatizer.lemmatize(word[0]))

    return processed


def process_pnorms(nested_dict):
    """returns the processed property norms"""

    processed = []
    min_freq = 5
    desired_tag = ['NN', 'JJ', 'JJR', 'JJS', 'NNS', 'NNPS', 'NNP', 'VBG']
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = list(stopwords.words('english'))

    for sentence in nested_dict:
        if int(nested_dict[sentence]) > min_freq:
            tokens = tokenizer.tokenize(sentence)
            removed_stopwords = [w for w in tokens if w not in stop_words]
            word_tagged = pos_tag(removed_stopwords)

            for word in word_tagged:
                if word[1] in desired_tag:
                    processed.append(word[0])

    return processed


def link_resources():
    """links the property norms with the right synset"""

    pnorms_dict = find_pnorms("pnorms.csv")
    noun_tag = wn.NOUN
    final_resource = {}

    for word in pnorms_dict:
        set_of_syns = wn.synsets(word, pos=noun_tag)

        if not set_of_syns:
            print("synset not found")
            continue
        elif len(set_of_syns) > 1:
            synset = choose_synset(word, pnorms_dict[word])
        else:
            synset = set_of_syns[0]

        processed_synset = process_synset(synset)
        processed_pnorms = process_pnorms(pnorms_dict[word])

        #print(processed_synset)
        #print(processed_pnorms)

        final_resource.update({word: {'std_definition': synset.definition(), 'property_norms': []}})

        for pnorms in processed_pnorms:
            if pnorms not in processed_synset:
                add_to_final_dict(final_resource[word], pnorms)

    print(final_resource)


link_resources()
