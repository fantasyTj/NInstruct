from .what_is_dish import what_is_dish, what_is_dish_cq
from .what_is_step_img_doing import what_is_step_img_doing, what_is_step_img_doing_cq
from .what_are_step_imgs_doing import what_are_step_imgs_doing, what_are_step_imgs_doing_cq
from .what_are_components_nested import what_are_components_nested, what_are_components_nested_mcq
from .what_are_components_flat import what_are_components_flat, what_are_components_flat_cq
from .how_to_sort_step_imgs import how_to_sort_step_imgs
from .what_is_next_step_no_img import what_is_next_step_no_img, what_is_next_step_no_img_cq
from .what_is_next_step_with_img import what_is_next_step_with_img, what_is_next_step_with_img_cq
from .what_is_previous_step_no_img import what_is_previous_step_no_img, what_is_previous_step_no_img_cq
from .what_is_previous_step_with_img import what_is_previous_step_with_img, what_is_previous_step_with_img_cq
from .how_to_finish_dish import how_to_finish_dish
from .what_new_task_generated_by_GPT import what_new_task_generated_by_GPT

STRATEGIES = {
    'what_is_dish': what_is_dish,
    'what_is_step_img_doing': what_is_step_img_doing,
    'what_are_step_imgs_doing': what_are_step_imgs_doing,
    'what_are_components_nested': what_are_components_nested,
    'what_are_components_flat': what_are_components_flat,
    'how_to_sort_step_imgs': how_to_sort_step_imgs,
    'what_is_next_step_no_img': what_is_next_step_no_img,
    'what_is_next_step_with_img': what_is_next_step_with_img,
    'what_is_previous_step_no_img': what_is_previous_step_no_img,
    'what_is_previous_step_with_img': what_is_previous_step_with_img,
    'how_to_finish_dish': how_to_finish_dish,
    'what_new_task_generated_by_GPT': what_new_task_generated_by_GPT
}

STRATEGIES_CQ = {
    'what_is_dish': what_is_dish_cq,
    'what_is_step_img_doing': what_is_step_img_doing_cq,
    'what_are_step_imgs_doing': what_are_step_imgs_doing_cq,
    'what_are_components_nested': what_are_components_nested_mcq,
    'what_are_components_flat': what_are_components_flat_cq,
    'what_is_next_step_no_img': what_is_next_step_no_img_cq,
    'what_is_next_step_with_img': what_is_next_step_with_img_cq,
    'what_is_previous_step_no_img': what_is_previous_step_no_img_cq,
    'what_is_previous_step_with_img': what_is_previous_step_with_img_cq
}
