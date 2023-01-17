import json
import requests
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-2.7b"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

with open("results/data.json") as f:
    d = json.load(f)

    q = "---\n"

    # Get some examples in the form of
    # ---
    # <SUMMARY>
    # <scu> # <scu> # ... # <scu> #
    # ---
    for s in d[0:2]:
        q = q + s["Summary"] + "\n"
        for scu in s["scus"]:
            q = q + scu + " # "
        q = q + "---\n"

    # Load the samples to query
    with open("data/realsumm/realsumm-smus-test.json") as fd:
        qd = json.load(fd)

        for sample in qd[0:1]:
            queried = query({ "inputs": q + sample["summary"], "options": { "wait_for_model":True}})
            print(q)
            print(queried)
