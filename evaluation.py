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

def evaluate_summaries(scus, stus, smus, output_file):
    rouge = RougeMetric()

    summaries = ["This is one summary", "This is another summary"]
    references = ["This is one reference", "This is another"]
    #references = ["This is one summary", "This is another summary"]

    outputDict = []
    #rouge_dict = rouge.evaluate_example(summaries[0], references[0])
    #outputDict.append(rouge_dict)

    for i, scu in enumerate(scus):

        #print(scu['instance_id'])
        # Evaluate
        rouge_dict_stus = rouge.evaluate_batch(scu['scus'], stus[i]['stus'])
        rouge_dict_smus = rouge.evaluate_batch(scu['scus'], smus[i]['smus'])

        #Save to json file
        outputDict.append({
                'instance_id': scu['instance_id'],
                'acc-stus': rouge_dict_stus['rouge']['rouge_1_f_score'],
                'acc-smus': rouge_dict_smus['rouge']['rouge_1_f_score'],
            })

    #print(rouge.supports_multi_ref) # True
    #multi_references = [["This is ref 1 for summ 1", "This is ref 2 for summ 1"], ["This is ref 1 for summ 2", "This is ref 2 for summ 2"]]
    #rouge_dict = rouge.evaluate_batch(summaries, multi_references)
    #outputDict.append(rouge_dict)

    jsonString = json.dumps(outputDict)
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

# PyrXSum dataset
smus = open_json_file('data/pyrxsum/pyrxsum-smus.json')
stus = open_json_file('data/pyrxsum/pyrxsum-stus.json')
scus = open_json_file('data/pyrxsum/pyrxsum-scus.json')

evaluate_summaries(scus, stus, smus, 'data/pyrxsum/pyrxsum-acc.json')
print("PyrXSum done!")

# REALSumm dataset !!! stu realsumm-70 has "."
smus = open_json_file('data/realsumm/realsumm-smus.json')
stus = open_json_file('data/realsumm/realsumm-stus.json')
scus = open_json_file('data/realsumm/realsumm-scus.json')

evaluate_summaries(scus, stus, smus, 'data/realsumm/realsumm-acc.json')
print("REALSumm done!")

# Tac2008 dataset
smus = open_json_file('data/tac08/tac2008-smus.json')
stus = open_json_file('data/tac08/tac2008-stus.json')
scus = open_json_file('data/tac08/tac2008-scus.json')

evaluate_summaries(scus, stus, smus, 'data/tac08/tac08-acc.json')
print("Tac2008 done!")

# PyrXSum dataset !!! stu d0913-A has "?" devided by 0 error
smus = open_json_file('data/tac09/tac2009-smus.json')
stus = open_json_file('data/tac09/tac2009-stus.json')
scus = open_json_file('data/tac09/tac2009-scus.json')

evaluate_summaries(scus, stus, smus, 'data/tac09/tac09-acc.json')
print("Tac2009 done!")
