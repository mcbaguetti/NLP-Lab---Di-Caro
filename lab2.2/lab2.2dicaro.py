import pandas as pd
from gensim import corpora, models, utils, parsing


def generate_topic(filename_training):

    parsed_txt = []
    first_interr = ", '"
    second_interr = '" + '
    third_interr = '*"'
    list_topics = []
    lda_file = "ldamodel.p"

    # extracts text and w/ lambda tokenize all the text saved in the dataframe txt
    txt = pd.read_csv(filename_training, usecols=['headline_text'])
    tokenized_txt = txt.apply(lambda row: utils.simple_preprocess(row['headline_text']), axis=1)

    # preprocess text
    for sent in tokenized_txt:
        processed = parsing.preprocessing.remove_stopword_tokens(sent)
        parsed_txt.append(processed)

    # creation of dict and corpus
    id2word = corpora.Dictionary(parsed_txt)
    corpus = [id2word.doc2bow(text) for text in parsed_txt]

    # training
    lda = models.LdaModel(corpus, id2word=id2word, num_topics=10, passes=2)

    # save the model
    # lda.save(lda_file)

    # get top 10 topics
    topics = lda.print_topics()

    for topic in topics:
        print(topic)

    """ topic_name = str(topic).split(first_interr, 1)[0]

        other = str(topic).split(first_interr, 1)[1]
        other2 = other.split(second_interr, 1)

        num_list = []
        word_list = []

        for elem in other2:
            num = float(elem.split(third_interr)[0])
            word = elem.split(third_interr)[1]

            num_list.append(num)
            word_list.append(word)"""


generate_topic("abcnews-date-text.csv")
