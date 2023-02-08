import openai
import json
import pandas as pd

ft_model = 'davinci:ft-personal-2023-02-08-09-42-43' # ft-yWG8yb5cL8E1du9igUeaFk4O

def get_path(ds, fn = None):
    print('Load data', ds,'...')
    return "../../eval_interface/src/data/" + ds + "/" + (fn if fn != None else ds + "-scus") + ".json"

def get_save_path(ds, fn = None):
    print('Save data', ds,'...')
    return "../../eval_interface/src/data/" + ds + "/" + (fn if fn != None else ds + "-sgus-davinci") + ".json"


def generate(ds):
    fn = get_path(ds)
    with open(fn) as f:
        dataset = []
        d = json.load(f)
        for idx, s in enumerate(d):
            print(idx, "/", len(d), "samples")
            sample = { "summary": s["summary"], "instance_id": s["instance_id"] }
            prompt = s["summary"].replace('<t> ','').replace(' </t>','').replace(" . ", ". ")
            res = openai.Completion.create(model=ft_model, prompt=prompt + ' ->', max_tokens=1000, stop=" END\n")
            sample['sgus'] = res['choices'][0]['text'].replace(" END\n", "").lstrip().replace(" . ", ". ").split(" # ")
            dataset.append(sample)
        json.dump(dataset, open(get_save_path(ds), "w"))

generate("pyrxsum")
generate("realsumm")