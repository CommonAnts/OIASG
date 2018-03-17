#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .data import data
from .resource import resource

vars = {}

def init():
	vars.update(data.get_all_dict(['UI'])) # 引入命名空间
	globals().update(vars)
	# 预加载资源
			
	normal_button_back = resource.load_image(NORMAL_BUTTON_BACK)
	normal_button_pressed_back = resource.load_image(NORMAL_BUTTON_PRESSED_BACK)
	normal_menu_back = resource.load_image(NORMAL_MENU_BACK)
	normal_page_back = resource.load_image(NORMAL_PAGE_BACK)
	normal_default_image = resource.load_image(NORMAL_DEFAULT_IMAGE)
	normal_slider_back = resource.load_image(NORMAL_SLIDER_BACK)
	normal_slider_cursor = resource.load_image(NORMAL_SLIDER_CURSOR)
	normal_checkbox_unchecked_back = resource.load_image(NORMAL_CHECKBOX_UNCHECKED_BACK)
	normal_checkbox_checked_back = resource.load_image(NORMAL_CHECKBOX_CHECKED_BACK)
	normal_scrollbar_back = resource.load_image(NORMAL_SCROLLBAR_BACK)
	normal_scrollbar_cursor = resource.load_image(NORMAL_SCROLLBAR_CURSOR)
	normal_switchbutton_back = resource.load_image(NORMAL_SWITCHBUTTON_BACK)
	normal_switchbutton_select_back = resource.load_image(NORMAL_SWITCHBUTTON_SELECT_BACK)
	normal_tag_rv_back = resource.load_image(NORMAL_TAG_RV_IMAGE)
	normal_tag_rv_selected_back = resource.load_image(NORMAL_TAG_RV_SELECTED_IMAGE)
	normal_progress_bar_front = resource.load_image(NORMAL_PROGRESS_BAR_FRONT)
	normal_progress_bar_back = resource.load_image(NORMAL_PROGRESS_BAR_BACK)
	normal_message_back = resource.load_image(NORMAL_MESSAGE_BACK)

	main_menu_back = resource.load_image(MAIN_MENU_BACK)
	main_menu_start_back = resource.load_image(MAIN_MENU_START_BACK)
	main_menu_start_pressed_back = resource.load_image(MAIN_MENU_START_PRESSED_BACK)

	game_header_back = resource.load_image(GAME_HEADER_BACK)
	# game_header_speedbar_back = resource.load_image(GAME_HEADER_SPEEDBAR_BACK)
	game_header_speedbar_button_back = resource.load_image(GAME_HEADER_SPEEDBAR_BUTTON_BACK)
	game_header_speedbar_pressed_back = resource.load_image(GAME_HEADER_SPEEDBAR_BUTTON_PRESSED_BACK)

	game_pages_character_back = resource.load_image(GAME_PAGES_CHARACTER_BACK)
	game_pages_timetable_back = resource.load_image(GAME_PAGES_TIMETABLE_BACK)
	game_pages_ability_back = resource.load_image(GAME_PAGES_ABILITY_BACK)
	game_pages_contest_back = resource.load_image(GAME_PAGES_CONTEST_BACK)

	game_header_status_bar_icons = [resource.load_image(i) for i in GAME_HEADER_STATUS_BAR_ICONS]

	game_header_switchpage_icons = [resource.load_image(i) for i in GAME_HEADER_SWITCHPAGE_ICONS]
	game_header_switchpage_disabled_icons = [(resource.load_image(i) if i is not None else None) for i in GAME_HEADER_SWITCHPAGE_DISABLED_ICONS]
	game_header_switchpage_button_select_back = resource.load_image(GAME_HEADER_SWITCHPAGE_BUTTON_SELECT_BACK)

	game_header_switch_down_icon = resource.load_image(GAME_HEADER_SWITCH_DOWN_ICON)
	game_header_switch_up_icon = resource.load_image(GAME_HEADER_SWITCH_UP_ICON)
	game_header_switch_disabled_image = resource.load_image(GAME_HEADER_SWITCH_DISABLED_IMAGE)

	game_board_back = resource.load_image(GAME_BOARD_BACK)

	game_message_timetable_back = resource.load_image(GAME_MESSAGE_TIMETABLE_BACK)
	game_message_log_back = resource.load_image(GAME_MESSAGE_LOG_BACK)
	game_message_strategy_back = resource.load_image(GAME_MESSAGE_STRATEGY_BACK)
	game_message_strategy_select_back = resource.load_image(GAME_MESSAGE_STRATEGY_SELECT_BACK)
	game_message_strategy_cursor = resource.load_image(GAME_MESSAGE_STRATEGY_CURSOR)
	
	game_slplan_button_back = resource.load_image(GAME_SLPLAN_BUTTON_BACK)
	game_slplan_button_pressed_back = resource.load_image(GAME_SLPLAN_BUTTON_PRESSED_BACK)
	game_slplan_info_back = resource.load_image(GAME_SLPLAN_INFO_BACK)
	game_slplan_copy_icon = resource.load_image(GAME_SLPLAN_COPY_ICON)
	game_slplan_remove_icon = resource.load_image(GAME_SLPLAN_REMOVE_ICON)
	game_slplan_use_icon = resource.load_image(GAME_SLPLAN_USE_ICON)
	game_slplan_rename_icon = resource.load_image(GAME_SLPLAN_RENAME_ICON)
	game_slplan_confirm_image = resource.load_image(GAME_SLPLAN_CONFIRM_IMAGE)
	
	game_pages_timetable_plan_add_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_ADD_ICON)
	game_pages_timetable_plan_edit_icon	= resource.load_image(GAME_PAGES_TIMETABLE_PLAN_EDIT_ICON)
	game_pages_timetable_plan_remove_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_REMOVE_ICON)
	game_pages_timetable_plan_save_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_SAVE_ICON)
	# game_pages_timetable_plan_load_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_LOAD_ICON)
	game_pages_timetable_plan_moveup_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_MOVEUP_ICON)
	game_pages_timetable_plan_movedown_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_MOVEDOWN_ICON)
	game_pages_timetable_plan_shiftup_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_SHIFTUP_ICON)
	game_pages_timetable_plan_shiftdown_icon = resource.load_image(GAME_PAGES_TIMETABLE_PLAN_SHIFTDOWN_ICON)
	
	game_pages_timetable_frame_back = resource.load_image(GAME_PAGES_TIMETABLE_FRAME_BACK)
	game_pages_timetable_frame_left_button_image = resource.load_image(GAME_PAGES_TIMETABLE_FRAME_LEFT_BUTTON_IMAGE)
	game_pages_timetable_frame_right_button_image = resource.load_image(
	GAME_PAGES_TIMETABLE_FRAME_RIGHT_BUTTON_IMAGE)
	game_pages_timetable_frame_plan_button_back = resource.load_image(GAME_PAGES_TIMETABLE_FRAME_PLAN_BUTTON_BACK)
	game_pages_timetable_frame_plan_button_pressed_back = resource.load_image(GAME_PAGES_TIMETABLE_FRAME_PLAN_BUTTON_PRESSED_BACK)
	
	vars.update(locals())
	globals().update(locals())