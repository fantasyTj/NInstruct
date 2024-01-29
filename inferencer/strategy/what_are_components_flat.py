import os
import random
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img, make_data_dict_with_type, choices_generate
from configs import IMG_SAVE_PATH

def what_are_components_flat(
    data: Dict[str, Any],
    what_are_components_flat_skipped_keys: List[str] = [],
    **kwargs) -> List[Any]:
    results = []

    cur_data_img = random.choice(data['img']) if isinstance(data['img'], list) else data['img']
    img_file_name = log_img(cur_data_img)
    img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

    # if os.path.isfile(img_file):
    #     LOGGER.warning(f'img has been downloaded in {what_are_components_flat.__name__}: [{img_file}]')

    # if not download_img(
    #     data['img'],
    #     img_file
    #     ):
    #     LOGGER.debug(f"img download failed, url: [{data['img']}]")
    #     log_failed_img(str(ID_COUNTER), data['img'], img_file)
        # return results

    for first_component in data['components_flat'].keys():
        if first_component in what_are_components_flat_skipped_keys:
            continue
        
        # 增加数据的多样性，一次性可以询问多个成分
        first_component_list = [first_component]
        sample_size = random.choice(list(range(len(data['components_flat'].keys()))))
        if sample_size:
            first_component_list.extend(random.choices(list(data['components_flat'].keys()), k=sample_size))
        first_component_list = list(set(first_component_list))

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_are_components_flat.__name__,
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜的{'，'.join(first_component_list)}如何？",
                    '，'.join([i+'：'+data['components_flat'][i] for i in first_component_list])+'。'
                ]
            )
        )
        ID_COUNTER.increment()

    return results

def what_are_components_flat_cq(
    data: Dict[str, Any],
    opool: Dict[str, Any],
    what_are_components_flat_skipped_keys: List[str] = [],
    what_are_components_flat_choices: int = 4,
    **kwargs) -> List[Any]:
    results = []

    cur_data_img = random.choice(data['img']) if isinstance(data['img'], list) else data['img']
    img_file_name = log_img(cur_data_img)
    img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

    for first_component in data['components_flat'].keys():
        if first_component in what_are_components_flat_skipped_keys:
            continue
        
        pool = opool['components_flat'][first_component]
        if not len(pool) > 1:
            continue
        what_are_components_flat_choices = min(what_are_components_flat_choices, len(pool))
        choices, golden_idxs = choices_generate(data['components_flat'][first_component], pool, what_are_components_flat_choices)
        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_are_components_flat_cq.__name__,
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜的{first_component}如何？\n选项："  
                    + f"{'，'.join([chr(ord('A')+i)+'.'+choices[i] for i in range(len(choices))])}",
                    f"{''.join([chr(ord('A')+i) for i in golden_idxs])}"
                ]
            )
        )
        ID_COUNTER.increment()

    return results
