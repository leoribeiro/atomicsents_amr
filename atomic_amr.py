import json
import csv
from tqdm import tqdm
import amrlib as amrlib
import penman
from penman.models import amr
from itertools import chain, combinations
import spacy

spacy = spacy.load("en_core_web_sm")

# Download and unzip models https://github.com/bjascob/amrlib-models
DIR_STOG_MODEL = 'model_parse_xfm_bart_large-v0_1_0'
DIR_GTOS_MODEL = 'model_generate_t5wtense-v0_1_0'
stog = amrlib.load_stog_model(DIR_STOG_MODEL)
gtos = amrlib.load_gtos_model(DIR_GTOS_MODEL)


def split_amr_meta(entry):
    meta_lines = []
    graph_lines = []
    for line in entry.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('# ::'):
            meta_lines.append(line)
        elif line.startswith('#'):
            continue
        else:
            graph_lines.append(line)
    return meta_lines, graph_lines


def gstring_to_oneline(gstring):
    meta_lines, graph_lines = split_amr_meta(gstring)
    gstring = ' '.join(graph_lines)
    gstring = re.sub(' +', ' ', gstring)
    return gstring


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    # s = list(iterable)
    s = iterable
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def read_csv(file):
    # Read CSV file
    with open(file) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]

        return data_read


def save_data(data, output_file):
    with open(output_file, "w", encoding="utf-8") as fd:
        for example in data:
            example = dict(example)
            fd.write(json.dumps(example, ensure_ascii=False) + "\n")


