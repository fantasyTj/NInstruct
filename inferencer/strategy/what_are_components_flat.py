import os
import random
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img
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
        first_component_list = []
        sample_size = random.choice(list(range(len(data['components_flat'].keys()))))
        if sample_size:
            first_component_list.extend(random.choices(list(data['components_flat'].keys()), k=sample_size))
        if first_component not in first_component_list:
            first_component_list.append(first_component)
        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                # cur_conversations=[
                #     f"图：<img>{img_file}</img>，图中这道菜的{first_component}如何？",
                #     f"{data['components_flat'][first_component]}。"
                # ]
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜的{'，'.join(first_component_list)}如何？",
                    '，'.join([i+'：'+data['components_flat'][i] for i in first_component_list])+'。'
                ]
            )
        )
        ID_COUNTER.increment()

    return results
