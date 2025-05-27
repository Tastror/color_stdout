import sys
from .color import color_dict

# ANSI escape code
# ECMA-48
# Linux: man console_codes

# \033: ESC
# \033[: CSI (Control Sequence Introducer)

# not used:
# CSI E (Next Line), CSI F (Previous Line), CSI S (Next Page), CSI T (Previous Page)

def crcode(
    color: str | int | list | tuple, code_only: bool = False
) -> str:

    # \033[xm: change to x color (0 reset, 1 bold, 4 underline, 30~37 90~97 colors)
    # \033[a;b;cm: equal to \033[am\033[bm\033[cm
    # faint, italic, blink, fast_blink is not supported in most terminals

    if type(color) == int:
        color_list = [color]
    elif type(color) == str:
        color_list = color.lower().split(',')
        color_list = [i.strip() for i in color_list]
    elif type(color) == list or type(color) == tuple:
        color_list = color
        color_list = [i.strip() if type(i) == str else i for i in color_list]
    else:
        raise TypeError(f"Unsupported color type: {type(color)}")

    color_list = [i for i in color_list if i != ""]
    if len(color_list) == 0:
        return ""

    result_code_start = "\033["
    result_code_end = "m"
    result_code = ""
    for i in color_list:
        if type(i) == str:
            if i in color_dict:
                result_code += str(color_dict[i]) + ";"
            elif i.isdigit():  # TODO: is this necessary?
                result_code += i + ";"
            else:
                if "," in i:
                    i_list = i.lower().split(',')
                    result_code += crcode(i_list, code_only=True) + ";"
                else:
                    raise ValueError(f"Unsupported color name: {i}")
        elif type(i) == int:
            result_code += str(i) + ";"
        else:
            result_code += crcode(i, code_only=True) + ";"

    if result_code[-1] == ";":
        result_code = result_code[:-1]
    if code_only:
        return result_code
    return result_code_start + result_code + result_code_end

def crformat(
    text: object,
    color: str | int | list | tuple | None = None,
    *,
    end_reset: bool = True  # only works when color is not None
) -> str:
    """
    param:
        end_reset: only works when color is not None
    """
    if color is None:
        return f"{text}"
    elif end_reset:
        return f"{crcode(color)}{text}{crcode('reset')}"
    else:
        return f"{crcode(color)}{text}"

def crprint(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    color: str | int | list | tuple | None = None,
    end_reset: bool = True,  # only works when color is not None
    # file: SupportsWrite[str] | None = None,  # important, always sys.stdout
    flush: bool = False
) -> None:
    """
    param:
        end_reset: only works when color is not None
    """
    if color is None:
        print(*values, sep=sep, end=end)
    else:
        sys.stdout.write(f"{crcode(color)}")
        print(*values, sep=sep, end=end)
        if end_reset:
            sys.stdout.write(f"{crcode('reset')}")
    if flush:
        sys.stdout.flush()

def crinput(
    *prompts: object,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | int | list | tuple | None = None,
    input_color: str | int | list | tuple | None = None,
    end_reset: bool = True,  # only works when input_color is not None
    # file: SupportsWrite[str] | None = None,  # important, always sys.stdout
    flush: bool = False
) -> str:
    """
    param:
        end: default is "", not "\\n"
        end_reset: only works when color is not None
    """
    crprint(*prompts, sep=sep, end=end, color=color, end_reset=True, flush=flush)
    if input_color is None:
        data = input()
    else:
        sys.stdout.write(f"{crcode(input_color)}")
        data = input()
        if end_reset:
            sys.stdout.write(f"{crcode('reset')}")
    if flush:
        sys.stdout.flush()
    return data



def clean_current(*, flush: bool = True):
    # \033[nJ: clear screen
    # n = 0: clear from cursor to end
    # n = 1: clear from cursor to start
    # n = 2: clear all (hide in back-scroll)
    # n = 3: clear all (incluing back-scroll data), or just clean back-scroll data
    sys.stdout.write("\033[2J")
    if flush:
        sys.stdout.flush()

def clean_totally(*, flush: bool = True):
    sys.stdout.write("\033[3J")
    sys.stdout.write("\033[2J")
    if flush:
        sys.stdout.flush()

