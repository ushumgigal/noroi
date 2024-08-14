import curses
import numpy
import os
from enum import Enum

def resize(scr, new_height, new_width):
    os.system("printf '\033[8;" + str(new_height) + ";" + str(new_width) + "t'")
    scr.clear()
    curses.resizeterm(new_height, new_width)
    scr.refresh()

class Attribute(Enum):

    BLINK = curses.A_BLINK
    BOLD = curses.A_BOLD
    DIM = curses.A_DIM
    REVERSE = curses.A_REVERSE
    STANDOUT = curses.A_STANDOUT
    UNDERLINE = curses.A_UNDERLINE

class Key(Enum):

    LEFT = 260
    RIGHT = 261
    UP = 259
    DOWN = 258
    SPACE = " "
    ENTER = "\n"
    ESC = ""
    BACKSPACE = 263
    DELETE = 330
    INSERT = 331
    HOME = 262
    END = 360
    PAGE_UP = 339
    PAGE_DOWN = 338
    F1 = 265
    F2 = 266
    F3 = 267
    F4 = 268
    F5 = 269
    F6 = 270
    F7 = 271
    F8 = 272
    F9 = 273
    F10 = 274
    F11 = 275
    F12 = 276
    TAB = "	"

class DivStatus(Enum):

    IDLE = 0
    FOCUSED = 1
    ACTIVE = 2
    DISABLED = 3

class Alignment(Enum):

    END = 0
    CENTER = 1

class AnchorEdges(Enum):

    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3

class DivTypes(Enum):

    DIV = 0
    LABEL = 1
    BUTTON = 2
    TEXT_AREA = 3

class ColorHandler:

    def __init__(self):
        self.__next_color_id = 0
        self.__next_color_pair_id = 0
        self.__colors = {}
        self.__color_pairs = {}

    def reset(self):
        self.__next_color_id = 0
        self.__next_color_pair_id = 0
        self.__colors = {}
        self.__color_pairs = {}

    def add_color_pair(self, color_pair):
        if(not (str(color_pair["fg"]) in self.__colors)):
            self.__next_color_id += 1

            if(self.__next_color_id >= curses.COLORS):
                err_msg = "Error: Too many colors. Should not exceed " + str(curses.COLORS) + " for this VT."
                raise ValueError(err_msg)

            self.__colors[str(color_pair["fg"])] = self.__next_color_id
            curses.init_color(
                self.__colors[str(color_pair["fg"])],
                color_pair["fg"][0],
                color_pair["fg"][1],
                color_pair["fg"][2] )

        if(not (str(color_pair["bg"]) in self.__colors)):
            self.__next_color_id += 1

            if(self.__next_color_id >= curses.COLORS):
                err_msg = "Error: Too many colors. Should not exceed " + str(curses.COLORS) + " for this VT."
                raise ValueError(err_msg)

            self.__colors[str(color_pair["bg"])] = self.__next_color_id
            curses.init_color(
                self.__colors[str(color_pair["bg"])],
                color_pair["bg"][0],
                color_pair["bg"][1],
                color_pair["bg"][2] )

        if(not (str(color_pair) in self.__color_pairs)):
            self.__next_color_pair_id += 1

            if(self.__next_color_pair_id >= curses.COLOR_PAIRS):
                err_msg = "Error: Too many color pairs. Should not exceed " + str(curses.COLOR_PAIRS) + " for this VT."
                raise ValueError(err_msg)

            self.__color_pairs[str(color_pair)] = self.__next_color_pair_id

            curses.init_pair(
                self.__color_pairs[str(color_pair)],
                self.__colors[str(color_pair["fg"])],
                self.__colors[str(color_pair["bg"])] )
        return curses.color_pair(self.__color_pairs[str(color_pair)])


