import os
import random
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img
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
        if data['components_nested'][first_component]: # 空字典
            continue
        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜所需要的{first_component}有哪些？",
                    f"，".join([i_second_componet for i_second_componet in data['components_nested'][first_component].keys()])
                ]
            )
        )
        ID_COUNTER.increment()
    for first_component in data['components_nested'].keys():
        for second_component in data['components_nested'][first_component].keys():
            if first_component in what_are_components_nested_skipped_keys or second_component in what_are_components_nested_skipped_keys:
                continue

            # 增加数据的多样性，一次性可以询问多个成分
            second_component_list = []
            sample_size = random.choice(list(range(len(data['components_nested'][first_component].keys()))))
            if sample_size:
                second_component_list.extend(random.choices(list(data['components_nested'][first_component].keys()), k=sample_size))
            if second_component not in second_component_list:
                second_component_list.append(second_component)
            results.append(
                make_data_dict(
                    cur_id=str(ID_COUNTER),
                    # cur_conversations=[
                    #     f"图：<img>{img_file}</img>，图中这道菜所需要的{first_component}：{second_component}有多少？",
                    #     f"{data['components_nested'][first_component][second_component]}。"
                    # ]
                    cur_conversations=[
                        f"图：<img>{img_file}</img>，图中这道菜所需要的{first_component}中的{'，'.join(second_component_list)}有多少？",
                        '，'.join([i+'：'+data['components_nested'][first_component][i] for i in second_component_list])+'。'
                    ]
                )
            )
            ID_COUNTER.increment()

    return results
