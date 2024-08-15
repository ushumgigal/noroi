from noroi.core import DivTypes, DivStatus, ColorHandler, Div, Label, Button, TextArea, resize
import curses

class HexMaster:

    __default_input_timeout_ms = 250
    __default_esc_timeout_ms = 10

    def __init__(self, setup=None):
        self.__setup = {} if (setup == None) else setup
        self.__divs = {}
        self.__div_constructors = {}
        self.__div_constructors[DivTypes.DIV] = Div
        self.__div_constructors[DivTypes.LABEL] = Label
        self.__div_constructors[DivTypes.BUTTON] = Button
        self.__div_constructors[DivTypes.TEXT_AREA] = TextArea
        self.__loop = True
        self.__focused_div = None
        self.__color_handler = ColorHandler()


        if( not("input_timeout_ms" in self.__setup) ):
            self.__setup["input_timeout_ms"] = HexMaster.__default_input_timeout_ms
        if( not("esc_timeout_ms" in self.__setup) ):
            self.__setup["esc_timeout_ms"] = HexMaster.__default_esc_timeout_ms

    def resize(self, new_height, new_width):
        resize(self.__scr, new_height, new_width)

    def terminate(self):
        self.__loop = False

    def enable_div(self, div):
        self.__divs[div].status = DivStatus.IDLE

    def disable_div(self, div):
        self.__divs[div].status = DivStatus.DISABLED

    def div_status(self, div):
        return self.__divs[div].status

    def focus(self, div):
        if(self.__focused_div != None):
            self.__focused_div.status = DivStatus.IDLE
        self.__divs[div].status = DivStatus.FOCUSED
        self.__focused_div = self.__divs[div]

    def __update(self):
        self.__color_handler.reset()
        self.__scr.erase()

        for d in self.__divs:
            self.__divs[d].visual_update(self.__scr, self.__divs, self.__color_handler)

        self.__scr.refresh()

        try:
            key = self.__scr.get_wch()
        except curses.error as err:
            if(str(err) == "no input"):
                if(self.__setup.get("no_input_frame_update") is not None):
                    self.__setup["no_input_frame_update"]()
                return

        if(self.__focused_div != None):
            if(self.__focused_div.status == DivStatus.FOCUSED):
                for k in self.__focused_div._setup["key_map"]["switch_focus"]:
                    if( k.value == key ):
                        if( self.__divs[self.__focused_div._setup["key_map"]["switch_focus"][k]].status == DivStatus.IDLE ):
                            self.focus(self.__focused_div._setup["key_map"]["switch_focus"][k])
                            if(self.__setup.get("post_input_frame_update") is not None):
                                self.__setup["post_input_frame_update"]()
                            return

            self.__focused_div.handle_input(key, self)
            if(self.__setup.get("post_input_frame_update") is not None):
                self.__setup["post_input_frame_update"]()

    def __quit(self):
        curses.nocbreak()
        self.__scr.keypad(False)
        curses.echo()
        curses.endwin()

    def add_div(self, setup, focus=False, start_disabled=False):
        self.__divs[ setup["name"] ] = self.__div_constructors[ setup["type"] ](setup)
        if(focus):
            self.focus(setup["name"])
        elif(start_disabled):
            self.disable_div(setup["name"])

    def remove_div(self, div, recursive=True):
        gone = self.__divs.pop(div)

        if not recursive:
            return

        widows = []

        for d in self.__divs:
            if (self.__divs[d]._setup.get("parent") is not None) :
                if( self.__divs[d]._setup["parent"] == gone._setup["name"] ):
                    widows.append(self.__divs[d]._setup["name"])

        for w in widows:
            self.remove_div(w)

    def start(self, size=None):
        self.__scr = curses.initscr()
        self.__scr.timeout(self.__setup["input_timeout_ms"])
        curses.noecho()
        curses.set_escdelay(self.__setup["esc_timeout_ms"])
        curses.curs_set(0)
        curses.start_color()
        curses.cbreak()
        self.__scr.keypad(True)

        if(size != None):
            self.resize( size[0], size[1] )

        while(self.__loop):
            self.__update()
        self.__quit()
