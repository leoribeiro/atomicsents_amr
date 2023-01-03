#!/usr/bin/python3
import setup_run_dir    # this import tricks script to run from 2 levels up
import os
from   amrlib.utils.logging import setup_logging, WARN
from   amrlib.models.parse_gsii.inference import Inference


if __name__ == '__main__':
    setup_logging(logfname='logs/generate.log', level=WARN)
    device     = 'cuda:0'
    if not torch.backends.mps.is_available():
        if not torch.backends.mps.is_built():
            print("MPS not available because the current PyTorch install was not "
                  "built with MPS enabled.")
        else:
            print("MPS not available because the current MacOS version is not 12.3+ "
                  "and/or you do not have an MPS-enabled device on this machine.")

    else:
        device = torch.device("mps")
    model_dir  = 'amrlib/data/model_parse_gsii'
    model_fn   = 'epoch200.pt'
    data_dir   = 'amrlib/data/tdata_gsii'
    test_data  = 'test.txt.features.nowiki'
    out_fn     = model_fn + '.test_generated'

    infer = Inference(model_dir, model_fn, device=device)
    infer.reparse_annotated_file(data_dir, test_data, model_dir, out_fn)
