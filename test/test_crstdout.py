from crstdout import *

if __name__ == "__main__":
    clean_and_to_start()

    cursor(2, 1)
    crprint(11111111, color="green")
    # str with "," will be split
    crprint(22222222, color="blue, bold, bg_white")
    # list or tuple is also supported, but no "," in str inner list / tuple
    crprint(33333333, color=("red, italic,", ("underline",), "bold", "blink"), end_reset=False)
    # thongh 44444444's end_reset == True, it won't work since no color specified
    crprint(44444444)
    # use this for reset, or color="reset" in next crprint
    color_reset()
    crprint(55555555)
    crprint_there(66666666, line=1, column=9, color="yellow, fast_blink")
    crprint_there(77777777, line=4)
    crprint_there(88888888, line=7, column=1)
    crprint_there(99999999, column=10)
    crprint_there("00000000")

    cursor_down(2)
    cursor_left(1000)
    # crinput can use crprint-like *value, sep and end for better use
    crinput(1, "normal", "color:", sep=" ", end=" ")
    crinput(2, "red prompt: ", color="red, italic")
    crinput(3, "green crinput: ", color="italic", input_color="green, underline")
    crinput(4, "red prompt, green crinput: ", color="red, italic", input_color="green, underline")

    import time
    cursor_right(10)
    for i in range(8):
        # use number (or list contains number) for color is also supported
        crprint_still(100000 + i, end="", color=i + 30)
        time.sleep(0.2)
    crprint(12312321312123213, end="", flush=True)
    time.sleep(0.2)
    crprint_thisline("clear this line")
    crprint()
    crprint(color.color_dict)
