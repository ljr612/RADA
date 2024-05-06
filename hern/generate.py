import torch
import torch.nn as nn
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
from torch.utils.data import DataLoader

import json
import csv
import math, random, sys
import numpy as np
import argparse
import os

from bindgen import *
from tqdm import tqdm


def build_model(args):
    if args.att_refine:
        model = AttRefineDecoder(args)
    elif args.no_target:
        model = UncondRefineDecoder(args)
    elif args.sequence:
        model = SequenceDecoder(args)
    else:
        model = CondRefineDecoder(args)
    return model.cuda()


if __name__ == "__main__":
    os.chdir(sys.path[0])
    model_ckpt, _, model_args = torch.load(sys.argv[1])
    model = build_model(model_args)
    model.load_state_dict(model_ckpt)
    model.eval()

    data = AntibodyComplexDataset(
            sys.argv[2],
            cdr_type=model_args.cdr,
            L_target=model_args.L_target,
    )
    torch.manual_seed(model_args.seed)
    np.random.seed(model_args.seed)
    random.seed(model_args.seed)
    batch_size = 250
    num_decode = 1000
    topk = int(sys.argv[3])

    print('PDB', 'Native', 'Designed', 'Perplexity')
    with torch.no_grad():
        for ab in tqdm(data):
            new_cdrs, new_ppl = [], []
            for _ in range(num_decode // batch_size):
                _, epitope, surface = make_batch([ab] * batch_size)
                out = model.generate(epitope, surface)
                new_cdrs.extend(out.handle)
                new_ppl.extend(out.ppl.tolist())

            orig_cdr = ab['binder_seq']
            new_res = sorted(zip(new_cdrs, new_ppl), key=lambda x:x[1])
            # print(len(new_res))

            for cdr,ppl in new_res[:topk]: # new_res 中有1000个结果，脚本的第三个参数就是保存多少个结果
                print(ab['pdb'], orig_cdr, cdr, '%.3f' % ppl)