from typing import Dict, Any, List, Tuple, Optional

from inferencer.strategy import STRATEGIES, STRATEGIES_CQ

class BaseInferencer():
    def __init__(self,
                 types: List[str]) -> None:
        self.inference_funcs = {
            i: STRATEGIES[i] for i in filter(lambda x: x in STRATEGIES, types)
            }
        self.inference_cq_funcs = {
            i: STRATEGIES_CQ[i] for i in filter(lambda x: x in STRATEGIES_CQ, types)
            }

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Subclass must implement the 'load' method")

    def fit(self,
            data: Dict[str, Any],
            pool: Optional[Dict[str, Any]] = None,
            **kwargs) -> List[Any]:
        results = []
        for cur_stra in self.inference_funcs.keys():
            results.extend(self.inference_funcs[cur_stra](data, **kwargs))
        for cur_stra in self.inference_cq_funcs.keys():
            results.extend(self.inference_cq_funcs[cur_stra](data, pool, **kwargs))
        return results
    