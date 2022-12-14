from summ_eval.rouge_metric import RougeMetric
import json


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def open_jsonl_file(filename):
    with open(filename) as f:
        data_json = [json.loads(jline) for jline in f.read().splitlines()]
        return data_json


def simple_evaluation(scus, sxus):
    rouge = RougeMetric()
    #print(sxus[0])
    if sxus[0] is None:
        return 0
    return rouge.evaluate_batch(scus, sxus)['rouge']['rouge_1_f_score']


def easiness_sent_evaluation(scus, sxus):
    rouge = RougeMetric()
    if sxus[0] is None:
        return 0
    # Easiness_sent
    # Get acc of every scu
    list_of_acc = []
    for scu in scus:
        r1_f1_score = []
        for sxu in sxus:
            r1_f1_score.append(rouge.evaluate_example(scu, sxu)['rouge']['rouge_1_f_score'])
        list_of_acc.append(max(r1_f1_score))
    # calculate average of acc list
    acc_sxu = (1 / len(list_of_acc)) * sum(list_of_acc)
    return acc_sxu


def evaluate_summaries(scus, stus, smus, output_file):
    # rouge = RougeMetric()

    summaries = ["This is one summary", "This is another summary"]
    references = ["This is one reference", "This is another"]
    # references = ["This is one summary", "This is another summary"]

    outputDict = []
    # rouge_dict = rouge.evaluate_example(summaries[0], references[0])
    # outputDict.append(rouge_dict)

    for i, scu in enumerate(scus):
        print(scu['instance_id'])
        # Evaluate
        # Simple evaluation by a collection of sentences
        stus_evaluation_total = simple_evaluation(scu['scus'], stus[i]['stus'])
        smus_evaluation_total = simple_evaluation(scu['scus'], smus[i]['smus'])

        # Easiness_sent
        stus_evaluation = easiness_sent_evaluation(scu['scus'], stus[i]['stus'])
        smus_evaluation = easiness_sent_evaluation(scu['scus'], smus[i]['smus'])

        # Save to json file
        outputDict.append({
            'instance_id': scu['instance_id'],
            'acc-stus': stus_evaluation,
            'acc-smus': smus_evaluation,
            'total_stus': stus_evaluation_total,
            'total_smus': smus_evaluation_total,
        })

    # print(rouge.supports_multi_ref) # True
    # multi_references = [["This is ref 1 for summ 1", "This is ref 2 for summ 1"], ["This is ref 1 for summ 2", "This is ref 2 for summ 2"]]
    # rouge_dict = rouge.evaluate_batch(summaries, multi_references)
    # outputDict.append(rouge_dict)

    jsonString = json.dumps(outputDict)
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


# PyrXSum dataset
def evaluate_pyrxsum():
    smus = open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-smus.json')
    stus = open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-stus.json')
    scus = open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-scus.json')

    evaluate_summaries(scus, stus, smus, 'eval_interface/src/data/pyrxsum/pyrxsum-acc.json')
    print("PyrXSum done!")


# REALSumm dataset !!! stu realsumm-70 has "." and smu realsumm-69 has "iii","****" and realsumm-97 has "most."
def evaluate_realsumm():
    smus = open_json_file('eval_interface/src/data/realsumm/realsumm-smus.json')
    stus = open_json_file('eval_interface/src/data/realsumm/realsumm-stus.json')
    scus = open_json_file('eval_interface/src/data/realsumm/realsumm-scus.json')

    evaluate_summaries(scus, stus, smus, 'eval_interface/src/data/realsumm/realsumm-acc.json')
    print("REALSumm done!")


# Tac2008 dataset
def evaluate_tac08():
    smus = open_json_file('eval_interface/src/data/tac08/tac2008-smus.json')
    stus = open_json_file('eval_interface/src/data/tac08/tac2008-stus.json')
    scus = open_json_file('eval_interface/src/data/tac08/tac2008-scus.json')

    evaluate_summaries(scus, stus, smus, 'eval_interface/src/data/tac08/tac08-acc.json')
    print("Tac2008 done!")


# Tac2009 dataset !!! stu d0913-A has "?" devided by 0 error
def evaluate_tac09():
    smus = open_json_file('eval_interface/src/data/tac09/tac2009-smus.json')
    stus = open_json_file('eval_interface/src/data/tac09/tac2009-stus.json')
    scus = open_json_file('eval_interface/src/data/tac09/tac2009-scus.json')

    evaluate_summaries(scus, stus, smus, 'eval_interface/src/data/tac09/tac09-acc.json')
    print("Tac2009 done!")


#evaluate_pyrxsum()
# evaluate_realsumm()
evaluate_tac08()
evaluate_tac09()
