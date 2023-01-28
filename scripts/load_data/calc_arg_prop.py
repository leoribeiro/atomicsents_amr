import json

import numpy as np


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def create_json(pred_args, name_of_output):
    # Calc probability
    outputDict = {}
    for key in pred_args:
        sum_of_values = sum(pred_args[key].values())
        output_Temp = {}
        for k in pred_args[key]:
            # Add to dict for json
            output_Temp[k] = pred_args[key][k]/sum_of_values

        outputDict[key] = dict(sorted(output_Temp.items(), key=lambda item: item[1], reverse=True))
    # get 80 % of the most used features
    outDict = {}
    for key in outputDict:
        commutative_sum = 0
        output_Temp = []
        for k in outputDict[key]:
            if commutative_sum <= 0.8:
                output_Temp.append(k)
            commutative_sum += outputDict[key][k]
        outDict[key] = output_Temp



    jsonString = json.dumps(outDict)
    jsonFile = open(name_of_output, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


create_json(open_json_file('../../data/pred_args.json'), '../../data/pred_args_prob.json')
