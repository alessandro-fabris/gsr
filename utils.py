import numpy as np
import string
from string import punctuation
from scipy.stats.stats import pearsonr, linregress
import we
import json
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer
import krovetz
import math
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES


# toy collections
TOPICS_PATH_TOY1 = "./data/toy/1/topics/"
CORPUS_PATH_TOY1 = "./data/toy/1/corpus/"
QRELS_FILE_TOY1_STEREO = './data/toy/1/qrels/stereo.qrel'
QRELS_FILE_TOY1_ANTISTEREO = './data/toy/1/qrels/antistereo.qrel'
QRELS_FILE_TOY1_NEUTRAL = './data/toy/1/qrels/neutral.qrel'

TOPICS_PATH_TOY2 = "./data/toy/2/topics/"
CORPUS_PATH_TOY2 = "./data/toy/2/corpus/"
QRELS_FILE_TOY2_STEREO = './data/toy/2/qrels/stereo.qrel'
QRELS_FILE_TOY2_ANTISTEREO = './data/toy/2/qrels/antistereo.qrel'
QRELS_FILE_TOY2_NEUTRAL = './data/toy/2/qrels/neutral.qrel'

STOPWORDS_FILE = "./data/indri_stoplist_eng.txt"
DEFINITIONAL_PAIRS_FILE = "./data/definitional_pairs.json"


# real collections
SOME_PATH = "Change me to something appopriate"

TOPICS_PATH_ROBUST = SOME_PATH
QRELS_FILE_ROBUST = SOME_PATH
CORPUS_PATH_ROBUST = SOME_PATH

TOPICS_PATH_NY = SOME_PATH
QRELS_FILE_NY = SOME_PATH
CORPUS_PATH_NY = SOME_PATH


kstemmer = krovetz.PyKrovetzStemmer()
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)


def get_corpus_path(collection):
    if collection == "robust":
        return CORPUS_PATH_ROBUST
    elif collection == "ny":
        return CORPUS_PATH_NY
    elif collection == "toy1":
        return CORPUS_PATH_TOY1
    elif collection == "toy2":
        return CORPUS_PATH_TOY2
    else:
        raise NameError

def get_topics_path(collection):
    if collection == "robust":
        return TOPICS_PATH_ROBUST
    elif collection == "ny":
        return TOPICS_PATH_NY
    elif collection == "toy1":
        return TOPICS_PATH_TOY1
    elif collection == "toy2":
        return TOPICS_PATH_TOY2
    else:
        raise NameError

def get_qrels_path(collection, type=None):
    if collection == "robust":
        return QRELS_FILE_ROBUST
    elif collection == "ny":
        return QRELS_FILE_NY
    elif collection == "toy1":
        if type == "stereo":
            return QRELS_FILE_TOY1_STEREO
        elif type == "antistereo":
            return QRELS_FILE_TOY1_ANTISTEREO
        elif type == "neutral":
            return QRELS_FILE_TOY1_NEUTRAL
    elif collection == "toy2":
        if type == "stereo":
            return QRELS_FILE_TOY2_STEREO
        elif type == "antistereo":
            return QRELS_FILE_TOY2_ANTISTEREO
        elif type == "neutral":
            return QRELS_FILE_TOY2_NEUTRAL
    else:
        raise NameError

def qid2q(qid, collection):
    p = get_topics_path(collection)
    file_name = p+"/"+str(qid)+".txt"
    with open(file_name, "r", encoding='utf8') as f:
        out = f.read().replace('\n', '')
    return out

def load_stopwords(fpath=STOPWORDS_FILE):
    sws = []
    for line in open(fpath, 'r'):
        sws.append(line.strip())
    return sws

def qid_to_avg_genderedness(collection, qid, E, gender_dir, sw_file=STOPWORDS_FILE, func_keep_word=None):
    full_path = get_topics_path(collection) + qid + ".txt"
    return txt_file_avg_genderedness(full_path, E, gender_dir, sw_file=sw_file, func_keep_word=func_keep_word)

def docid_to_avg_genderedness(collection, docid, E, gender_dir, sw_file=STOPWORDS_FILE,
                              func_keep_word=None, w2gend=None):
    full_path = get_corpus_path(collection) + docid + ".txt"
    return txt_file_avg_genderedness(full_path, E, gender_dir, sw_file=sw_file, func_keep_word=func_keep_word,
                                     w2gend=w2gend)

def txt_file_avg_genderedness(file_name, E, gender_dir, sw_file=STOPWORDS_FILE, verbose=False, func_keep_word=None, w2gend=None):
    keep_gendered_sws = True
    text = ' '.join(open(file_name, 'r').readlines())
    sw = load_stopwords(sw_file)
    if keep_gendered_sws:
        keep = ["mrs", "ms", "she", "her", "hers", "herself", "mr", "he", "his", "himself"]
        sw = [w for w in sw if w not in keep]
    words = tokenize(text, stemming=False, stoplist=sw)
    genderedness = 0
    exclude = set(punctuation)
    w_count = 0
    if len(words) == 0:
        return float('nan')
    for word in words:
        word = ''.join(ch for ch in word if ch not in exclude)
        if func_keep_word is None or func_keep_word(word):
            try:
                if w2gend is None:
                    genderedness += gender_dir.dot(E.v(word))
                else:
                    genderedness += w2gend[word]
                w_count += 1
            except KeyError:
                if verbose:
                    print(word+" not in E")
    if w_count == 0:
        if verbose:
            print("No genderedness info for text: " + text)
        return float('nan')
    else:
        return genderedness / w_count