class Div:

    def __end_align(self, start, end, size):
        outer_size = end - start + 1
        return end - size + 1

    def __center_align(self, start, end, size):
        outer_size = end - start + 1
        return start + int( (outer_size-size) /2)

    def __init__(self, setup):
        self._setup = setup

        self.status = DivStatus.IDLE
        self._spot_x = 0
        self._spot_y = 0

        self._aligners = {}
        self._aligners[Alignment.END] = self.__end_align
        self._aligners[Alignment.CENTER] = self.__center_align

        self._current_width = 0
        self._current_height = 0

        self._current_horizontal_margin = 0
        self._current_vertical_margin = 0

    def _relative_size(self, rate, outer_size):
        relative_size = int(outer_size*rate) - 1
        return relative_size

    def visual_update(self, scr, divs, color_handler):
        parent_exists = (self._setup.get("parent") is not None)

        parent_width = curses.COLS if (not parent_exists) else divs[self._setup["parent"]]._current_width
        parent_height = curses.LINES if (not parent_exists) else divs[self._setup["parent"]]._current_height

        if( isinstance(self._setup["width"], int) ):
            self._current_width = self._setup["width"]
        elif( isinstance(self._setup["width"], float) ):
            self._current_width = self._relative_size( self._setup["width"], parent_width)
        else:
            err_msg = "Error: Div width may only be of type int or float."
            raise ValueError(err_msg)

        if( isinstance(self._setup["height"], int) ):
            self._current_height = self._setup["height"]
        elif( isinstance(self._setup["height"], float) ):
            self._current_height = self._relative_size( self._setup["height"], parent_height)
        else:
            err_msg = "Error: Div height may only be of type int or float."
            raise ValueError(err_msg)

        if( (self._current_width >= curses.COLS) or (self._current_height >= curses.LINES) ):
            new_height = max(self._current_height+1, curses.LINES)
            new_width =  max(self._current_width+1, curses.COLS)
            resize(scr, new_height, new_width)

        color_pair = color_handler.add_color_pair(self._setup["colors"][self.status])

        row = ""

        if( self._setup.get("horizontal_alignment") is not None):
            if(parent_exists):
                self._spot_x = self._aligners[self._setup["horizontal_alignment"]](
                    divs[self._setup["parent"]]._spot_x,
                    divs[self._setup["parent"]]._spot_x + divs[self._setup["parent"]]._current_width - 1,
                    self._current_width )
            else:
                self._spot_x = self._aligners[self._setup["horizontal_alignment"]](
                    0,
                    curses.COLS-1,
                    self._current_width )
        elif(parent_exists):
            self._spot_x = divs[self._setup["parent"]]._spot_x

        if( self._setup.get("vertical_alignment") is not None):
            if(parent_exists):
                self._spot_y = self._aligners[self._setup["vertical_alignment"]](
                    divs[self._setup["parent"]]._spot_y,
                    divs[self._setup["parent"]]._spot_y + divs[self._setup["parent"]]._current_height - 1,
                    self._current_height )
            else:
                self._spot_y = self._aligners[self._setup["vertical_alignment"]](
                    0,
                    curses.LINES-1,
                    self._current_height )
        elif(parent_exists):
            self._spot_y = divs[self._setup["parent"]]._spot_y

        if( self._setup.get("anchors") is not None):

            if( self._setup.get("anchors").get("horizontal") is not None):
                anchor = self._setup["anchors"]["horizontal"]
                if(anchor["edge_of_target_div"] == AnchorEdges.LEFT):
                    self._spot_x = divs[anchor["latch_to_div"]]._spot_x - self._current_width
                elif(anchor["edge_of_target_div"] == AnchorEdges.RIGHT):
                    self._spot_x = divs[anchor["latch_to_div"]]._spot_x + divs[anchor["latch_to_div"]]._current_width

            if( self._setup.get("anchors").get("vertical") is not None):
                anchor = self._setup["anchors"]["vertical"]
                if(anchor["edge_of_target_div"] == AnchorEdges.TOP):
                    self._spot_y = divs[anchor["latch_to_div"]]._spot_y - self._current_height
                elif(anchor["edge_of_target_div"] == AnchorEdges.BOTTOM):
                    self._spot_y = divs[anchor["latch_to_div"]]._spot_y + divs[anchor["latch_to_div"]]._current_height

        if( self._setup.get("horizontal_margin") is not None):
            if( isinstance(self._setup["horizontal_margin"], int) ):
                self._current_horizontal_margin = self._setup["horizontal_margin"]
            elif( isinstance(self._setup["horizontal_margin"], float) ):
                self._current_horizontal_margin = self._relative_size( self._setup["horizontal_margin"], parent_width)
            else:
                err_msg = "Error: Div horizontal_margin may only be of type int or float."
                raise ValueError(err_msg)

        if( self._setup.get("vertical_margin") is not None):
            if( isinstance(self._setup["vertical_margin"], int) ):
                self._current_vertical_margin = self._setup["vertical_margin"]
            elif( isinstance(self._setup["vertical_margin"], float) ):
                self._current_vertical_margin = self._relative_size( self._setup["vertical_margin"], parent_height)
            else:
                err_msg = "Error: Div vertical_margin may only be of type int or float."
                raise ValueError(err_msg)

        self._spot_x += self._current_horizontal_margin
        self._spot_y += self._current_vertical_margin

        attributes = 0
        if( self._setup.get("attributes") is not None):
            for a in self._setup["attributes"]:
                attributes = attributes | a.value

        for l in range(self._current_width):
            row += " "
        for h in range(self._current_height):
            if( (0 <= self._spot_y+h < curses.LINES) and (0 <= self._spot_x < curses.COLS) ):
                scr.addstr( self._spot_y+h, self._spot_x, row, color_pair | attributes )

        return color_pair | attributes

