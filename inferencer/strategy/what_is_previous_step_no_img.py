import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, make_data_dict_with_type, choices_generate, remove_punctuation
from configs import IMG_SAVE_PATH

filter_func = lambda x:len(x)>3 and '成品' not in x # 筛除steps_description中的噪音

def what_is_previous_step_no_img(
    data: Dict[str, Any],
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    pool = list(map(lambda x: remove_punctuation(x['description']), data['steps']))
    for i in range(len(pool)-1, 0, -1):
        if not all([filter_func(pool[i]), filter_func(pool[i-1])]):
            continue

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_is_previous_step_no_img.__name__,
                cur_conversations=[
                f'在做菜品{data["title"]}时，“{pool[i]}”的上一步是什么？',
                f'上一步是{pool[i-1]}。'
                ]
            )
        )
        ID_COUNTER.increment()
    return results

def what_is_previous_step_no_img_cq(
    data: Dict[str, Any],
    opool: Dict[str, Any],
    what_is_previous_step_num_choices: int = 4,
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    pool = list(map(lambda x: remove_punctuation(x['description']), data['steps']))
    for i in range(len(pool)-1, 0, -1):
        if not all([filter_func(pool[i]), filter_func(pool[i-1])]):
            continue

        what_is_previous_step_num_choices = min(what_is_previous_step_num_choices, len(pool))
        choices, golden_idxs = choices_generate(pool[i-1], pool, what_is_previous_step_num_choices)

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_is_previous_step_no_img_cq.__name__,
                cur_conversations=[
                    f'在做菜品{data["title"]}时，“{pool[i-1]}”的上一步是什么？\n选项：'  
                    + f"{'，'.join([chr(ord('A')+i)+'.'+choices[i] for i in range(len(choices))])}",
                    f"{''.join([chr(ord('A')+i) for i in golden_idxs])}"
                ]
            )
        )
        ID_COUNTER.increment()
    return results