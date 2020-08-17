# correlation between genderedness of query and relevant docs

import utils
import we
from utils import dirness_q_and_docs_from_we
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # collection = "robust"
    # collection = "NY"
    # collection = "toy1"
    collection = "toy2"
    types = ["stereo", "neutral", "antistereo"]
    type2tit = {"stereo": "S",
                "neutral": "N",
                "antistereo": "CS"}

    WE = "w2v"
    discount = False

    filename_we = utils.embedding_filename(WE)
    E = we.WordEmbedding(filename_we)
    gender_dir = utils.compute_gender_dir(E)
    w2gend = {w: gender_dir.dot(E.v(w)) for w in E.words}
    slopes = []

    fig, axs = plt.subplots(1, len(types), sharey=True, sharex=True)
    if collection == "toy1":
        ylim = (-0.5, 0.5)
    elif collection == "toy2":
        ylim = (-0.05, 0.05)
    xlim = (-0.2, 0.4)
    for i, type in enumerate(types):
        q_id_to_rel_docs, q_id_to_scores = utils.q_id_to_rel_docs(collection, type=type)

        genderness_q, genderness_docs = dirness_q_and_docs_from_we(collection, q_id_to_rel_docs, E, gender_dir, q_id_to_scores=q_id_to_scores,
                                               w2gend=w2gend, disc=discount, verbose=False, exclude_query_terms=True)

        axs[i].scatter(genderness_q, genderness_docs, c="g")
        #some values might be nan, due to e.g. query terms not being encoded in WE
        corr, p, slope, intercept = utils.nan_corr(genderness_q, genderness_docs)
        slopes.append(slope)
        axs[i].set_xlim(xlim)
        axs[i].set_ylim(ylim)
        x1, x2 = xlim
        y1 = x1 * slope + intercept
        y2 = x2 * slope + intercept
        axs[i].plot([x1, x2], [y1, y2], 'k:')
        axs[i].set_title(type2tit[type])
        axs[i].set(adjustable='box')
        axs[i].set(aspect=(xlim[1]-xlim[0])/(ylim[1]-ylim[0]))
        axs[i].grid(linestyle='-', linewidth=0.2)
    axs[0].set(ylabel=r'$g_q(\mathcal{L})$')
    axs[1].set(xlabel=r'$g(q)$')
    plt.savefig("./plots/temp.pdf", bbox_inches='tight')