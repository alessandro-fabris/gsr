import utils
import os

if __name__ == "__main__":
    collection = "toy2"

    jobs1 = ["hygienist", "secretary", "hairdresser", "dietician", "paralegal", "receptionist", "phlebotomist", "maid", "nurse", "typist"]
    jobs2 = ["stonemason", "roofer", "electrician", "plumber", "carpenter", "firefighter", "millwright", "welder", "machinist", "driver"]

    adjs1 = ["honest", "affectionate", "compassionate", "patient", "unselfish", "polite", "outgoing", "romantic", "sensitive", "emotional"]
    adjs2 = ["ambitious", "confident", "hardworking", "independent", "decisive", "proud", "aggressive", "critical", "stubborn", "strong", "demanding", "possessive", "arrogant", "selfish"]

    all_jobs = jobs2 + jobs1
    all_adjs = adjs2 + adjs1
    #corpus
    for job in all_jobs:
        for adj in all_adjs:
            filename = utils.get_corpus_path(collection) + "/" + job + "_" + adj + ".txt"
            text = "The " + job + " is " + adj
            with open(filename, "w", encoding='utf8') as f:
            # file = open(filename, "w")
                f.write(text)
                f.close()

    #topics
    for job in all_jobs:
        filename = utils.get_topics_path(collection) + "/" + job + ".txt"
        text = job
        with open(filename, "w", encoding='utf8') as f:
            f.write(text)
            f.close()
    # qrels
    #stereo
    filename = utils.get_qrels_path(collection, type="stereo")
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w", encoding='utf8') as f:
        for job in all_jobs:
            for adj in all_adjs:
                if (adj in adjs2 and job in jobs2) or (adj in adjs1 and job in jobs1):
                    line = " ".join([job, "placeholder", job + "_" + adj, "1"])
                    f.write(line+"\n")

    # antistereo
    filename = utils.get_qrels_path(collection, type="antistereo")
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w", encoding='utf8') as f:
        for job in all_jobs:
            for adj in all_adjs:
                if (adj in adjs2 and job in jobs1) or (adj in adjs1 and job in jobs2):
                    line = " ".join([job, "placeholder", job + "_" + adj, "1"])
                    f.write(line + "\n")

    #neutral
    filename = utils.get_qrels_path(collection, type="neutral")
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w", encoding='utf8') as f:
        for job in all_jobs:
            for adj in all_adjs:
                line = " ".join([job, "placeholder", job + "_" + adj, "1"])
                f.write(line + "\n")