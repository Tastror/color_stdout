__init_dict = globals().copy()

reset, bold, faint, italic, underline, blink, fast_blink = tuple(i for i in range(0, 6 + 1))
dark_black, dark_red, dark_green, dark_yellow, dark_blue, dark_purple, dark_cyan, dark_white = \
    tuple(i for i in range(30, 37 + 1))
bg_dark_black, bg_dark_red, bg_dark_green, bg_dark_yellow, bg_dark_blue, bg_dark_purple, bg_dark_cyan, bg_dark_white = \
    tuple(i for i in range(40, 47 + 1))
black, red, green, yellow, blue, purple, cyan, white = \
    tuple(i for i in range(90, 97 + 1))
bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_purple, bg_cyan, bg_white = \
    tuple(i for i in range(100, 107 + 1))

gray = dark_black
end = reset

__now_dict = globals().copy()
color_dict = {k: v for k, v in __now_dict.items() if k not in __init_dict and isinstance(v, int)}