class Label(Div):

    def __init__(self, setup):
        Div.__init__(self, setup)

        self._current_inner_horizontal_margin = 0
        self._current_inner_vertical_margin = 0

    def visual_update(self, scr, divs, color_handler):
        color_pair_and_attributes = Div.visual_update(self, scr, divs, color_handler)

        rows = self._setup["inner"]["value"].split("\n")
        max_row_width = 0
        for r in rows:
            if len(r) > max_row_width:
                max_row_width = len(r)

        text_spot_x = self._spot_x
        text_spot_y = self._spot_y

        if( self._setup.get("inner").get("horizontal_alignment") is not None):
            text_spot_x = self._aligners[self._setup["inner"]["horizontal_alignment"]](
                self._spot_x,
                self._spot_x + self._current_width - 1,
                max_row_width )

        if( self._setup.get("inner").get("vertical_alignment") is not None):
            text_spot_y = self._aligners[self._setup["inner"]["vertical_alignment"]](
                self._spot_y,
                self._spot_y + self._current_height - 1,
                len(rows) )

        if( self._setup.get("inner").get("horizontal_margin") is not None):
            if( isinstance(self._setup["inner"]["horizontal_margin"], int) ):
                self._current_inner_horizontal_margin = self._setup["inner"]["horizontal_margin"]
            elif( isinstance(self._setup["inner"]["horizontal_margin"], float) ):
                self._current_inner_horizontal_margin = self._relative_size( self._setup["inner"]["horizontal_margin"], self._current_width)
            else:
                err_msg = "Error: Inner horizontal_margin may only be of type int or float."
                raise ValueError(err_msg)

        if( self._setup.get("inner").get("vertical_margin") is not None):
            if( isinstance(self._setup["inner"]["vertical_margin"], int) ):
                self._current_inner_vertical_margin = self._setup["inner"]["vertical_margin"]
            elif( isinstance(self._setup["inner"]["vertical_margin"], float) ):
                self._current_inner_vertical_margin = self._relative_size( self._setup["inner"]["vertical_margin"], self._current_height)
            else:
                err_msg = "Error: Inner vertical_margin may only be of type int or float."
                raise ValueError(err_msg)

        text_spot_x += self._current_inner_horizontal_margin
        text_spot_y += self._current_inner_vertical_margin

        for r in range( len(rows) ):
            centered_text_spot_x = self._aligners[Alignment.CENTER](
                text_spot_x,
                text_spot_x + max_row_width - 1,
                len(rows[r]) )
            if( (0 <= text_spot_y+r < curses.LINES) and (0 <= centered_text_spot_x < curses.COLS) ):
                scr.addstr( text_spot_y+r, centered_text_spot_x, rows[r], color_pair_and_attributes )

