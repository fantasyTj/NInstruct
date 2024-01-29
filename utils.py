import os
import re
import pickle
import json
import importlib
import ast
import time
import argparse
from argparse import ArgumentParser
from typing import List, Any, Dict, Union
import openai

import configs
from configs import OPEN_AI_KEY, IMG_DOWNLOAD_FAILED_LOGS, IMG_DOWNLOAD_TODO
import random, string

import hashlib

def generate_hash(url):
    sha256 = hashlib.sha256()
    sha256.update(url.encode('utf-8'))

    hash_code = sha256.hexdigest()

    return hash_code

class Counter:
    def __init__(self, prev_str: str = ''):
        self.count = 0
        self.prev_str = prev_str

    def set_str(self, prev_str: str):
        self.prev_str = prev_str

    def increment(self):
        self.count += 1

    def config(self, count: int):
        self.count = count

    def str2int(self, cur_str):
        return int(cur_str.replace(f'{self.prev_str}_', ''))

    def __str__(self):
        return f'{self.prev_str}_{self.count:010d}'


class GPT:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPEN_AI_KEY)

    def answer(self, question):
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])

        return completion.choices[0].message.content


ID_COUNTER = Counter()
IMG_FILES = {}

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/running.log',
                    filemode='w')

LOGGER = logging.getLogger('ginstruct')

from functools import reduce

def merge_dicts(dicts):
    return reduce(lambda a, b: {**a, **b}, dicts)

def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def save_pickle(file_name, data):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.DEFAULT_PROTOCOL)

def preprocess_text(text: str = ''):
    assert isinstance(text, str)
    # text = re.sub(r'^\d+\s*', '', text) # 去除开头的数字
    text = text.strip()
    text = re.sub(r'^[.,;?”’:。，]+', '', text)  # 去除开头的标点符号
    text = re.sub(r'\[(\w+)R\]', r'[\1]', text) # [赞R] 替换为 [赞]
    text = re.sub(r'@\S+\s*', '', text) # 删除 @ 之后的信息
    text = text.strip()
    return text

def preprocess_strip_begin_numbers(text: str = ''):
    assert isinstance(text, str)
    text = re.sub(r'^\d+\s*', '', text) # 去除开头的数字
    return text

def remove_non_chinese_digits(text):
    # 使用正则表达式匹配非数字和非中文字符并替换为空格
    cleaned_text = re.sub(r'[^\u4e00-\u9fff0-9]', '', text)
    return cleaned_text

def log_img(url: str):
    if url is None:
        return 'null.jpg'

    global IMG_FILES
    if url not in IMG_FILES.keys():
        dest_file = generate_hash(url) + '.jpg'
        with open(IMG_DOWNLOAD_TODO, 'a') as f:
            f.write(f'{url},{dest_file}\n')
        IMG_FILES[url] = dest_file

    return IMG_FILES[url]

def download_img(url: str, dest_file: str):
    if not os.path.isfile(dest_file):
        max_attempts = 10
        time_limit = 180 # in 3min
        start_time = time.time()

        for attempt in range(1, max_attempts + 1):
            try:
                wget.download(url, dest_file)
                return True
            except Exception as e:
                LOGGER.debug(f"Attempt {attempt} failed: {e}")
                if time.time() - start_time >= time_limit:
                    LOGGER.debug("Download timed out.")
                    break
                continue

        LOGGER.debug("Download failed after multiple attempts.")
        return False
    return True

def log_failed_img(data_id: str, url: str, dest_file: str):
    with open(IMG_DOWNLOAD_FAILED_LOGS, 'a') as f:
        f.write(f'{data_id},{url},{dest_file}\n')

def get_class_from_module(module_name, class_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except ModuleNotFoundError:
        return None

def make_data_dict(cur_id, cur_conversations):
    return {
        "id": cur_id,
        "conversations": [
            {
                "from": "user" if i % 2 == 0 else "assistant",
                "value": cur_conversations[i]
            } for i in range(len(cur_conversations))
        ]}

def make_data_dict_with_type(cur_id, cur_conversations, type: str):
    return make_data_dict(cur_id, cur_conversations) | {'type': type}

def is_last_char_punctuation(s):
    chinese_punctuation = '！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'
    all_punctuation = string.punctuation + chinese_punctuation
    return s[-1] in all_punctuation

remove_punctuation = lambda x: x[:-1] if len(x)>=1 and is_last_char_punctuation(x) else x

def choices_generate(golden: Union[str, List[str]], opool: List[str], total_num: int, sort: bool = True):
    pool = opool.copy()
    golden = golden if isinstance(golden, list) else [golden]
    try:
        assert all([i in pool for i in golden])
    except:
        print(golden, pool)
    for i in golden:
        pool.remove(i)
    choices = random.choices(pool, k=total_num-len(golden)) + golden
    random.shuffle(choices)
    if sorted:
        return choices, sorted([choices.index(i) for i in golden])
    else:
        return choices, [choices.index(i) for i in golden]

def save_results(data, data_id2file_name) -> None:
    with open(os.path.join(configs.JSON_SAVE_PATH, 'data.json'), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    map_csv_file = os.path.join(configs.JSON_SAVE_PATH, 'map.csv')
    write_map_csv_header = True if not os.path.isfile(map_csv_file) else False
    with open(map_csv_file, 'a', encoding='utf-8') as csv_file:
        if write_map_csv_header:
            csv_file.write("data_id,file_name\n")
        for key, value in data_id2file_name.items():
            csv_file.write(f"{key},{value}\n")

def parse_dict_arg(arg_str):
    try:
        parsed_dict = ast.literal_eval(arg_str)
        if not isinstance(parsed_dict, dict):
            raise ValueError("Input is not in a valid dictionary format.")
        return parsed_dict
    except (SyntaxError, ValueError):
        raise argparse.ArgumentTypeError("Unable to parse the input as a valid dictionary.")

def get_command_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp', type=str, default='meishichina')
    parser.add_argument('--infer', nargs='*', default=None, required=True)
    parser.add_argument("--fit-kwargs", type=parse_dict_arg, default={}, help="Provide a dictionary-like argument")

    args, _ = parser.parse_known_args()
    parser = ArgumentParser(parents=[parser], add_help=False)

    return args, parser

import pprint
_utils_pp = pprint.PrettyPrinter()
def pprint(x):
    _utils_pp.pprint(x)

class DataProcessHandle:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def update(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __str__(self):
        cur_str = ''
        prompt = ''
        if 'title' in self.data.keys() and self.data['title']:
            prompt += f'标题：{self.data["title"]}\n'
        if 'description' in self.data.keys() and self.data['description']:
            prompt += f'描述：{self.data["title"]}\n'
        if 'components_flat' in self.data.keys() and self.data['components_flat']:
            prompt += '，'.join([k + v for k, v in self.data['components_flat'].items()]) + '\n'
        if 'components_nested' in self.data.keys() and self.data['components_nested']:
            for idx, (k, v) in enumerate(self.data['components_nested'].items()):
                if idx > 0:
                    prompt += '，'
                prompt += k + ' '
                for idx, (l, s) in enumerate(v.items()):
                    if idx > 0:
                        prompt += '，'
                    prompt += l + s
            prompt += '。\n'
        if 'tips' in self.data.keys() and self.data['tips']:
            prompt += f'技巧：{self.data["title"]}\n'
        if 'steps' in self.data.keys() and self.data['steps']:
            prompt += '步骤：' + '，'.join([f"({cur_idx + 1}) {cur_step['description']}" for cur_idx, cur_step in enumerate(self.data['steps'])])

        return prompt