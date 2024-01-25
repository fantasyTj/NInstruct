import os
from typing import List, Any, Dict
import random, string

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, generate_hash, log_img
from configs import IMG_SAVE_PATH

def is_last_char_punctuation(s):
    chinese_punctuation = '！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'
    all_punctuation = string.punctuation + chinese_punctuation
    return s[-1] in all_punctuation

def how_to_finish_dish(data: Dict[str, Any], 
                       **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    cur_data_img = random.choice(data['img']) if isinstance(data['img'], list) else data['img']
    img_file_name = log_img(cur_data_img)
    img_file = os.path.join(IMG_SAVE_PATH, img_file_name)
    step_list = list(map(lambda x:x['description'] ,data['steps']))
    step_list = [i[:-1] if len(i)>=1 and is_last_char_punctuation(i) else i for i in step_list]
    step_list = list(filter(lambda x:len(x)>2 and '成品' not in x ,step_list)) # # 筛除steps_description中的噪音

    results.append(
        make_data_dict(
            cur_id=str(ID_COUNTER),
            cur_conversations=[
                random.choices([
                    f"图：<img>{img_file}</img>，这道菜怎么做？",
                    f"{data['title']}这道菜怎么做？",
                    f"图：<img>{img_file}</img>，这道{data['title']}怎么做？",  
                ], [0.5, 0.25, 0.25], k=1)[0],
                # f"图：<img>{img_file}</img>，这道菜怎么做？",
                # f"图：<img>{img_file}</img>，这道{data['title']}怎么做？",
                f"步骤如下：{'；'.join(step_list)}。"
            ]
        )
    )
    ID_COUNTER.increment()

    return results