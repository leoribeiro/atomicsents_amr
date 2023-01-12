import json
import csv
from tqdm import tqdm
import amrlib as amrlib
import penman
from penman.models import amr
from itertools import chain, combinations
# import spacy
from nli_evaluation import sent_in_summary
import re

from amrlib.graph_processing.amr_fix import maybe_fix_unlinked_in_subgraph

# spacy = spacy.load("en_core_web_sm")

# Download and unzip models https://github.com/bjascob/amrlib-models
# DIR_STOG_MODEL = 'model_parse_xfm_bart_large-v0_1_0'
# DIR_GTOS_MODEL = 'model_generate_t5wtense-v0_1_0'
# stog = amrlib.load_stog_model(DIR_STOG_MODEL)
# gtos = amrlib.load_gtos_model(DIR_GTOS_MODEL)

amr_graph = "# ::snt  Anuradha Koirala and 425 young women and girls have been sleeping outdoors because of aftershocks . (c / cause-01 :ARG0 (a / aftershock) :ARG1 (s / sleep-01 :ARG0 (a2 / and :op1 (p / person :name (n / name :op1 \"Anuradha\" :op2 \"Koirala\")) :op2 (w / woman) :op3 (g / girl) :quant 42 :mod (y / young)) :location (o / outdoors))) "

g = penman.decode(amr_graph, model=amr.model)
t = penman.configure(g)

notes_in_tree = {}
for path, branch in t.walk():
    # val_node = path_var(path, t.node)
    role, target = branch
    if role == "/":
        continue
    if role in notes_in_tree:
        notes_in_tree[role] += 1
    else:
        notes_in_tree[role] = 1
print(f"Tree: {t}")
print(f"Number of nodes: {notes_in_tree}")
for i in range(10):
    print(t.node[i])
print(t.nodes())

{('/', 'cause-01'): {'val_description': 'c', 'triples': [(':ARG0', ('a', [('/', 'aftershock')])), (':ARG1', ('s', [
    ('/', 'sleep-01'), (':ARG0', ('a2', [('/', 'and'), (
    ':op1', ('p', [('/', 'person'), (':name', ('n', [('/', 'name'), (':op1', '"Anuradha"'), (':op2', '"Koirala"')]))])),
                                         (':op2', ('w', [('/', 'woman')])), (':op3', ('g', [('/', 'girl')])),
                                         (':quant', '425'), (':mod', ('y', [('/', 'young')]))])),
    (':location', ('o', [('/', 'outdoors')]))]))]},

 ('/', 'sleep-01'): {'val_description': 's', 'triples': [(':ARG0', (
'a2', [('/', 'and'), (
':op1', ('p', [('/', 'person'), (':name', ('n', [('/', 'name'), (':op1', '"Anuradha"'), (':op2', '"Koirala"')]))])),
       (':op2', ('w', [('/', 'woman')])), (':op3', ('g', [('/', 'girl')])), (':quant', '425'),
       (':mod', ('y', [('/', 'young')]))])), (':location', ('o', [('/', 'outdoors')]))]},
 ('/', 'and'): {'val_description': 'a2', 'triples': [(':op1', (
 'p', [('/', 'person'), (':name', ('n', [('/', 'name'), (':op1', '"Anuradha"'), (':op2', '"Koirala"')]))])),
                                                     (':op2', ('w', [('/', 'woman')])),
                                                     (':op3', ('g', [('/', 'girl')])), (':quant', '425'),
                                                     (':mod', ('y', [('/', 'young')]))]},
 ('/', 'person'): {'val_description': 'p',
                   'triples': [(':name', ('n', [('/', 'name'), (':op1', '"Anuradha"'), (':op2', '"Koirala"')]))]},
 ('/', 'name'): {'val_description': 'n', 'triples': [(':op1', '"Anuradha"'), (':op2', '"Koirala"')]}}
