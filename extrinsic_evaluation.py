import json
from scipy import stats


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def calc_correlation_system(results, golden, is_pearson):
    results_array = []
    golden_array = []
    # Iterate over the key-value pairs in the data
    for label, value in results[0].items():
        if label != 'dataset':
            results_array.append(float(value))
            golden_array.append(float(golden[0][label]))
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


def corr_evaluation_dataset(pearson_system, spearman_system, pearson_summary, spearman_summary, output_file):
    outputDict = []

    output_Temp = {'instance_id': 'realsumm',
                   'pearson_system': pearson_system,
                   'spearman_system': spearman_system,
                   'pearson_summary': pearson_summary,
                   'spearman_summary': spearman_summary
                   }
    outputDict.append(output_Temp)

    jsonString = json.dumps(outputDict)
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def corr_evaluate_realsumm():
    pearson_system = calc_correlation_system(open_json_file('average-results-summarys.json'),
                                             open_json_file('average-results-gold-labels.json'), True)
    spearman_system = calc_correlation_system(open_json_file('average-results-summarys.json'),
                                              open_json_file('average-results-gold-labels.json'), False)
    pearson_summary = calc_correlation_summary(
        open_json_file('eval_interface/src/data/realsumm/realsumm-nli-test2.json'),
        open_json_file('eval_interface/src/data/realsumm/realsumm-gold_score.json'), True)
    spearman_summary = calc_correlation_summary(
        open_json_file('eval_interface/src/data/realsumm/realsumm-nli-test2.json'),
        open_json_file('eval_interface/src/data/realsumm/realsumm-gold_score.json'), False)

    corr_evaluation_dataset(pearson_system, spearman_system, pearson_summary, spearman_summary,
                            'eval_interface/src/data/realsumm/realsumm-extrinsic_evaluation.json')
    print("REALSumm done!")


corr_evaluate_realsumm()
