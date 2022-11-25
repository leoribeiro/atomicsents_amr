import json


def open_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines


def create_json(summary, name_of_sxus, sxus, name_of_output):
    outputDict = []
    for i, l in enumerate(summary):
        outputDict.append(
            {
                'instance_id': name_of_output[:-10] + "-" + str(i),
                'summary': l.replace('\n', ''),
                name_of_sxus: sxus[i].replace('\n', '').split("\t"),
            }
        )

    jsonString = json.dumps(outputDict)
    jsonFile = open(name_of_output, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

# Create Json out of source PyrXSum source data
summary = open_file('data/PyrXSum(Source)/references.txt')
stus = open_file('data/PyrXSum(Source)/STUs.txt')
scus = open_file('data/PyrXSum(Source)/SCUs.txt')
create_json(summary, 'stus', stus, 'data/pyrxsum/pyrxsum-stus.json')
create_json(summary, 'scus', scus, 'data/pyrxsum/pyrxsum-scus.json')

# Create Json out of source REALSumm data
summary = open_file('data/REALSumm(Source)/references.txt')
stus = open_file('data/REALSumm(Source)/STUs.txt')
scus = open_file('data/REALSumm(Source)/SCUs.txt')
create_json(summary, 'stus', stus, 'data/realsumm/realsumm-stus.json')
create_json(summary, 'scus', scus, 'data/realsumm/realsumm-scus.json')
