#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from noroi.core import DivTypes, DivStatus, Alignment, AnchorEdges, Key
from noroi.wrapper import HexMaster
import threading
import datetime
import time

input_status = "Awaiting input.."
no_input_counter = 0
no_input_limit = 20

def handle_post_frame():
    global no_input_counter
    global input_status
    no_input_counter = 0
    input_status = "Input received."

def handle_no_input():
    global no_input_counter
    global no_input_limit
    global input_status
    if( no_input_counter < no_input_limit ):
        no_input_counter += 1
    elif( no_input_counter == no_input_limit ):
        input_status = "No input received for " + str(no_input_counter) + " frames."
        no_input_counter += 1

hex_master_setup = \
{
    "no_input_frame_update" : handle_no_input,
    "post_input_frame_update": handle_post_frame,
}

hex_master = HexMaster(hex_master_setup)

main = \
{
    "name" : "main",
    "type" : DivTypes.DIV,

    "height" : 1.0,
    "width" : 1.0,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [1,0, 444], "fg": [999,49,0] },
    },

    "horizontal_alignment" : Alignment.CENTER,
    "vertical_alignment" : Alignment.CENTER,
}

banner = \
{
    "name" : "banner",
    "type" : DivTypes.LABEL,

    "height" : 3,
    "width" : .7,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [501,500, 444], "fg": [499,49,499] },
    },

    "inner":
    {
        "value": "Noroi Example",
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_alignment" : Alignment.CENTER,
    },

    "parent": "main",

    "horizontal_alignment" : Alignment.CENTER,

    "vertical_margin": 1,
}

status_bar = \
{
    "name" : "status_bar",
    "type" : DivTypes.LABEL,

    "height" : 1,
    "width" : 1.0,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [0,0,0], "fg": [450,450,450] },
    },

    "inner":
    {
        "value": "status...",
        "horizontal_margin": 1,
    },

    "horizontal_alignment" : Alignment.CENTER,

    "anchors":
    {
        "vertical":
        {
            "latch_to_div": "main",
            "edge_of_target_div": AnchorEdges.BOTTOM
        },
    },

}

quit_popup = \
{
    "name" : "quit_popup",
    "type" : DivTypes.LABEL,

    "height" : 0.4,
    "width" : 0.5,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [301,0, 444], "fg": [999,49,0] },
    },

    "horizontal_alignment" : Alignment.CENTER,
    "vertical_alignment" : Alignment.CENTER,

    "inner":
    {
        "value": "You're leaving already?",
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_margin": 0.20,
    },
}

def quit_program(div, hex_master):
    hex_master.terminate()

verify_quit_button = \
{
    "name" : "verify_quit_button",
    "type" : DivTypes.BUTTON,
    "inner":
    {
        "value": "AYE",
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_alignment" : Alignment.CENTER,
    },

    "height" : 3,
    "width" : 7,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [321,0, 0], "fg": [999,49,0] },
        DivStatus.FOCUSED : { "bg": [671,0, 0], "fg": [59,0,0] },
        DivStatus.DISABLED : { "bg": [121,0, 0], "fg": [0,0,30] }
    },

    "parent": "quit_popup",

    "horizontal_alignment" : Alignment.END,
    "vertical_alignment" : Alignment.END,

    "horizontal_margin": -.15,
    "vertical_margin": -3,

    "key_map":
    {
        "interact" : Key.ENTER.value,
        "switch_focus" :
        {
            Key.LEFT : "cancel_quit_button",
        }
    },

    "on_interact": quit_program,

}

def cancel_quit(key, hex_master):
    hex_master.remove_div("quit_popup")
    hex_master.focus("quit_button")

cancel_quit_button = \
{
    "name" : "cancel_quit_button",
    "type" : DivTypes.BUTTON,
    "inner":
    {
        "value": "NAY",
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_alignment" : Alignment.CENTER,
    },

    "height" : 3,
    "width" : 7,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [321,0, 0], "fg": [999,49,0] },
        DivStatus.FOCUSED : { "bg": [671,0, 0], "fg": [59,0,0] },
        DivStatus.DISABLED : { "bg": [121,0, 0], "fg": [0,0,30] }
    },

    "parent": "quit_popup",

    "vertical_alignment" : Alignment.END,

    "horizontal_margin": .15,
    "vertical_margin": -3,

    "key_map":
    {
        "interact" : Key.ENTER.value,
        "switch_focus" :
        {
            Key.RIGHT : "verify_quit_button",
        }
    },
    "on_interact": cancel_quit
}

def popup_quit(key, hex_master):
    hex_master.add_div(quit_popup)
    hex_master.add_div(verify_quit_button)
    hex_master.add_div(cancel_quit_button, focus=True)