def load_source_docs(file_path, to_dict=False):
    with open(file_path, encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    if to_dict:
        data = {example["id"]: example for example in data}
    return data


import re


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


def path_var(path, node):
    var, branches = node
    for step in path[:-1]:
        var, branches = branches[step][1]
    return var


def get_subgraphs2(amr_graph):
    g = penman.decode(amr_graph, model=amr.model)
    t = penman.configure(g)

    dict_variables = {}
    # import pdb
    # pdb.set_trace()
    root_node = t.node[0]
    subgraphs = []
    paths_variables = {}
    for path, branch in t.walk():
        val_node = path_var(path, t.node)
        if val_node not in dict_variables:
            dict_variables[val_node] = branch
            continue

        # if val_node != root_node:
        #     continue
        # import pdb
        # pdb.set_trace()
        role, target = branch
        # print(path, val_node, branch)
        # if isinstance(target, tuple):
        # print(path, val_node, branch)
        # print(penman.format(target))
        if dict_variables[val_node] not in paths_variables:
            paths_variables[dict_variables[val_node]] = {}
            paths_variables[dict_variables[val_node]]['val_description'] = val_node
            paths_variables[dict_variables[val_node]]['triples'] = []
        paths_variables[dict_variables[val_node]]['triples'].append((role, target))
        # linearized_graph = penman.format((val_node, [dict_variables[val_node], (role, target), (role, target)]))

    for variables in paths_variables.keys():
        val_node = paths_variables[variables]['val_description']

        args_triples = []
        other_triples = []

        for arg in paths_variables[variables]['triples']:
            if 'ARG' in arg[0]:
                args_triples.append(arg)
            else:
                other_triples.append(arg)

        # lists_args = list(powerset(paths_variables[variables]['triples']))

        lists_args = []
        lists_args.append(args_triples)
        for arg in other_triples:
            lists_args.append(args_triples + [arg])
        # import pdb
        # pdb.set_trace()
        for list_args in lists_args:
            # list_args = list(list_args)

            filtered_list_args = []
            for arg in list_args:
                if 'purpose' in arg[0]:
                    continue
                filtered_list_args.append(arg)

            list_args = filtered_list_args

            count_args = 0
            check_arg2 = False
            for arg in list_args:
                if 'ARG' in arg[0]:
                    count_args += 1
                if 'ARG2' in arg[0]:
                    check_arg2 = True

            if list_args:
                if count_args > 1 or (check_arg2 and len(list_args) > 1):
                    # for l in lists_args:
                    #     if isinstance(l, tuple):
                    #         tuple_instance = l
                    #     else:
                    #         tuple_instance = l[0]
                    #
                    #     if tuple_instance[1] in dict_variables.keys():
                    #         tuple_instance[1] = (tuple_instance[1], )
                    linearized_graph = penman.format((val_node, [dict_variables[val_node], *list_args]))
                    subgraphs.append(linearized_graph)

    return subgraphs


def get_subgraphs(amr_graph):
    g = penman.decode(amr_graph, model=amr.model)
    # filtered_instances = []
    # for v in g.instances():
    #     if has_numbers(v.target):
    #         print(v)
    #         filtered_instances.append(v)
    t = penman.configure(g)

    dict_variables = {}
    root_node = t.node[0]
    subgraphs = []
    for path, branch in t.walk():
        val_node = path_var(path, t.node)
        if val_node not in dict_variables:
            dict_variables[val_node] = branch

        if val_node != root_node:
            continue

        # import pdb
        # pdb.set_trace()
        role, target = branch
        if isinstance(target, tuple):
            # print(path, val_node, branch)
            # print(penman.format(target))
            linearized_graph = penman.format((val_node, [dict_variables[val_node], (role, target)]))
            subgraphs.append(linearized_graph)
    return subgraphs


def get_concepts(g_tag):
    tokens = g_tag.split()
    dict_concepts = {}
    for t in tokens:
        if "~" in t:
            t = t.replace("(", "")
            t = t.replace(")", "")
            parts_t = t.split("~")
            dict_concepts[parts_t[0]] = t
    return dict_concepts


def replace_graph_with_tags(dict_tag, graph):
    for key, value in dict_tag.items():
        graph = graph.replace(key, value)
    return graph


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


def open_jsonl_file(filename):
    with open(filename) as f:
        data_json = [json.loads(jline) for jline in f.read().splitlines()]
        return data_json


def run_amr(filename, data_json):
    outputDict = []
    for example in data_json:  # [:2]:
        # print("Id:", example['instance_id'])
        # print("Summary:", example['summary'])
        page_doc = spacy(example['summary'], disable=["tagger"])
        sentences = [sent.text for sent in page_doc.sents]

        graphs, graphs_tags = stog.parse_sents(sentences, add_metadata=True)

        # print("  ")
        # print("  ")
        list_of_sents = []
        list_of_trees = []
        for idx, (s, g, g_tag) in enumerate(zip(sentences, graphs, graphs_tags)):
            # print("Sentence #", idx)
            # print(s)
            # print(g)
            # print(g_tag)
            # print("  ")
            # print("AMR subgraphs:")
            # print("  ")
            dict_tag = get_concepts(g_tag)
            subgraphs = get_subgraphs2(g)
            subgraphs_tag = []
            for sb in subgraphs:
                list_of_trees.append(sb)
                sb = gstring_to_oneline(sb)
                sb = replace_graph_with_tags(dict_tag, sb)
                subgraphs_tag.append(sb)
                # print("-")

            sents, _ = gtos.generate_taged(subgraphs_tag, disable_progress=True)
            for sent in sents:
                if sent.__contains__(" ") and not sent.__contains__("* * "):
                    list_of_sents.append(sent)
        # Think about something that makes more sense ( NONE etc.)
        if len(list_of_sents) == 0:
            list_of_sents.append(None)
        outputDict.append(
            {'instance_id': example['instance_id'],
             'summary': example['summary'],
             'tree': list_of_trees,
             'smus': list_of_sents, }
        )
        # for s1, g1 in zip(sents, subgraphs):
        # print(g1)
        # print(s1)
        # print(" ")
        # print(" ")
        # print("--")

        # print("----")
        # print(" ")
        # print(" ")

    jsonString = json.dumps(outputDict)
    jsonFile = open(filename, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


# Create smus out of Tac2008 data
def run_tac08():
    data_json = open_json_file('eval_interface/src/data/tac08/tac2008-scus.json')
    run_amr('eval_interface/src/data/tac08/tac2008-smus.json', data_json)


# Create smus out of Tac2009 data
def run_tac09():
    data_json = open_json_file('eval_interface/src/data/tac09/tac2009-scus.json')
    run_amr('eval_interface/src/data/tac09/tac2009-smus.json', data_json)


# Create smus out of PyrXSum data
def run_pyyrxsum():
    data_json = open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-scus.json')
    run_amr('eval_interface/src/data/pyrxsum/pyrxsum-smus.json', data_json)


# Create smus out of REALSumm data
def run_realsumm():
    data_json = open_json_file('eval_interface/src/data/realsumm/realsumm-scus.json')
    run_amr('eval_interface/src/data/realsumm/realsumm-smus.json', data_json)


#run_realsumm()
#run_pyyrxsum()
run_tac08()
run_tac09()