def clean_line(*, flush: bool = True):
    # \033[nK: clear line
    # n = 0: clear from cursor to end
    # n = 1: clear from cursor to start
    # n = 2: clear all
    sys.stdout.write("\033[2K")
    if flush:
        sys.stdout.flush()

def cursor_home(*, flush: bool = True):
    # \033[x;yf or \033[x;yH (safer): move to x, y
    # missing x or y: set to 1 (move to start)
    sys.stdout.write("\033[H")
    if flush:
        sys.stdout.flush()

def cursor_row_home(*, flush: bool = True):
    # \033[nG: move to n column
    # missing n: set to 1 (move to start)
    sys.stdout.write("\033[G")
    if flush:
        sys.stdout.flush()

def clean_current_and_to_start(*, flush: bool = True):
    clean_current(flush=False)
    cursor_home(flush=flush)

def clean_totally_and_to_start(*, flush: bool = True):
    clean_totally(flush=False)
    cursor_home(flush=flush)

def clean_line_and_to_start(*, flush: bool = True):
    clean_line(flush=False)
    cursor_row_home(flush=flush)

clean = clean_totally
clean_and_to_start = clean_totally_and_to_start



def store_cursor(*, flush: bool = True):
    # \0337 or \033[s: save cursor position
    sys.stdout.write("\033[s")
    if flush:
        sys.stdout.flush()

def restore_cursor(*, flush: bool = True):
    # \0338 or \033[u: restore cursor position
    sys.stdout.write("\033[u")
    if flush:
        sys.stdout.flush()

def cursor(line: int | None = None, column: int | None = None, *, flush: bool = True):
    # \033[l;cf or \033[l;cH: move to line l, column c
    # \033[cG: only move to column c, line not changed
    # \033[ld: only move to line l, column not changed
    if line is None and column is None:
        pass
    elif line is not None and column is None:
        sys.stdout.write(f"\033[{line}d")
    elif line is None and column is not None:
        sys.stdout.write(f"\033[{column}G")
    else:
        sys.stdout.write(f"\033[{line};{column}H")
    if flush:
        sys.stdout.flush()

def cursor_up(n: int, *, flush: bool = True):
    # \033[nA: move up n chars
    sys.stdout.write(f"\033[{n}A")
    if flush:
        sys.stdout.flush()

def cursor_down(n: int, *, flush: bool = True):
    # \033[nB: move down n chars
    sys.stdout.write(f"\033[{n}B")
    if flush:
        sys.stdout.flush()

def cursor_right(n: int, *, flush: bool = True):
    # \033[nC: move right n chars
    sys.stdout.write(f"\033[{n}C")
    if flush:
        sys.stdout.flush()

def cursor_left(n: int, *, flush: bool = True):
    # \033[nD: move left n chars
    sys.stdout.write(f"\033[{n}D")
    if flush:
        sys.stdout.flush()



def crprint_there(
    *value: object,
    line: int | None = None,
    column: int | None = None,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | int | list | tuple | None = None,
    end_reset: bool = True,
    flush: bool = True
):
    """
    param:
        end: default is "", not "\\n"
        end_reset: only works when color is not None
    """
    cursor(line, column, flush=False)
    crprint(*value, sep=sep, end=end, color=color, end_reset=end_reset, flush=flush)

def crprint_still(
    *value: object,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | int | list | tuple | None = None,
    end_reset: bool = True,
    flush: bool = True
):
    """
    param:
        end: default is "", not "\\n"
        end_reset: only works when color is not None
    """
    store_cursor(flush=False)
    crprint(*value, sep=sep, end=end, color=color, end_reset=end_reset)
    restore_cursor(flush=flush)

def crprint_thisline(
    *value: object,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | int | list | tuple | None = None,
    end_reset: bool = True,
    flush: bool = True
):
    """
    param:
        end: default is "", not "\\n"
        end_reset: only works when color is not None
    """
    clean_line_and_to_start(flush=False)
    crprint(*value, sep=sep, end=end, color=color, end_reset=end_reset, flush=flush)

def color_reset(*, flush: bool = True):
    crprint(color="reset", end_reset=False, end="", flush=flush)
