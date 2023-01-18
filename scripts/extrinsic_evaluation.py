import json
from scipy import stats


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def calc_correlation_system(results, golden, is_pearson):
    results_array = []
    golden_array = []
    print(results)
    print(golden)
    # Iterate over the key-value pairs in the data
    for label, value in results.items():
        if label not in ['dataset', 'stu-average', 'smu-average']:
            results_array.append(float(value))
            rep_label = label.replace("summary", "label")
            golden_array.append(float(golden[rep_label]))
    if is_pearson:
        res = stats.pearsonr(results_array, golden_array)[0]
    else:
        res = stats.spearmanr(results_array, golden_array)[0]

    return res


def calc_correlation_summary(results, golden, is_pearson):
    results_array = []
    golden_array = []
    # Iterate over the key-value pairs in the data
    res = []
    for i, data in enumerate(results):

        for label, value in data.items():
            if label != 'instance_id':
                results_array.append(float(value))
                rep_label = label.replace("summary", "label")
                golden_array.append(float(golden[i][rep_label]))
        if is_pearson:
            res.append(stats.pearsonr(results_array, golden_array)[0])
        else:
            res.append(stats.spearmanr(results_array, golden_array)[0])
    res = sum(res) / len(res)

    return res


def write_to_json(list_of_results, output_file):
    outputDict = []
    list_of_datasets = ['pyrxsum', 'realsumm']
    for i, result in enumerate(list_of_results):
        output_Temp = {'instance_id': list_of_datasets[i],
                       'pearson_system': result[0],
                       'spearman_system': result[1],
                       'pearson_summary': result[2],
                       'spearman_summary': result[3]
                       }
        outputDict.append(output_Temp)

    jsonString = json.dumps(outputDict)
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def corr_evaluate_realsumm():
    print("REALSumm start!")
    pearson_system = calc_correlation_system(open_json_file('../data/average-results-sg2.json')[1],
                                             open_json_file('../data/average-results-gold-labels.json')[1], True)
    spearman_system = calc_correlation_system(open_json_file('../data/average-results-sg2.json')[1],
                                              open_json_file('../data/average-results-gold-labels.json')[1], False)
    pearson_summary = calc_correlation_summary(
        open_json_file('../eval_interface/src/data/realsumm/realsumm-nli-sg2.json'),
        open_json_file('../eval_interface/src/data/realsumm/realsumm-gold_score.json'), True)
    spearman_summary = calc_correlation_summary(
        open_json_file('../eval_interface/src/data/realsumm/realsumm-nli-sg2.json'),
        open_json_file('../eval_interface/src/data/realsumm/realsumm-gold_score.json'), False)

    print("REALSumm done!")
    print([pearson_system, spearman_system, pearson_summary, spearman_summary])
    return [pearson_system, spearman_system, pearson_summary, spearman_summary]


def corr_evaluate_pyrxsum():
    print("PyrXSum start!")
    pearson_system = calc_correlation_system(open_json_file('../data/average-results-sg2.json')[0],
                                             open_json_file('../data/average-results-gold-labels.json')[0], True)
    spearman_system = calc_correlation_system(open_json_file('../data/average-results-sg2.json')[0],
                                              open_json_file('../data/average-results-gold-labels.json')[0], False)
    pearson_summary = calc_correlation_summary(
        open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-nli-sg2.json'),
        open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-gold_score.json'), True)
    spearman_summary = calc_correlation_summary(
        open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-nli-sg2.json'),
        open_json_file('../eval_interface/src/data/pyrxsum/pyrxsum-gold_score.json'), False)

    print("PyrXSum done!")
    print([pearson_system, spearman_system, pearson_summary, spearman_summary])
    return [pearson_system, spearman_system, pearson_summary, spearman_summary]


def corr_evaluation_datase():
    list_of_results = []
    list_of_results.append(corr_evaluate_pyrxsum())
    list_of_results.append(corr_evaluate_realsumm())

    write_to_json(list_of_results, '../data/extrinsic_evaluation-sg2.json')


corr_evaluation_datase()
