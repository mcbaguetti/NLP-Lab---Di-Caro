import spacy
import re
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

#spacy.cli.download("en_core_web_sm")


def add_to_dict(dictionary, ssubj, sobj):
    """adds a relation to diff sem_type to a dictionary or if it exists already it increments his value """

    sem_type = ssubj + " -> " + sobj

    if sem_type not in dictionary.keys():
        dictionary.update({sem_type: 1})
    else:
        dictionary[sem_type] += 1


def choose_synset(subj, obj, ambiguos, verb, pos):
    """runs and return the sysnet chosen by lesk on an ambiguos word"""

    sentence = subj + " " + verb + " " + obj
    final_syns = lesk(context_sentence=sentence, ambiguous_word=ambiguos, pos=pos)

    return final_syns


def find_sem_type(synset):
    """return lexname/semantic type"""

    return synset.lexname()


def sort(dictionary):
    """print the sorted a dictionary"""

    for sem_rel in sorted(dictionary, key=dictionary.get, reverse=True):
        print(sem_rel, dictionary[sem_rel])


def process_txt(filename, verb_chosen):
    """process a txt file and search for a verb"""

    subj = "nsubj"
    dir_obj = "dobj"
    verb_pos = "VERB"
    nlp = spacy.load("en_core_web_sm")
    sem_relations = {}
    print("the verb chosen is: " + verb_chosen)

    with open(filename, encoding="utf8") as file:

        for row in file:
            verb_founded = False
            if re.search(verb_chosen, row):
                proc_row = nlp(row)

                for token in proc_row:
                    if token.dep_ == subj:
                        subject_lemma = token.lemma_

                    if token.lemma_ == verb_chosen and token.pos_ == verb_pos:
                        verb_founded = True

                    if token.dep_ == dir_obj and verb_founded:
                        d_object_lemma = token.lemma_
                        aggr_sem_type(subject_lemma, d_object_lemma, verb_chosen, sem_relations)
                        break

        sort(sem_relations)


def aggr_sem_type(subj, obj, verb, sem_relations):
    """aggregates semantic types between subj and obj"""

    noun_tag = wn.NOUN
    subj_pron = ["I", "you", "he", "she", "we", "they", "that", "this", "everyone", "all"]
    obj_pron = ["I", "you", "he", "she", "we", "they", "me", "you", "her", "him", "us", "everyone", "all"]
    obj_pron_thing = ["that", "this", "it"]
    subj = subj.lower()
    obj = obj.lower()

    if subj in subj_pron:
        sem_type_subj = "noun.person"
    else:
        set_subj_syn = wn.synsets(subj, pos=noun_tag)

        if not set_subj_syn:
            sem_type_subj = "unknown"
            # print("subj synset not found")
            # print(subj)

        elif len(set_subj_syn) > 1:
            subj_syn = choose_synset(subj, obj, subj, verb, noun_tag)
            sem_type_subj = find_sem_type(subj_syn)
        else:
            subj_syn = set_subj_syn[0]
            sem_type_subj = find_sem_type(subj_syn)

    if obj in obj_pron:
        sem_type_obj = "noun.person"
    elif obj in obj_pron_thing:
        sem_type_obj = "noun.artifact"
    else:
        set_obj_syn = wn.synsets(obj, pos=noun_tag)

        if not set_obj_syn:
            sem_type_obj = "unknown"
            # print("obj synset not found")
            # print(obj)

        elif len(set_obj_syn) > 1:
            obj_syn = choose_synset(subj, obj, obj, verb, noun_tag)
            sem_type_obj = find_sem_type(obj_syn)

        else:
            obj_syn = set_obj_syn[0]
            sem_type_obj = find_sem_type(obj_syn)

    add_to_dict(sem_relations, sem_type_subj, sem_type_obj)


process_txt("eng_newscrawl_2018_100K-sentences.txt", "get")
