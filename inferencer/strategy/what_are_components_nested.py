import os
import random
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img, make_data_dict_with_type, choices_generate
from configs import IMG_SAVE_PATH

def what_are_components_nested(
    data: Dict[str, Any],
    what_are_components_nested_skipped_keys: List[str] = [],
    **kwargs) -> List[Any]:
    results = []

    cur_data_img = random.choice(data['img']) if isinstance(data['img'], list) else data['img']
    img_file_name = log_img(cur_data_img)
    img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

    # if os.path.isfile(img_file):
    #     LOGGER.warning(f'img has been downloaded in {what_are_components_nested.__name__}: [{img_file}]')

    # if not download_img(
    #     data['img'],
    #     img_file
    #     ):
    #     LOGGER.debug(f"img download failed, url: [{data['img']}]")
    #     log_failed_img(str(ID_COUNTER), data['img'], img_file)
    #     # return results

    for first_component in data['components_nested'].keys():
        if first_component in what_are_components_nested_skipped_keys:
            continue
        if not data['components_nested'][first_component]: # 空字典
            continue
        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_are_components_nested.__name__+'_first',
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜所需要的{first_component}由什么组成？",
                    f"，".join([i_second_componet for i_second_componet in data['components_nested'][first_component].keys()])
                ]
            )
        )
        ID_COUNTER.increment()
    for first_component in data['components_nested'].keys():
        ignore_str = ['适量', '少许']
        filtered_second_compoents = [k for k,v in data['components_nested'][first_component].items() if v not in ignore_str]
        for second_component in filtered_second_compoents:
            if first_component in what_are_components_nested_skipped_keys or second_component in what_are_components_nested_skipped_keys:
                continue

            # 增加数据的多样性，一次性可以询问多个成分
            second_component_list = [second_component]
            sample_size = random.choice(list(range(len(filtered_second_compoents))))
            if sample_size:
                second_component_list.extend(random.choices(filtered_second_compoents, k=sample_size))
            second_component_list = list(set(second_component_list))

            results.append(
                make_data_dict_with_type(
                    cur_id=str(ID_COUNTER),
                    type=what_are_components_nested.__name__+'_second',
                    cur_conversations=[
                        f"图：<img>{img_file}</img>，图中这道菜所需要的{first_component}中的{'，'.join(second_component_list)}有多少？",
                        '，'.join([i+'：'+data['components_nested'][first_component][i] for i in second_component_list])+'。'
                    ]
                )
            )
            ID_COUNTER.increment()

    return results

def what_are_components_nested_mcq(
    data: Dict[str, Any],
    opool: Dict[str, Any],
    what_are_components_nested_skipped_keys: List[str] = [],
    **kwargs) -> List[Any]:
    results = []

    cur_data_img = random.choice(data['img']) if isinstance(data['img'], list) else data['img']
    img_file_name = log_img(cur_data_img)
    img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

    for first_component in data['components_nested'].keys():
        if first_component in what_are_components_nested_skipped_keys:
            continue
        if not data['components_nested'][first_component]: # 空字典
            continue

        pool = opool['components_nested'][first_component]
        if not len(pool) > len(data['components_nested'][first_component]):
            continue
        what_are_components_nested_choices = min(len(data['components_nested'][first_component])*3, len(pool))
        choices, golden_idxs = choices_generate(list(data['components_nested'][first_component].keys()), pool, what_are_components_nested_choices)
        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_are_components_nested_mcq.__name__+'_first',
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜所需要的{first_component}由什么组成？\n选项：" 
                    + f"{'，'.join([chr(ord('A')+i)+'.'+choices[i] for i in range(len(choices))])}",
                    f"{''.join([chr(ord('A')+i) for i in golden_idxs])}"
                ]
            )
        )
        ID_COUNTER.increment()

    return results
