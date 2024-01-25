import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER
from configs import IMG_SAVE_PATH

def what_is_next_step_no_img(
    data: Dict[str, Any],
    **kwargs) -> List[Any]:
    results = []
    filter_func = lambda x:len(x['description'])>2 and '成品' not in x['description'] # 筛除steps_description中的噪音
    if len(data['steps']) == 0:
        return results
    for i in range(len(data['steps'])-1):
        if not all([filter_func(data['steps'][i]), filter_func(data['steps'][i+1])]):
            continue
        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                #    response['指令'],
                #    response['输入'],
                #    response['输出']
                f'在做菜品{data["title"]}时，完成{data["steps"][i]["description"]}后，下一步是什么？',
                f'下一步是{data["steps"][i+1]["description"]}'
                ]
            )
        )
        ID_COUNTER.increment()
    return results