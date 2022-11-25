from summ_eval.rouge_metric import RougeMetric
import json


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json

def evaluate_summaries(scus, sxus, sxus_name):
    rouge = RougeMetric()

    summaries = ["This is one summary", "This is another summary"]
    references = ["This is one reference", "This is another"]
    #references = ["This is one summary", "This is another summary"]




    outputDict = []
    #rouge_dict = rouge.evaluate_example(summaries[0], references[0])
    #outputDict.append(rouge_dict)

    for i, scu in enumerate(scus):

        rouge_dict = rouge.evaluate_batch(scu['scus'], sxus[i]['stus'])
        outputDict.append(rouge_dict['rouge']['rouge_1_f_score'])


    #print(rouge.supports_multi_ref) # True
    #multi_references = [["This is ref 1 for summ 1", "This is ref 2 for summ 1"], ["This is ref 1 for summ 2", "This is ref 2 for summ 2"]]
    #rouge_dict = rouge.evaluate_batch(summaries, multi_references)
    #outputDict.append(rouge_dict)




    jsonString = json.dumps(outputDict)
    jsonFile = open('results/evaluation_test.json', "w")
    jsonFile.write(jsonString)
    jsonFile.close()


smus = open_json_file('data/pyrxsum/pyrxsum-smus.json')
stus = open_json_file('data/pyrxsum/pyrxsum-stus.json')
scus = open_json_file('data/pyrxsum/pyrxsum-scus.json')
#print(smus[0]['smus'])
#print(scus[0]['scus'])
evaluate_summaries(scus, stus, 'smus')
