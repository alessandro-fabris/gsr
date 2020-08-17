import utils
import os

if __name__ == "__main__":
    collection = "toy1"
    jobs_f = ["hygienist", "secretary", "hairdresser", "dietician", "paralegal", "receptionist", "phlebotomist", "maid", "nurse", "typist"]
    jobs_m = ["stonemason", "roofer", "electrician", "plumber", "carpenter", "firefighter", "millwright", "welder", "machinist", "driver"]
    m_or_w = ["man", "woman"]

    all_jobs = jobs_m + jobs_f
    #corpus
    for job in all_jobs:
        for person in m_or_w:
            filename = utils.get_corpus_path(collection) + "/" + person + "_" + job + ".txt"
            text = "The " + person + " is a " + job
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
            person = m_or_w[0] if job in jobs_m else m_or_w[1]
            line = " ".join([job, "placeholder", person + "_" + job, "1"])
            # q_id, placeholder, doc_id, relevant = line.split()
            f.write(line+"\n")

    # antistereo
    filename = utils.get_qrels_path(collection, type="antistereo")
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w", encoding='utf8') as f:
        for job in all_jobs:
            person = m_or_w[1] if job in jobs_m else m_or_w[0]
            line = " ".join([job, "placeholder", person + "_" + job, "1"])
            # q_id, placeholder, doc_id, relevant = line.split()
            f.write(line+"\n")

    #neutral
    filename = utils.get_qrels_path(collection, type="neutral")
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w", encoding='utf8') as f:
        for job in all_jobs:
            for person in m_or_w:
                line = " ".join([job, "placeholder", person + "_" + job, "1"])
                # q_id, placeholder, doc_id, relevant = line.split()
                f.write(line + "\n")
