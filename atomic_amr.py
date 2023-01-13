import json
import csv
from tqdm import tqdm
import amrlib as amrlib
import penman
from penman.models import amr
from itertools import chain, combinations
import spacy
from nli_evaluation import sent_in_summary
import re
from penman.graph import Graph

from amrlib.graph_processing.amr_fix import maybe_fix_unlinked_in_subgraph

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


def get_subgraphs3(amr_graph):
    g = penman.decode(amr_graph, model=amr.model)
    t = penman.configure(g)
    '''
    notes_in_tree = {}
    test = []
    current_list = test
    for path, branch in t.walk():
        val_node = path_var(path, t.node)
        role, target = branch
        if role == "/":
            continue
        if role in notes_in_tree:
            notes_in_tree[role][0] += 1
            notes_in_tree[role][1].append(val_node)
        else:
            notes_in_tree[role] = [1, [val_node]]
            # current_list.append((val_node, [branch]))
            # current_list = current_list[0][1]
    print(notes_in_tree)
    '''
    # print(g)
    # print(g.top)
    list_of_t = []
    # list_of_trees.append(penman.format(t))
    temp_graph = []
    temp = ""
    end = True
    base_node_tuple = g.triples[0]
    base_node = g.triples[0][0]
    sub_grahs = []
    iteration = 1
    counter = 0
    start = True
    stop = False
    base_node_counter = -1  # Amount of direct leaves
    for i, subtree in enumerate(g.triples):
        if i == 0:
            continue
        if subtree[0] == base_node:
            list_of_t.append([base_node_tuple, subtree])
        else:
            list_of_t[-1].append(subtree)

    # Todo 1: spliten nach op, wenn vorher and
    # check and presence
    temp_graph_and = [[]]
    i = 0
    end_of_outer_loop = True
    while end_of_outer_loop:
        node = g.triples[i]
        for n in temp_graph_and:
            n.append(node)
        if node[2] == "and":
            end_of_inner_loop = True
            if i == 0:
                node_id_of_arg = ('XXX','XXX', 'XXX')
            else:
                node_id_of_arg = g.triples[i - 1]
            node_id_of_and = g.triples[i]
            subtree_graphs = []
            i += 1
            number_of_subtrees = len(temp_graph_and)
            while end_of_inner_loop:
                node = g.triples[i]
                if node[0] == node_id_of_and[0] and ":op" in node[1]:
                    for n in temp_graph_and:
                        tempp = n.copy()
                        tempp.append(node)
                        subtree_graphs.append(tempp)

                elif node[0] == node_id_of_arg[0] or i >= len(g.triples) - 1:
                    if i >= len(g.triples) - 1:
                        end_of_outer_loop = False
                    temp_graph_and = subtree_graphs
                    i -= 2
                    end_of_inner_loop = False


                else:
                    for j in range(number_of_subtrees):
                        subtree_graphs[-(j + 1)].append(node)
                i += 1

        if i >= len(g.triples) - 1:
            end_of_outer_loop = False
        else:
            i += 1
    if len(temp_graph_and) != 1:
        list_of_t.extend(temp_graph_and)
    # Todo 2: löschen von einzelnen Eigenschaften
    '''
    while end:
        for i, node in enumerate(g.triples):
            if i == 0:
                temp_graph.append(node)
                continue
            if node[0] == base_node and stop:
                break
            if node[0] == base_node:
                counter += 1
            if node[0] == base_node and counter == iteration:
                stop = True
            if i == len(g.triples) - 1:
                end = False

            temp_graph.append(node)
        stop = False
        counter = 0
        iteration += 1

        list_of_trees.append(penman.format(penman.configure(Graph(temp_graph))))
        temp_graph = []
    '''

    # print(t.nodes().index())
    # test_graph = Graph(test_graph)
    # test_tree = penman.configure(test_graph)
    # print(test_graph)
    # print(test_tree)
    # print(t.nodes().count('op1'))
    # test2 = t
    # list_of_trees.append(penman.configure(Graph([('c', ':instance', 'cause-01'), ('c', ':ARG0', 'a'), ('a', ':instance', 'aftershock'), ('c', ':ARG1', 's'), ('s', ':instance', 'sleep-01'), ('s', ':ARG0', 'a2'), ('a2', ':instance', 'and'), ('a2', ':op2', 'w'), ('w', ':instance', 'woman'), ('a2', ':op3', 'g'), ('g', ':instance', 'girl'), ('a2', ':quant', '425'), ('a2', ':mod', 'y'), ('y', ':instance', 'young'), ('s', ':location', 'o'), ('o', ':instance', 'outdoors')])))

    list_of_t = list(map(lambda x: penman.format(penman.configure(Graph(x))), list_of_t))

    return list_of_t


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
    duplicate_counter = 0

    for index_i, example in enumerate(data_json):
        if index_i not in [7]:# and False:  # [5, 61, 86, 38]:# and False:
            print(f"Skip example: {example['instance_id']}")
        else:
            # print("Id:", example['instance_id'])
            # print("Summary:", example['summary'])
            se = example['summary']

            if "\u00a0" in se:
                se = se.replace("\u00a0", '')
            se = re.sub(r'\s+', ' ', se)
            if "<t>" in se:
                # initializing tag
                tag = "t"
                # regex to extract required strings
                reg_str = "<" + tag + ">(.*?)</" + tag + ">"
                sentences = re.findall(reg_str, se)
            else:
                page_doc = spacy(se, disable=["tagger"])
                sentences = [se.text for se in page_doc.sents]
            # sentences.encode("utf-8").decode("utf-8", "replace")

            # sentences = list(map(lambda string: "".join(
            #    map(lambda x: "_" if string.find("'") <= x[0] < string.find("'", string.find("'") + 1) and x[1] == " " else x[1], enumerate(string))) if "'" in string else string, sentences))
            # print(sentences)

            graphs, graphs_tags = stog.parse_sents(sentences, add_metadata=True)

            # print("  ")
            # print("  ")
            print(example['instance_id'])
            list_of_sents = []
            list_of_trees = []
            summary_trees = []
            for idx, (s, g, g_tag) in enumerate(zip(sentences, graphs, graphs_tags)):
                summary_trees.append(g)

                # print("  ")
                # print("AMR subgraphs:")
                # print("  ")
                dict_tag = get_concepts(g_tag)
                subgraphs = get_subgraphs3(g)
                # TODO: Fallback okay ? --> Original sentence for default if too short?
                if 0 == len(subgraphs):
                    subgraphs = get_subgraphs(g)

                subgraphs_tag = []
                for sb in subgraphs:
                    sb = maybe_fix_unlinked_in_subgraph(g, sb)
                    list_of_trees.append(sb)
                    sb = gstring_to_oneline(sb)
                    sb = replace_graph_with_tags(dict_tag, sb)
                    subgraphs_tag.append(sb)
                    # print("-")

                sents, _ = gtos.generate_taged(subgraphs_tag, disable_progress=True)
                if False:
                    print("Sentence #", idx)
                    print(s)
                    print(graphs)
                    print(graphs_tags)
                    print(subgraphs)
                    print(g_tag)
                    print(sents)
                for sent in sents:
                    if sent in list_of_sents:  # sent.__contains__(" ") and not sent.__contains__("* * "):
                        duplicate_counter += 1
                    list_of_sents.append(sent)
            list_of_correct_sent = sent_in_summary(se, list_of_sents)
            # print(list_of_correct_sent)
            list_of_sents = [value1 for value1, value2 in zip(list_of_sents, list_of_correct_sent) if value2]
            list_of_trees = [value1 for value1, value2 in zip(list_of_trees, list_of_correct_sent) if value2]
            # Think about something that makes more sense ( NONE etc.)
            if len(list_of_sents) == 0:
                list_of_sents.append(None)
            outputDict.append(
                {'instance_id': example['instance_id'],
                 'summary': se,  # example['summary'],
                 'summary_trees': summary_trees,
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
    print(f"Number of duplicates: {duplicate_counter}")


'''
# Create smus out of Tac2008 data
def run_tac08_amr(scu_path, result_path):
    data_json = open_json_file(scu_path)
    run_amr(result_path, data_json)


# Create smus out of Tac2009 data
def run_tac09_amr(scu_path, result_path):
    data_json = open_json_file(scu_path)
    run_amr(result_path, data_json)


# Create smus out of PyrXSum data
def run_pyyrxsum_amr(scu_path, result_path):
    data_json = open_json_file(scu_path)
    run_amr(result_path, data_json)


# Create smus out of REALSumm data
def run_realsumm_amr(scu_path, result_path):
    data_json = open_json_file(scu_path)
    run_amr(result_path, data_json)
'''


def run_amr_data(scus, result_path):
    run_amr(result_path, scus)


run_amr_data(open_json_file('eval_interface/src/data/realsumm/realsumm-scus.json'),
             'eval_interface/src/data/realsumm/realsumm-smus-temp-test-all.json')
