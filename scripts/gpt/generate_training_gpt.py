import jsonlines
import json
import random

data = []

def load_json(fn):
    with open(fn) as f:
        d = json.load(f)
        for s in d:
            sample = {}
            sample['prompt'] = s["summary"]
            response = ""
            for scu in s["scus"]:
                response = response + scu + " # "
            sample["completion"] = response
            data.append(sample)
            

def get_path(ds, fn = None):
    print('Load data', ds,'...')
    return "eval_interface/src/data/" + ds + "/" + (fn if fn != None else ds + "-scus") + ".json"


load_json(get_path("tac08", "tac2008-scus-sp"))
load_json(get_path("tac09", "tac2009-scus-sp"))

print("Shuffle data")
random.shuffle(data)

print("Write file...")
with open("data/gpt_training.jsonl", "w") as fp:
    writer = jsonlines.Writer(fp) 
    writer.write_all(data)
    writer.close()

print("Successfully wrote file.")