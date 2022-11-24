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


summary = open_file('data/PyrXSum/references.txt')
stus = open_file('data/PyrXSum/STUs.txt')
scus = open_file('data/PyrXSum/SCUs.txt')
create_json(summary, 'stus', stus, 'data/pyrxsum-stus.json')
create_json(summary, 'scus', scus, 'data/pyrxsum-scus.json')

summary = open_file('data/REALSumm/references.txt')
stus = open_file('data/REALSumm/STUs.txt')
scus = open_file('data/REALSumm/SCUs.txt')
create_json(summary, 'stus', stus, 'data/realsumm-stus.json')
create_json(summary, 'scus', scus, 'data/realsumm-scus.json')
