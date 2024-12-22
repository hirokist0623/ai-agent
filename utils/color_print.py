from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def _colored_print(color, *args, **kwargs):
    """
    Generic function for colored printing.

    Args:
        color: Fore color to use.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    print(color + " ".join(map(str, args)), **kwargs)
    print(Style.RESET_ALL, end="")


def _colored_input(color, prompt):
    """
    Generic function for colored input.

    Args:
        color: Fore color to use.
        prompt: Input prompt.
    """
    print(color + prompt + Style.RESET_ALL, end="")
    return input()


def gprint(*args, **kwargs):
    """
    Print text in green color.
    """
    _colored_print(Fore.GREEN, *args, **kwargs)


def cprint(*args, **kwargs):
    """
    Print text in cyan color.
    """
    _colored_print(Fore.CYAN, *args, **kwargs)


def iinput(prompt):
    """
    Input with indigo prompt (#6970FF).
    """
    return _colored_input("\033[38;2;105;112;255m", prompt)


# Test the color printing and input
if __name__ == "__main__":
    gprint("This should be green")
    cprint("This should be cyan")
    print("This should be the default color")

    iinput("Indigo input: ")