class Button(Label):

    def __init__(self, setup):
        Label.__init__(self, setup)

    def visual_update(self, scr, divs, color_handler):
        Label.visual_update(self, scr, divs, color_handler)

    def handle_input(self, key, hex_master):
        if( key == self._setup["key_map"]["interact"] ):
            self._setup["on_interact"](self, hex_master)

class TextArea(Div):

    def __init__(self, setup):
        Div.__init__(self, setup)
        self.__cursor_index = 0
        self.__cursor_above = 0
        self.__cursor_below = 0
        self.__cursor_row_start = 0
        self.__cursor_row_end = 0
        self.__inner_width = 0
        self.__inner_height = 0

        self._current_inner_horizontal_margin = 0
        self._current_inner_vertical_margin = 0

    def visual_update(self, scr, divs, color_handler):
        color_pair_and_attributes = Div.visual_update(self, scr, divs, color_handler)

        rows = []
        row = ""
        row_counter = 0
        col_counter = 0

        cursor_row = 0
        cursor_col = 0
        if( -1 == self.__cursor_index ):
            cursor_row = 0
            cursor_col = -1

        if( isinstance(self._setup["inner"]["width"], int) ):
            self.__inner_width = self._setup["inner"]["width"]
        elif( isinstance(self._setup["inner"]["width"], float) ):
            self.__inner_width = self._relative_size( self._setup["inner"]["width"], self._current_width)
        else:
            err_msg = "Error: Inner width may only be of type int or float."
            raise ValueError(err_msg)

        if( isinstance(self._setup["inner"]["height"], int) ):
            self.__inner_height = self._setup["inner"]["height"]
        elif( isinstance(self._setup["inner"]["height"], float) ):
            self.__inner_height = self._relative_size( self._setup["inner"]["height"], self._current_height)
        else:
            err_msg = "Error: Inner height may only be of type int or float."
            raise ValueError(err_msg)

        for c in range( len(self._setup["inner"]["value"]) ):
            if( c == self.__cursor_index ):
                if( self._setup["inner"]["value"][c] == "\n" ):
                    cursor_row = len(rows)+1
                    cursor_col = -1
                elif( col_counter == (self.__inner_width)-1 ):
                    cursor_row = len(rows)+1
                    cursor_col = -1
                elif( col_counter > (self.__inner_width)-1 ):
                    cursor_row = len(rows)+1
                    cursor_col = 0
                else:
                    cursor_row = len(rows)
                    cursor_col = col_counter
            if( self._setup["inner"]["value"][c] == "\n" ):
                rows.append(row)
                row = ""
                col_counter = 0
                continue
            elif( col_counter >= (self.__inner_width) ):
                rows.append(row)
                row = ""
                col_counter = 0
            row += self._setup["inner"]["value"][c]
            col_counter += 1
            if c == len(self._setup["inner"]["value"])-1 :
                rows.append(row)

        self.__cursor_above = self.__cursor_index
        if(cursor_row > 0):
            if( len(rows[cursor_row-1]) == (self.__inner_width) ):
                self.__cursor_above -= (self.__inner_width)

            else:
                self.__cursor_above -= (cursor_col + 1)
                self.__cursor_above -= ( len( rows[cursor_row-1] ) + 1 )
                if( len( rows[cursor_row-1] ) > cursor_col ):
                    self.__cursor_above += (cursor_col+1)
                else:
                    self.__cursor_above += len( rows[cursor_row-1] )
        else:
            self.__cursor_above = -1

        self.__cursor_below = self.__cursor_index
        if cursor_row == len(rows)-1 :
            self.__cursor_below = len(self._setup["inner"]["value"]) - 1
        elif(cursor_row < len(rows)-1):

            if( len(rows[cursor_row]) == (self.__inner_width) ):
                self.__cursor_below += (self.__inner_width)

            else:
                self.__cursor_below = self.__cursor_index - cursor_col - 1
                self.__cursor_below += ( len( rows[cursor_row] ) + 1)
                if( len( rows[cursor_row+1] ) > cursor_col ):
                    self.__cursor_below += (cursor_col+1)
                else:
                    self.__cursor_below += len( rows[cursor_row+1] )
        elif len(self._setup["inner"]["value"]) != 0 :
            if self._setup["inner"]["value"][ len(self._setup["inner"]["value"])-1 ] == "\n" :
                self.__cursor_below = len(self._setup["inner"]["value"])-1 

        self.__cursor_row_start = self.__cursor_index
        self.__cursor_row_end = self.__cursor_index
        if( cursor_row < len(rows) ):
            if( len(rows[cursor_row]) > 1 ):
                self.__cursor_row_start -= (cursor_col+1)
                self.__cursor_row_end += (len(rows[cursor_row]) - cursor_col - 1)

        text_spot_x = self._spot_x
        text_spot_y = self._spot_y

        if( self._setup.get("inner").get("horizontal_alignment") is not None):
            text_spot_x = self._aligners[self._setup["inner"]["horizontal_alignment"]](
                self._spot_x,
                self._spot_x + self._current_width - 1,
                self.__inner_width )

        if( self._setup.get("inner").get("vertical_alignment") is not None):
            text_spot_y = self._aligners[self._setup["inner"]["vertical_alignment"]](
                self._spot_y,
                self._spot_y + self._current_height - 1,
                self.__inner_height )

        if( self._setup.get("inner").get("horizontal_margin") is not None):
            if( isinstance(self._setup["inner"]["horizontal_margin"], int) ):
                self._current_inner_horizontal_margin = self._setup["inner"]["horizontal_margin"]
            elif( isinstance(self._setup["inner"]["horizontal_margin"], float) ):
                self._current_inner_horizontal_margin = self._relative_size( self._setup["inner"]["horizontal_margin"], self._current_width)
            else:
                err_msg = "Error: Inner horizontal_margin may only be of type int or float."
                raise ValueError(err_msg)

        if( self._setup.get("inner").get("vertical_margin") is not None):
            if( isinstance(self._setup["inner"]["vertical_margin"], int) ):
                self._current_inner_vertical_margin = self._setup["inner"]["vertical_margin"]
            elif( isinstance(self._setup["inner"]["vertical_margin"], float) ):
                self._current_inner_vertical_margin = self._relative_size( self._setup["inner"]["vertical_margin"], self._current_height)
            else:
                err_msg = "Error: Inner vertical_margin may only be of type int or float."
                raise ValueError(err_msg)

        text_spot_x += self._current_inner_horizontal_margin
        text_spot_y += self._current_inner_vertical_margin

        starting_row = 0
        if( len(rows) >= self.__inner_height ):
            starting_row = cursor_row - self.__inner_height + 1
            if starting_row < 0 :
                starting_row = 0
        printed_rows = 0

        for r in range(starting_row, numpy.clip( starting_row+self.__inner_height, 0, len(rows) ) ):
            if( (0 <= text_spot_y+printed_rows < curses.LINES) and (0 <= text_spot_x < curses.COLS) ):
                scr.addstr( text_spot_y+printed_rows, text_spot_x, rows[r], color_pair_and_attributes )
            if( self.status == DivStatus.ACTIVE ):
                if( r == cursor_row ):
                    scr.move(text_spot_y+printed_rows, text_spot_x+cursor_col+1)
                    char_at_cursor = chr(scr.inch()&255)
                    if( (0 <= text_spot_y+printed_rows < curses.LINES) and (0 <= text_spot_x+cursor_col+1 < curses.COLS) ):
                        scr.addstr( text_spot_y+printed_rows, text_spot_x+cursor_col+1, char_at_cursor, color_pair_and_attributes
                            | curses.A_REVERSE | curses.A_BLINK )
            printed_rows += 1

        if( self.status == DivStatus.ACTIVE ):
            if( cursor_row == len(rows) ):
                scr.move(text_spot_y+ numpy.clip(len(rows), 0, self.__inner_height-1) , text_spot_x)
                char_at_cursor = chr(scr.inch()&255)
                if( (0 <= (text_spot_y + numpy.clip(len(rows), 0, self.__inner_height-1)) < curses.LINES) and (0 <= text_spot_x < curses.COLS) ):
                    scr.addstr( text_spot_y + numpy.clip(len(rows), 0, self.__inner_height-1), text_spot_x, char_at_cursor, color_pair_and_attributes
                        | curses.A_REVERSE | curses.A_BLINK )

    def handle_input(self, key, hex_master):
        if(self.status == DivStatus.FOCUSED):
            if( key == self._setup["key_map"]["activate"] ):
                self.status = DivStatus.ACTIVE
        elif(self.status == DivStatus.ACTIVE):
            if( key == self._setup["key_map"]["deactivate"] ):
                self.status = DivStatus.FOCUSED
            elif( key == self._setup["key_map"]["active"]["left"] ):
                self.__cursor_index = numpy.clip(self.__cursor_index-1, -1, len(self._setup["inner"]["value"])-1)
            elif( key == self._setup["key_map"]["active"]["right"] ):
                self.__cursor_index = numpy.clip(self.__cursor_index+1, -1, len(self._setup["inner"]["value"])-1)
            elif( (key == self._setup["key_map"]["active"]["up"]) or (key == self._setup["key_map"]["active"]["page_up"]) ):
                self.__cursor_index = self.__cursor_above
            elif( (key == self._setup["key_map"]["active"]["down"]) or (key == self._setup["key_map"]["active"]["page_down"]) ):
                self.__cursor_index = self.__cursor_below
            elif( key == self._setup["key_map"]["active"]["backspace"] ):
                if( self.__cursor_index == -1 ):
                    return
                self._setup["inner"]["value"] = \
                    self._setup["inner"]["value"][:self.__cursor_index] + self._setup["inner"]["value"][self.__cursor_index + 1 :]
                self.__cursor_index = numpy.clip(self.__cursor_index-1, -1, len(self._setup["inner"]["value"])-1)
            elif( key == self._setup["key_map"]["active"]["delete"] ):
                if( self.__cursor_index == len(self._setup["inner"]["value"]) ):
                    return
                self._setup["inner"]["value"] = \
                    self._setup["inner"]["value"][:self.__cursor_index+1] + self._setup["inner"]["value"][self.__cursor_index + 2 :]
            elif( key == self._setup["key_map"]["active"]["home"] ):
                self.__cursor_index = self.__cursor_row_start
            elif( key == self._setup["key_map"]["active"]["end"] ):
                self.__cursor_index = self.__cursor_row_end
            else:
                if( isinstance(key, int) ):
                    if( (key >= Key.F1.value) and (key <= Key.F12.value) ):
                        return
                    if( key == Key.INSERT.value ):
                        return

                elif( key == Key.TAB.value ):
                    key = " "

                input_char = (str(key))
                if( self.__cursor_index == -1 ):
                    self._setup["inner"]["value"] = input_char + self._setup["inner"]["value"]
                else:
                    self._setup["inner"]["value"] = \
                        self._setup["inner"]["value"][:self.__cursor_index + 1] + input_char + self._setup["inner"]["value"][self.__cursor_index +1 :]
                self.__cursor_index = numpy.clip(self.__cursor_index+1, -1, len(self._setup["inner"]["value"])-1)


