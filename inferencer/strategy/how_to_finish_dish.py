import os
from typing import List, Any, Dict
import random, string

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, generate_hash, log_img, make_data_dict_with_type, is_last_char_punctuation, remove_punctuation
from configs import IMG_SAVE_PATH

def how_to_finish_dish(data: Dict[str, Any], 
                       **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    cur_data_img = random.choice(data['img']) if isinstance(data['img'], list) else data['img']
    img_file_name = log_img(cur_data_img)
    img_file = os.path.join(IMG_SAVE_PATH, img_file_name)
    pool = list(map(lambda x: remove_punctuation(x['description']) ,data['steps']))
    pool = list(filter(lambda x:len(x)>2 and '成品' not in x ,pool)) # # 筛除steps_description中的噪音
    
    if len(pool) == 0:
        return results
    results.append(make_data_dict_with_type(
            cur_id=str(ID_COUNTER),
            type=how_to_finish_dish.__name__,
            cur_conversations=[
                random.choices([
                    f"图：<img>{img_file}</img>，这道菜怎么做？",
                    f"{data['title']}这道菜怎么做？",
                    f"图：<img>{img_file}</img>，这道{data['title']}怎么做？",  
                ], [0.5, 0.25, 0.25], k=1)[0],
                f"步骤如下：{'；'.join(pool)}。"
            ]
        )
    )
    ID_COUNTER.increment()

    return results