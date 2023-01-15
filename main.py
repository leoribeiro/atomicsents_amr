from atomic_amr import run_amr_data
from average_results import clac_average_for_datasets
import json
from evaluation import evaluate_data
from nli_evaluation import nli_evaluate_data
import sys


def open_json_file(filename):
    with open(filename) as f:
        data_json = json.load(f)
        return data_json


# Run the generation of SMUS
def realsumm_amr():
    run_amr_data(open_json_file('eval_interface/src/data/realsumm/realsumm-scus.json'),
                 'eval_interface/src/data/realsumm/realsumm-smus-test-with-st.json')


def pyrxsum_amr():
    run_amr_data(open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-scus.json'),
                 'eval_interface/src/data/pyrxsum/pyrxsum-smus.json')


def tac08_amr():
    run_amr_data(open_json_file('eval_interface/src/data/tac08/tac2008-scus.json'),
                 'eval_interface/src/data/tac08/tac2008-smus-test.json')


def tac09_amr():
    run_amr_data(open_json_file('eval_interface/src/data/tac09/tac2009-scus.json'),
                 'eval_interface/src/data/tac09/tac2009-smus.json')


# Run average results
"""
clac_average_for_datasets([[open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-acc.json'),
                           open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-nli.json')],
                           [open_json_file('eval_interface/src/data/realsumm/realsumm-acc-test.json'),
                            open_json_file('eval_interface/src/data/realsumm/realsumm-nli-scu.json')],
                           [open_json_file('eval_interface/src/data/tac08/tac08-acc.json'),
                            open_json_file('eval_interface/src/data/tac08/tac08-nli.json')],
                           [open_json_file('eval_interface/src/data/tac09/tac09-acc.json'),
                            open_json_file('eval_interface/src/data/tac09/tac09-nli.json')]])
"""


def calc_average():
    clac_average_for_datasets([[open_json_file('eval_interface/src/data/realsumm/realsumm-acc-test.json'),
                                open_json_file('eval_interface/src/data/realsumm/realsumm-nli-scu.json')]])


# evaluation of STUs and SMUs against SCUs
# pyrxsum
def eval_pyrxsum():
    evaluate_data(open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-smus.json'),
                  open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-stus.json'),
                  open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-scus.json'),
                  'eval_interface/src/data/pyrxsum/pyrxsum-acc.json',
                  True, True, False)


# realsum
def eval_realsumm():
    evaluate_data(open_json_file('eval_interface/src/data/realsumm/realsumm-smus-temp-test-all.json'),
                  open_json_file('eval_interface/src/data/realsumm/realsumm-stus.json'),
                  open_json_file('eval_interface/src/data/realsumm/realsumm-scus.json'),
                  'eval_interface/src/data/realsumm/realsumm-acc-test.json',
                  True, True, False)


# tac08
def eval_tac08():
    evaluate_data(open_json_file('eval_interface/src/data/tac08/tac2008-smus.json'),
                  open_json_file('eval_interface/src/data/tac08/tac2008-stus.json'),
                  open_json_file('eval_interface/src/data/tac08/tac2008-scus.json'),
                  'eval_interface/src/data/tac08/tac08-acc.json',
                  True, True, False)


# tac 08
def eval_tac09():
    evaluate_data(open_json_file('eval_interface/src/data/tac09/tac2009-smus.json'),
                  open_json_file('eval_interface/src/data/tac09/tac2009-stus.json'),
                  open_json_file('eval_interface/src/data/tac09/tac2009-scus.json'),
                  'eval_interface/src/data/tac09/tac09-acc.json',
                  True, True, False)


# nli evaluation
def extrinsic_eval_realsumm():
    summarys = open_json_file('eval_interface/src/data/realsumm/realsumm-system-summary.json')
    nli_evaluate_data(summarys,
                      open_json_file('eval_interface/src/data/pyrxsum/pyrxsum-smus.json'),
                      'eval_interface/src/data/pyrxsum/pyrxsum-nli.json')


def extrinsic_eval_pyrxsum():
    summarys = open_json_file('eval_interface/src/data/realsumm/realsumm-system-summary.json')
    nli_evaluate_data(summarys,
                      open_json_file('eval_interface/src/data/realsumm/realsumm-scus.json'),
                      'eval_interface/src/data/realsumm/realsumm-nli-scu.json')


def extrinsic_eval_tac08():
    summarys = open_json_file('eval_interface/src/data/realsumm/realsumm-system-summary.json')
    nli_evaluate_data(summarys,
                      open_json_file('eval_interface/src/data/tac08/tac2008-smus.json'),
                      'eval_interface/src/data/tac08/tac08-nli.json')


def extrinsic_eval_tac09():
    summarys = open_json_file('eval_interface/src/data/realsumm/realsumm-system-summary.json')
    nli_evaluate_data(summarys,
                      open_json_file('eval_interface/src/data/tac09/tac2009-smus.json'),
                      'eval_interface/src/data/tac09/tac09-nli.json')


try:
    function = sys.argv[1]
    globals()[function]()
except IndexError:
    raise Exception("Please provide function name")
except KeyError:
    raise Exception("Function {} hasn't been found".format(function))
