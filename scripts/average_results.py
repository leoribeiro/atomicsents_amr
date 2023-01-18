import json


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def calc_average(score, nli):
    score_average_stus = []
    score_average_smus = []
    nli_average = []
    for i in score:
        score_average_stus.append(i['easiness-stus-acc-bert'])
        score_average_smus.append(i['easiness-smus-acc-bert'])

    score_average_stus_value = 1 / len(score_average_stus) * sum(score_average_stus)
    score_average_smus_value = 1 / len(score_average_smus) * sum(score_average_smus)

    for i in nli:
        nli_average.append(i['score'])

    nli_average_value = 1 / len(nli_average) * sum(nli_average)

    return [score_average_stus_value, score_average_smus_value, nli_average_value]


def calc_average_sys_sum(score, nli):
    score_average_stus = []
    score_average_smus = []
    for i in score:
        score_average_stus.append(i['easiness-stus-acc-bert'])
        score_average_smus.append(i['easiness-smus-acc-bert'])

    score_average_stus_value = 1 / len(score_average_stus) * sum(score_average_stus)
    score_average_smus_value = 1 / len(score_average_smus) * sum(score_average_smus)
    nli_list = {}
    for i, data in enumerate(nli):

        # Iterate over the key-value pairs in the data
        for label, value in data.items():
            print(label)
            if "instance_id" not in label:

                if i == 0:
                    nli_list[label] = value
                else:
                    nli_list[label] += value


    for label, value in nli_list.items():
        nli_list[label] = 1 / len(nli) * nli_list[label]

    return [score_average_stus_value, score_average_smus_value, nli_list]


def clac_average_for_datasets(resources):
    pyrxsum_score = open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-acc-sg2.json')
    pyrxsum_nli = open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-nli-sg2.json')

    realsumm_score = open_json_file('../eval_interface/src/data/realsumm/realsumm-acc-sg2.json')
    realsumm_nli = open_json_file('../eval_interface/src/data/realsumm/realsumm-nli-sg2.json')

    tac08_score = open_json_file('../eval_interface/src/data/tac08/tac08-acc.json')
    tac08_nli = open_json_file('../eval_interface/src/data/tac08/tac08-nli.json')

    tac09_score = open_json_file('../eval_interface/src/data/tac09/tac09-acc.json')
    tac09_nli = open_json_file('../eval_interface/src/data/tac09/tac09-nli.json')
    average = []
    for scores, nli in resources:
        #average.append(calc_average(scores, nli))
        average.append(calc_average_sys_sum(scores, nli))

    # calc_average(pyrxsum_score, pyrxsum_nli),
    average = [calc_average_sys_sum(pyrxsum_score, pyrxsum_nli), calc_average_sys_sum(realsumm_score, realsumm_nli),
               calc_average(tac08_score, tac08_nli), calc_average(tac09_score, tac09_nli)]

    outputDict = []
    # "pyrxsum",
    datasets = ["pyrxsum", "realsumm", "tac08", "tac09"]
    print(average)
    for i in range(len(datasets)):
        if i <= 1:
            output_Temp = {'dataset': datasets[i]}
            output_Temp['stu-average'] = average[i][0]
            output_Temp['smu-average'] = average[i][1]
            print(average[i])
            for label, value in average[i][2].items():
                output_Temp[label] = value
            outputDict.append(output_Temp)
        else:

            outputDict.append({
                "dataset": datasets[i],
                "stu-average": average[i][0],
                "smu-average": average[i][1],
                "nli-average": average[i][2],
            })

    jsonString = json.dumps(outputDict)
    jsonFile = open("../data/average-results-sg2.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


clac_average_for_datasets([])
