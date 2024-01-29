import os
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img, make_data_dict_with_type, choices_generate, remove_punctuation
from configs import IMG_SAVE_PATH

filter_func = lambda x:len(x['description'])>3 and '成品' not in x['description'] # 筛除steps_description中的噪音

def what_is_step_img_doing(data: Dict[str, Any], **kwargs) -> List[Any]:
    results = []
    for idx, cur_step in enumerate(data['steps']):
        if not filter_func(cur_step):
            continue
        img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{what_is_step_img_doing.__name__}_{idx}.jpg")

        img_file_name = log_img(cur_step['img'])
        img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

        # if os.path.isfile(img_file):
        #     LOGGER.warning(f'img has been downloaded in {what_is_step_img_doing.__name__}: [{img_file}]')

        # if not download_img(
        #     cur_step['img'],
        #     img_file
        #     ):
        #     LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
        #     log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)
        #     # continue

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_is_step_img_doing.__name__,
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中在做什么？",
                    f"{remove_punctuation(cur_step['description'])}。"
                ]
            )
        )
        ID_COUNTER.increment()
    return results

def what_is_step_img_doing_cq(data: Dict[str, Any], 
                              opool: Dict[str, Any], 
                              what_is_step_img_doing_cq_choices: int = 4,
                              **kwargs) -> List[Any]:
    results = []
    pool = list(map(lambda x: remove_punctuation(x['description']), data['steps']))
    for idx, cur_step in enumerate(data['steps']):
        if not filter_func(cur_step):
            continue
        img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{what_is_step_img_doing.__name__}_{idx}.jpg")

        img_file_name = log_img(cur_step['img'])
        img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

        if not len(pool) > 1:
            continue
        what_is_step_img_doing_cq_choices = min(what_is_step_img_doing_cq_choices, len(pool))
        choices, golden_idxs = choices_generate(remove_punctuation(cur_step['description']), pool, what_is_step_img_doing_cq_choices)

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_is_step_img_doing_cq.__name__,
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中在做什么？\n选项："
                    + f"{'，'.join([chr(ord('A')+i)+'.'+choices[i] for i in range(len(choices))])}",
                    f"{''.join([chr(ord('A')+i) for i in golden_idxs])}"
                ]
            )
        )
        ID_COUNTER.increment()
    return results