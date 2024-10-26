import sys

usual_print = print
usual_input = input

# ANSI escape code
# ECMA-48
# Linux: man console_codes

# \033: ESC
# \033[: CSI (Control Sequence Introducer)

# not used:
# CSI E (Next Line), CSI F (Previous Line), CSI S (Next Page), CSI T (Previous Page)


def color_to_code(color: str) -> str:
    # \033[xm: change to x color (0 reset, 1 bold, 4 underline, 30~37 90~97 colors)
    # \033[a;b;cm: equal to \033[am\033[bm\033[cm
    reset, bold, _, _, underline = tuple(f"\033[{i}m" for i in range(0, 4 + 1))
    dark_black, dark_red, dark_green, dark_yellow, dark_blue, dark_purple, dark_cyan, dark_white = tuple(f"\033[{i}m" for i in range(30, 37 + 1))
    black, red, green, yellow, blue, purple, cyan, white = tuple(f"\033[{i}m" for i in range(90, 97 + 1))
    del _
    for name, code in locals().items():
        if name == color:
            return code

def format_color(
    text: object,
    color: str | None = None,
    *,
    end_reset: bool = True
) -> str:
    if color is None:
        return f"{text}"
    elif end_reset:
        return f"{color_to_code(color)}{text}{color_to_code('reset')}"
    else:
        return f"{color_to_code(color)}{text}"

def print(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    color: str | None = None,
    end_reset: bool = True,  # only works when color is not None
    # file: SupportsWrite[str] | None = None,  # important, always sys.stdout
    flush: bool = True  # important, different from usual print
) -> None:
    if color is None:
        usual_print(*values, sep=sep, end=end)
    else:
        sys.stdout.write(f"{color_to_code(color)}")
        usual_print(*values, sep=sep, end=end)
        if end_reset:
            sys.stdout.write(f"{color_to_code('reset')}")
    if flush:
        sys.stdout.flush()

def input(
    *prompts: object,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | None = None,
    input_color: str | None = None,
    end_reset: bool = True,  # only works when input_color is not None
    # file: SupportsWrite[str] | None = None,  # important, always sys.stdout
    flush: bool = True  # important
) -> str:
    print(*prompts, sep=sep, end=end, color=color, end_reset=True, flush=flush)
    if input_color is None:
        data = usual_input()
    else:
        sys.stdout.write(f"{color_to_code(input_color)}")
        data = usual_input()
        if end_reset:
            sys.stdout.write(f"{color_to_code('reset')}")
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

def cursor_to_start(*, flush: bool = True):
    # \033[x;yf or \033[x;yH (safer): move to x, y
    # missing x or y: set to 1 (move to start)
    sys.stdout.write("\033[H")
    if flush:
        sys.stdout.flush()

def cursor_to_line_start(*, flush: bool = True):
    # \033[nG: move to n column
    # missing n: set to 1 (move to start)
    sys.stdout.write("\033[G")
    if flush:
        sys.stdout.flush()

def clean_current_and_to_start(*, flush: bool = True):
    clean_current(flush=False)
    cursor_to_start(flush=flush)

def clean_totally_and_to_start(*, flush: bool = True):
    clean_totally(flush=False)
    cursor_to_start(flush=flush)

def clean_line_and_to_start(*, flush: bool = True):
    clean_line(flush=False)
    cursor_to_line_start(flush=flush)

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

def move(line: int | None = None, column: int | None = None, *, flush: bool = True):
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

def move_up(n: int, *, flush: bool = True):
    # \033[nA: move up n chars
    sys.stdout.write(f"\033[{n}A")
    if flush:
        sys.stdout.flush()

def move_down(n: int, *, flush: bool = True):
    # \033[nB: move down n chars
    sys.stdout.write(f"\033[{n}B")
    if flush:
        sys.stdout.flush()

def move_right(n: int, *, flush: bool = True):
    # \033[nC: move right n chars
    sys.stdout.write(f"\033[{n}C")
    if flush:
        sys.stdout.flush()

def move_left(n: int, *, flush: bool = True):
    # \033[nD: move left n chars
    sys.stdout.write(f"\033[{n}D")
    if flush:
        sys.stdout.flush()



def print_there(
    *value: object,
    line: int | None = None,
    column: int | None = None,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | None = None,
    end_reset: bool = True,
    flush: bool = True
):
    move(line, column, flush=False)
    print(*value, sep=sep, end=end, color=color, end_reset=end_reset, flush=flush)

def print_still(
    *value: object,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | None = None,
    end_reset: bool = True,
    flush: bool = True
):
    store_cursor(flush=False)
    print(*value, sep=sep, end=end, color=color, end_reset=end_reset, flush=False)
    restore_cursor(flush=flush)

def print_thisline(
    *value: object,
    sep: str | None = " ",
    end: str | None = "",  # important
    color: str | None = None,
    end_reset: bool = True,
    flush: bool = True
):
    clean_line_and_to_start(flush=False)
    print(*value, sep=sep, end=end, color=color, end_reset=end_reset, flush=flush)



if __name__ == "__main__":

    # test

    clean_and_to_start()

    move(2, 1)
    print(11111111)
    print(22222222)
    print(33333333)
    print(44444444)
    print(55555555)
    print_there(66666666, line=1, column=9)
    print_there(77777777, line=4)
    print_there(88888888, line=7, column=1)
    print_there(99999999, column=10)
    print_there("00000000")

    move_down(2)
    move_left(1000)
    input("normal", "color:", sep=" ", end=" ")  # use print-like *value, sep and end
    input("red prompt: ", color="red")
    input("green input: ", input_color="green")
    input("red prompt, green input: ", color="red", input_color="green")

    import time
    move_right(10)
    for i in range(10):
        print_still(i, end="")
        time.sleep(0.2)
    print(12312321312123213, end="")
    time.sleep(0.2)
    print_thisline("thisline")    
