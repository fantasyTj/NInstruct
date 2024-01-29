import re
import os
import glob
import json
from tqdm import tqdm
from pathlib import Path
from typing import List
from utils import get_class_from_module, save_results, pprint, ID_COUNTER, load_pickle, save_pickle
from inferencer import EXP_STR2CLASS_NAME
import configs
from configs import DATA_PATHS
from typing import Dict, Any

def aggregate(pool: Dict[str, Any], data: Dict[str, Any]):
    assert type(pool['title'])==list and type(pool['components_flat'])==dict and type(pool['components_nested'])==dict
    # title
    pool['title'].append(data['title'])
    # components_flat
    for k, v in data['components_flat'].items():
        if k not in pool['components_flat']:
            pool['components_flat'][k] = [] 
        pool['components_flat'][k].append(v)
    # components_nested
    for k, v in data['components_nested'].items():
        if k not in pool['components_nested']:
            pool['components_nested'][k] = []
        pool['components_nested'][k].extend(list(data['components_nested'][k].keys()))

def dedeplicate(pool: Dict[str, Any]):
    # title
    pool['title'] = list(set(pool['title']))
    # components_flat
    for k, v in pool['components_flat'].items():
        pool['components_flat'][k] = list(set(v))
    # components_nested
    for k, v in pool['components_nested'].items():
        pool['components_nested'][k] = list(set(v))

class GenerateInstances():
    def __init__(self,
                 exp_str: str,
                 infer_strs: List[str]) -> None:
        Path(os.path.join(configs.JSON_SAVE_PATH, exp_str)).mkdir(parents=True, exist_ok=True)
        self.exp_str = exp_str
        self.infer_strs = infer_strs
        inferencer_class = get_class_from_module('inferencer', EXP_STR2CLASS_NAME[exp_str])
        assert inferencer_class is not None, 'Inferencer class import failed.'
        self.inferencer = inferencer_class(types=infer_strs)

    def run(self) -> None:
        pool = {'title':[], 'components_flat':{}, 'components_nested':{}}
        files = glob.glob(os.path.join(DATA_PATHS[self.exp_str], "*.pkl"))
        for pkl_file in tqdm(files):
            cur = self.inferencer.load(pkl_file)
            if not len(cur):
                continue
            aggregate(pool, cur)
        dedeplicate(pool)
        save_path = os.path.join(configs.JSON_SAVE_PATH, self.exp_str, 'pool.pkl')
        save_pickle(save_path, pool)

def main():
    # args, _ = get_command_line_parser()
    exps = ["meishichina", "daydaycook", "douguo", "meishijie", "xiachufang", "xinshipu", "shipuxiu"]
    # pprint(vars(args))
    for exp in exps:
        generator = GenerateInstances(
            exp_str=exp,
            infer_strs=[]
            )
        generator.run()

if __name__ == '__main__':
    main()