def compute_gender_dir(E, definitional_filename=DEFINITIONAL_PAIRS_FILE):
    with open(definitional_filename, "r") as f:
        defs = json.load(f)
    gender_dir = we.doPCA(defs, E).components_[0]
    return gender_dir

def contains_digits(token):
    for c in token:
        if c.isdigit():
            return True
    return False

def tokenize(text, stemming=True, stoplist=None):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
    text = text.translate(translator)
    text = text.lower()
    text = text.strip()
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)
    if stemming:
        analyzer = StemmingAnalyzer(stoplist=stoplist, minsize=2, stemfn=kstemmer.stem)
    else:
        analyzer = StandardAnalyzer(stoplist=stoplist, minsize=2)

    tokens = [token.text for token in analyzer(text)]
    tokens = [word for word in tokens if not contains_digits(word)]
    return tokens

def remove_idcs_from_list(l, idcs):
    out = [val for idx, val in enumerate(l) if idx not in idcs]
    return out

def q_id_to_rel_docs(collection, type=None):
    qrels_file = get_qrels_path(collection, type=type)
    d = {}
    s = {}
    with open(qrels_file, "r", encoding='utf8') as f:
        for line in f:
            q_id, placeholder, doc_id, relevant = line.split()
            if int(relevant) > 0:
                if q_id not in d:
                    d[q_id] = []
                    s[q_id] = []
                d[q_id].append(doc_id)
                s[q_id].append(int(relevant))
    return d, s

def nan_corr(v1, v2, verbose=False):
    idcs_1_nan = [i for i, val in enumerate(v1) if math.isnan(val)]
    idcs_2_nan = [i for i, val in enumerate(v2) if math.isnan(val)]
    idcs_remove = idcs_1_nan + idcs_2_nan
    vals1 = remove_idcs_from_list(v1, idcs_remove)
    vals2 = remove_idcs_from_list(v2, idcs_remove)
    if verbose and len(idcs_remove) > 0:
        print("nan_corr() found " + str(len(idcs_remove)) + " nans")
    slope, intercept, r_value, p_value, std_err = linregress(vals1, vals2)
    return r_value, p_value, slope, intercept

def word_in_list(w, lst, lemmatize=False):
    if lemmatize:
        lemmas = lemmatizer(w, u'NOUN')
        all_lemmas = []
        for l in lemmas:
            all_lemmas.extend([l.lower(), l.upper(), l.title()])
        for word in lst:
            if any([w_ in lemmatizer(word, u'NOUN') for w_ in all_lemmas]):
                return True
        return False
    else:
        return any([w_ in lst for w_ in [w.lower(), w.upper(), w.title()]])


def dirness_q_and_docs_from_we(collection, q_id_to_rel_docs, E, dir, disc=False, q_id_to_scores=None, verbose=False,
                               w2gend=None, exclude_query_terms=True):
    """ compute average projection of queries and documents along direction dir
    """
    genderness_q = []
    genderness_docs = []
    lemmatize = True
    for i, qid in enumerate(q_id_to_rel_docs):
        if verbose:
            print(str(i) + "/" + str(len(q_id_to_rel_docs)))
        gq = qid_to_avg_genderedness(collection, qid, E, dir, func_keep_word=None)
        genderness_q.append(gq)
        if exclude_query_terms:
            query = qid2q(qid, collection)
            lst = query.translate(str.maketrans('', '', string.punctuation)).split()
            func = lambda w: not word_in_list(w, lst, lemmatize=lemmatize)
        else:
            func = None
        g_docs = [docid_to_avg_genderedness(collection, docid, E, dir, func_keep_word=func, w2gend=w2gend) for
                  docid in q_id_to_rel_docs[qid]]
        idcs_nan = [i for i, g in enumerate(g_docs) if math.isnan(g)]
        if len(idcs_nan) > 0.01 * len(g_docs):
            raise ValueError
        if disc:
            if q_id_to_scores is None:
                # normally we assume qid_to_rel_docs to be ordered with no ties
                weights = [1 / max(1, np.log2(i + 1)) for i in range(len(g_docs))]
                weights = np.array(weights) / sum(weights)
            else:
                # if not, we can specify q_id_to_scores, consistent with qid_to_rel_docs
                scores = [s for i, s in enumerate(q_id_to_scores[qid]) if i not in idcs_nan]
                assert (len(scores) == len(g_docs))
                uniq_scores = sorted(list(set(scores)), reverse=True)
                score_to_num_docs_better_rank = {s: sum([1 for s_ in scores if s_ > s]) for s in uniq_scores}
                weights = [1 / max(1, np.log2(score_to_num_docs_better_rank[s] + 1)) for s in scores]
                weights = np.array(weights) / sum(weights)
        else:
            weights = np.ones_like(g_docs) / len(g_docs)
        assert (np.isclose(sum(weights), 1))
        genderness_docs.append(np.array(g_docs).dot(weights))
    return genderness_q, genderness_docs

def embedding_filename(embeddings):
    if embeddings == "w2v":
        embedding_filename = "./data/google_news_vectors_negative300.bin"
    elif embeddings == "fasttext":
        embedding_filename = "./data/fasttext.bin"
    elif embeddings == "fasttext_w2v_vocab":
        embedding_filename = "./data/fasttext_w2v_vocab.bin"
    return embedding_filename