quit_button = \
{
    "name" : "quit_button",
    "type" : DivTypes.BUTTON,

    "inner":
    {
        "value": "Quit",
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_margin": 1,
    },

    "height" : 3,
    "width" : 0.2,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [321,0, 0], "fg": [999,49,0] },
        DivStatus.FOCUSED : { "bg": [671,0, 0], "fg": [59,0,0] },
        DivStatus.DISABLED : { "bg": [121,0, 0], "fg": [0,0,30] }
    },

    "parent": "main",

    "horizontal_alignment" : Alignment.END,
    "vertical_alignment" : Alignment.END,

    "horizontal_margin": -10,
    "vertical_margin": -10,

    "key_map":
    {
        "interact" : Key.ENTER.value,
        "switch_focus" :
        {
            Key.UP : "enable_text_button",
            Key.LEFT : "some_text",
        }
    },

    "on_interact": popup_quit,
}

some_text = \
{
    "name" : "some_text",
    "type" : DivTypes.TEXT_AREA,
    "inner":
    {
        "value": "Use the arrow keys to switch focus between the TUI elements you see here.\n\n<Enter> key interacts with buttons and this text area.\n\nTo start editing the text, simply enable this part here with that button on the right, then switch focus and interact.\n\nOnce activated, you can use the arrow keys to navigate within the text area.\n\nIt's quite basic, really. Word wrapping and some conventional shortcuts will be added in the future.\n\nTo quit editing, press <Escape> to deactivate the text area. Finally, you can disable the text area with the same button from earlier, which should read \"← Disable Text Area\" now.\n\nAlso, there's a status bar below, if you haven't noticed.\n\nThat's all. Go nuts!",
        "width": 0.9,
        "height": 0.9,
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_alignment" : Alignment.CENTER,
    },

    "width": .4,
    "height": .54,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [0,321, 0], "fg": [700,700,730] },
        DivStatus.FOCUSED : { "bg": [0,671, 0], "fg": [59,0,0] },
        DivStatus.ACTIVE : { "bg": [0,121, 900], "fg": [900,900,930] },
        DivStatus.DISABLED : { "bg": [0,121, 0], "fg": [300,300,330] },
        "cursor" : { "bg": [0,321, 0], "fg": [999,49,0] },
    },

    "parent": "main",

    "vertical_alignment" : Alignment.CENTER,

    "horizontal_margin": .14,

    "key_map":
    {
        "activate" : Key.ENTER.value,
        "deactivate" : Key.ESC.value,
        "switch_focus" :
        {
            Key.RIGHT : "enable_text_button",
        },
        "active" :
        {
            "left": Key.LEFT.value,
            "right": Key.RIGHT.value,
            "up": Key.UP.value,
            "down": Key.DOWN.value,
            "backspace": Key.BACKSPACE.value,
            "delete": Key.DELETE.value,
            "home": Key.HOME.value,
            "end": Key.END.value,
            "page_up": Key.PAGE_UP.value,
            "page_down": Key.PAGE_DOWN.value,
        }
    },
}

def toggle_text_area(div, hex_master):
    if( hex_master.div_status("some_text") == DivStatus.DISABLED ):
        hex_master.enable_div("some_text")
        div._setup["inner"]["value"] = "← Disable Text Area"
    elif( hex_master.div_status("some_text") == DivStatus.IDLE ):
        hex_master.disable_div("some_text")
        div._setup["inner"]["value"] = "← Enable Text Area"

enable_text_button = \
{
    "name" : "enable_text_button",
    "type" : DivTypes.BUTTON,
    "inner":
    {
        "value": "← Enable Text Area",
        "horizontal_alignment" : Alignment.CENTER,
        "vertical_alignment" : Alignment.CENTER,
    },

    "height" : 3,
    "width" : .2,

    "colors" :
    {
        DivStatus.IDLE : { "bg": [0,321, 0], "fg": [49,999,0] },
        DivStatus.FOCUSED : { "bg": [0,671, 0], "fg": [59,0,0] },
        DivStatus.DISABLED : { "bg": [0,121, 0], "fg": [0,0,30] }
    },

    "parent": "main",

    "horizontal_alignment" : Alignment.END,

    "horizontal_margin": -10,
    "vertical_margin": 10,

    "key_map":
    {
        "interact" : Key.ENTER.value,
        "switch_focus" :
        {
            Key.DOWN : "quit_button",
            Key.LEFT : "some_text",
        }
    },

    "on_interact": toggle_text_area,
}

keep_looping = True
def date_loop():
    while(keep_looping):
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        status_bar["inner"]["value"] = now + " | " + input_status
        time.sleep(.25)

x = threading.Thread(target=date_loop)
x.start()

hex_master.add_div(main)
hex_master.add_div(banner)
hex_master.add_div(status_bar)
hex_master.add_div(quit_button)
hex_master.add_div(enable_text_button, focus=True)
hex_master.add_div(some_text, start_disabled=True)

scr_height = 36
scr_width = 108

hex_master.start(size=[scr_height, scr_width])

keep_looping = False
x.join()
