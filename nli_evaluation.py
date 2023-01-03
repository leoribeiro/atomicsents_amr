from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json

max_length = 256

premise = "Two women are embracing while holding to go packages."
hypothesis = "The men are fighting outside a deli."

hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
# hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
# hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
# hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
# hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"

tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)


def nli_evaluation(smus, output_file):
    outputDict = []

    for i, smu_list in enumerate(smus):
        counter = 0
        for smu in smu_list['smus']:
            tokenized_input_seq_pair = tokenizer.encode_plus(smu_list['summary'], smu,
                                                     max_length=max_length,
                                                     return_token_type_ids=True, truncation=True)

            input_ids = torch.Tensor(tokenized_input_seq_pair['input_ids']).long().unsqueeze(0)

            # remember bart doesn't have 'token_type_ids', remove the line below if you are using bart.
            token_type_ids = torch.Tensor(tokenized_input_seq_pair['token_type_ids']).long().unsqueeze(0)
            attention_mask = torch.Tensor(tokenized_input_seq_pair['attention_mask']).long().unsqueeze(0)

            outputs = model(input_ids,
                    attention_mask=attention_mask,
                    token_type_ids=token_type_ids,
                    labels=None)
            # Note:
            # "id2label": {
            #     "0": "entailment",
            #     "1": "neutral",
            #     "2": "contradiction"
            # },

            predicted_probability = torch.softmax(outputs[0], dim=1)[0].tolist()  # batch_size only one

            #print("Premise:", premise)
            #print("Hypothesis:", hypothesis)
            #print("Entailment:", predicted_probability[0])
            #print("Neutral:", predicted_probability[1])
            #print("Contradiction:", predicted_probability[2])

            if predicted_probability[0] > 0.5:
                counter += 1

        calculated_score = counter / len(smu_list['smus'])

        # Save to json file
        outputDict.append({
            'instance_id': smu_list['instance_id'],
            'score': calculated_score,
        })

    jsonString = json.dumps(outputDict)
    jsonFile = open(output_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


# PyrXSum dataset
def nli_evaluate_pyrxsum():
    smus = open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-smus.json')

    nli_evaluation(smus, 'eval_interface/src/data/pyrxsum/pyrxsum-nli.json')
    print("PyrXSum done!")


# REALSumm dataset !!! stu realsumm-70 has "." and smu realsumm-69 has "iii","****" and realsumm-97 has "most."
def nli_evaluate_realsumm():
    smus = open_json_file('eval_interface/src/data/realsumm/realsumm-smus.json')

    nli_evaluation(smus, 'eval_interface/src/data/realsumm/realsumm-nli.json')
    print("REALSumm done!")


# Tac2008 dataset
def nli_evaluate_tac08():
    smus = open_json_file('eval_interface/src/data/tac08/tac2008-smus.json')

    nli_evaluation(smus, 'eval_interface/src/data/tac08/tac08-nli.json')
    print("Tac2008 done!")


# Tac2009 dataset !!! stu d0913-A has "?" devided by 0 error
def nli_evaluate_tac09():
    smus = open_json_file('eval_interface/src/data/tac09/tac2009-smus.json')

    nli_evaluation(smus, 'eval_interface/src/data/tac09/tac09-nli.json')
    print("Tac2009 done!")


nli_evaluate_pyrxsum()
nli_evaluate_realsumm()
#nli_evaluate_tac08()
#nli_evaluate_tac09()