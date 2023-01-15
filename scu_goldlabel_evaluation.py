import json



def gold_evaluation_dataset(labels, output_file):
    outputDict = []

    for i, data in enumerate(labels):
        # Parse the JSON data
        # data = json.loads(data)
        # Iterate over the key-value pairs in the data
        for label, value in data.items():

            if "instance_id" in label:
                output_Temp = {'instance_id': value}
                print(value)
            else:
                label_scu = str(value).replace('\n', '')
                label_scu_array = label_scu.split('\t')

                result = list(map(int, map(lambda x: x.strip('"'), label_scu_array)))
                output_Temp[label] = sum(result) / len(result)

        outputDict.append(output_Temp)

    jsonString = json.dumps(outputDict)
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


# PyrXSum dataset
def gold_evaluate_pyrxsum():
    labels = open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-golden-labels.json')

    gold_evaluation_dataset(labels, 'eval_interface/src/data/pyrxsum/pyrxsum-gold_score.json')
    print("PyrXSum done!")


# REALSumm dataset !!! stu realsumm-70 has "." and smu realsumm-69 has "iii","****" and realsumm-97 has "most."
def gold_evaluate_realsumm():
    labels = open_json_file('eval_interface/src/data/realsumm/realsumm-golden-labels.json')

    gold_evaluation_dataset(labels, 'eval_interface/src/data/realsumm/realsumm-gold_score.json')
    print("REALSumm done!")


# Tac2008 dataset
def gold_evaluate_tac08():


    #nli_evaluation_dataset(smus, 'eval_interface/src/data/tac08/tac08-nli.json')
    print("Tac2008 done!")


# Tac2009 dataset !!! stu d0913-A has "?" devided by 0 error
def gold_evaluate_tac09():


    #nli_evaluation_dataset(smus, 'eval_interface/src/data/tac09/tac09-nli.json')
    print("Tac2009 done!")


def gold_evaluate_data(labels, result_path):
    gold_evaluation_dataset(labels, result_path)
    print(f"nli evaluation of {result_path} done!")

# nli_evaluate_pyrxsum()
gold_evaluate_realsumm()
# nli_evaluate_tac08()
# nli_evaluate_tac09()
