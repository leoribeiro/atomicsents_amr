import json


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def calc_average_sys_sum(gold):
    gold_list = {}
    for i, data in enumerate(gold):

        # Iterate over the key-value pairs in the data
        for label, value in data.items():
            print(label)
            if "instance_id" not in label:

                if i == 0:
                    gold_list[label] = value
                else:
                    gold_list[label] += value

    for label, value in gold_list.items():
        gold_list[label] = 1 / len(gold) * gold_list[label]

    return gold_list



def clac_average_for_gold_labels(resources):

    pyrxsum_gold = open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-gold_score.json')


    realsumm_gold = open_json_file('../eval_interface/src/data/realsumm/realsumm-gold_score.json')


    tac08_nli = open_json_file('../eval_interface/src/data/tac08/tac08-nli.json')

    tac09_nli = open_json_file('../eval_interface/src/data/tac09/tac09-nli.json')
    resources = [pyrxsum_gold, realsumm_gold]
    average = []
    for gold in resources:
        # average.append(calc_average(scores, nli))
        average.append(calc_average_sys_sum(gold))

    # calc_average(pyrxsum_score, pyrxsum_nli),
    #average = [calc_average(pyrxsum_score, pyrxsum_nli), calc_average_sys_sum(realsumm_score, realsumm_nli),
    #           calc_average(tac08_score, tac08_nli), calc_average(tac09_score, tac09_nli)]

    outputDict = []
    # "pyrxsum",
    datasets = ["pyrxsum", "realsumm", "tac08", "tac09"]
    print(average)
    for i in range(len(datasets)):
        if i <= 1:
            output_Temp = {'dataset': datasets[i]}
            print(datasets[i])
            for label, value in average[i].items():
                output_Temp[label] = value
            outputDict.append(output_Temp)



    jsonString = json.dumps(outputDict)
    jsonFile = open("../data/average-results-gold-labels.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

# clac_average_for_datasets()
clac_average_for_gold_labels([open_json_file('../eval_interface/src/data/realsumm/realsumm-gold_score.json')])