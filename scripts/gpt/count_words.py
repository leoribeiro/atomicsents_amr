import json

with open("eval_interface/src/data/pyrxsum/pyrxsum-scus.json") as f:
    d = json.load(f)
    word_count = 0

    for s in d: 
        word_count = word_count + len(s["summary"].split())

        for sc in s["scus"]:
            word_count = word_count + len(s["summary"].split())

    print()
    print()
    print("--------------")
    print("pyrxsum")
    print("--------------")
    print()
    print("word count", word_count)
    # 750 about 1000 tokens cost 
    cost = round(word_count / 750 * 0.003, 2)
    cost_ = round(word_count / 750 * 0.03, 2)
    print("Estimated cost", cost, "-", cost_)

    icost = round(word_count / 750 * 0.012, 2)
    icost_ = round(word_count / 750 * 0.12, 2)
    print("Estimated cost (inf)", icost, "-", icost_)

    print("Estimated cost (tot)", icost+cost, "-", icost_+cost)


with open("eval_interface/src/data/realsumm/realsumm-scus.json") as f:
    d = json.load(f)
    word_count = 0

    for s in d: 
        word_count = word_count + len(s["summary"].split())

        for sc in s["scus"]:
            word_count = word_count + len(s["summary"].split())


    print()
    print()
    print("--------------")
    print("realsumm")
    print("--------------")
    print()
    print("word count", word_count)
    # 750 about 1000 tokens cost 
    cost = round(word_count / 750 * 0.003, 2)
    cost_ = round(word_count / 750 * 0.03, 2)
    print("Estimated cost", cost, "-", cost_)

    icost = round(word_count / 750 * 0.012, 2)
    icost_ = round(word_count / 750 * 0.12, 2)
    print("Estimated cost (inf)", icost, "-", icost_)

    print("Estimated cost (tot)", icost+cost, "-", icost_+cost)
