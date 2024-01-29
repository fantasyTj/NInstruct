import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img, make_data_dict_with_type, choices_generate, remove_punctuation
from configs import IMG_SAVE_PATH

filter_func = lambda x:len(x['description'])>3 and '成品' not in x['description'] # 筛除steps_description中的噪音

def what_is_previous_step_with_img(data: Dict[str, Any], what_is_previous_step_num_iters: int = 1, **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results

    cur_steps = random.sample(
        list(range(len(data['steps']) - 1)),
        min(what_is_previous_step_num_iters, len(data['steps']) - 1)
        )
    for i in cur_steps:
        cur_step = data['steps'][i]
        pre_step = data['steps'][i - 1]
        if not all([filter_func(cur_step), filter_func(pre_step)]):
            continue

        img_file_name = log_img(cur_step['img'])
        img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

        # if os.path.isfile(img_file):
        #     LOGGER.warning(
        #         f'img has been downloaded in {what_is_next_step_with_img.__name__}: [{img_file}]'
        #     )

        # if not download_img(cur_step['img'], img_file):
        #     LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
        #     log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_is_previous_step_with_img.__name__,
                cur_conversations=[
                    f'在做菜品{data["title"]}时，图<img>{img_file}</img>的上一步是什么？',
                    f'下一步是{remove_punctuation(pre_step["description"])}。'
                ]))
        ID_COUNTER.increment()
    return results

def what_is_previous_step_with_img_cq(data: Dict[str, Any], 
                                  opool: Dict[str, Any],
                                  what_is_previous_step_num_iters: int = 1, 
                                  what_is_previous_step_num_choices: int = 4,
                                  **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    pool = list(map(lambda x: remove_punctuation(x['description']), data['steps']))
    cur_steps = random.sample(
            list(range(len(data['steps']) - 1)),
            min(what_is_previous_step_num_iters, len(data['steps']) - 1)
        )
    for i in cur_steps:
        cur_step = data['steps'][i]
        pre_step = data['steps'][i - 1]
        if not all([filter_func(cur_step), filter_func(pre_step)]):
            continue

        img_file_name = log_img(cur_step['img'])
        img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

        if not len(pool) > 1:
            continue
        what_is_previous_step_num_choices = min(what_is_previous_step_num_choices, len(pool))
        choices, golden_idxs = choices_generate(remove_punctuation(pre_step['description']), pool, what_is_previous_step_num_choices)

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_is_previous_step_with_img_cq.__name__,
                cur_conversations=[
                    f'在做菜品{data["title"]}时，图<img>{img_file}</img>的上一步是什么？\n选项'  
                    + f"{'，'.join([chr(ord('A')+i)+'.'+choices[i] for i in range(len(choices))])}",
                    f"{''.join([chr(ord('A')+i) for i in golden_idxs])}"
                ]))
        ID_COUNTER.increment()
    return results
