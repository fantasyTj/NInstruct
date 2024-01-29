import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, generate_hash, log_img, make_data_dict_with_type, choices_generate, remove_punctuation
from configs import IMG_SAVE_PATH

def what_are_step_imgs_doing(
    data: Dict[str, Any],
    what_are_step_num_imgs: int = 3,
    what_are_step_num_iters: int = 1,
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results

    what_are_step_num_imgs = min(len(data['steps']), random.choice(range(2, what_are_step_num_imgs + 1)))
    for _ in range(what_are_step_num_iters):
        cur_sampled = random.sample(range(len(data['steps'])), what_are_step_num_imgs)
        img_file_list = []
        for img_idx in cur_sampled:
            cur_step = data['steps'][img_idx]

            img_file_name = log_img(cur_step['img'])
            img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

            # if not download_img(
            #     cur_step['img'],
            #     img_file
            #     ):
            #     LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
            #     log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)
            #     # continue

            img_file_list.append(img_file)

        if len(img_file_list) != len(cur_sampled):
            continue

        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_are_step_imgs_doing.__name__,
                cur_conversations=[
                    '，'.join([f"({cur_idx + 1}) <img>{cur_img_file}</img>" for cur_idx, cur_img_file in enumerate(img_file_list)])
                        + f"，这些图中在做什么？",
                    '；'.join([f"图 ({cur_idx + 1})：{remove_punctuation(data['steps'][img_idx]['description'])}" for cur_idx, img_idx in enumerate(cur_sampled)]) + '。'
                ]
            )
        )
        ID_COUNTER.increment()
    return results

def what_are_step_imgs_doing_cq(
    data: Dict[str, Any],
    opool: Dict[str, Any],
    what_are_step_num_imgs: int = 3,
    what_are_step_num_iters: int = 1,
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    filter_func = lambda x: len(x['description'])>3 and '成品' not in x['description']
    step_list = list(filter(filter_func, data['steps']))
    pool = list(map(lambda x: remove_punctuation(x['description']), step_list))
    what_are_step_num_imgs = min(len(step_list), what_are_step_num_imgs)
    if what_are_step_num_imgs < 2:
        return results
    for _ in range(what_are_step_num_iters):
        cur_sampled = random.sample(range(len(step_list)), random.choice(range(2, what_are_step_num_imgs + 1)))
        img_file_list = []
        for img_idx in cur_sampled:
            cur_step = step_list[img_idx]

            img_file_name = log_img(cur_step['img'])
            img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

            img_file_list.append(img_file)

        if len(img_file_list) != len(cur_sampled):
            continue
        what_are_step_num_choices = min(what_are_step_num_imgs*3, len(pool))
        choices, golden_idxs = choices_generate([pool[i] for i in cur_sampled], pool, what_are_step_num_choices, sort=False)
        results.append(
            make_data_dict_with_type(
                cur_id=str(ID_COUNTER),
                type=what_are_step_imgs_doing_cq.__name__,
                cur_conversations=[
                    '，'.join([f"({cur_idx + 1}) <img>{cur_img_file}</img>" for cur_idx, cur_img_file in enumerate(img_file_list)])
                        + f"，这些图中在做什么？请按顺序为{'、'.join(['图'+str(idx+1) for idx in range(len(img_file_list))])}选择进行选择。\n选项：" 
                        + f"{'，'.join([chr(ord('A')+i)+'.'+choices[i] for i in range(len(choices))])}",
                    f"{''.join(['图'+str(i)+chr(ord('A')+idx) for i, idx in enumerate(golden_idxs)])}"
                ]
            )
        )
        ID_COUNTER.increment()
    return results