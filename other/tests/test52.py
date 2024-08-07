import time


import warnings


ansi = {
        # 'ansi' is a variable that contains all the commonly used ANSI formats.
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blinking': '\033[5m',
        'reverse': '\033[7m',
        'hidden': '\033[8m',
        'strikethrough': '\033[9m'
    }


def progress(idx: int, max_idx: int, *, desc: str = None, b_len: int = 50) -> None:
    r"""
    **Prints a progress bar.**

    Arguments:
    ----------
    - **idx** : (*int*)
        The current index.
    - **max_idx** : (*int*)
        The maximum index.
    - **desc** : (*str*), default=None
        The bar description.
    - **b_len** : (*int*), default=50:
        The bar length

    Returns:
    ----------
    None.

    Example:
    ----------
    >>> from gardenpy.utils.helper_functions import progress
    >>> for i in range(5000):
    >>>     progress(i, 5000)
    """
    # get ansi formats
    if not isinstance(b_len, int):
        # invalid datatype
        raise ValueError(f"'b_len' is not an integer: '{b_len}'")
    # completed progress
    completed = (idx + 1) / max_idx
    # make progress bar
    p_bar = (
        f"\r{ansi['green']}{'—' * int(b_len * completed)}"
        f"{ansi['red']}{'—' * (b_len - int(b_len * completed))}{ansi['reset']}"
    )
    if desc is None:
        # print progress bar
        print(p_bar, end='')
    else:
        # set description
        p_desc = f"{desc}"
        # print description
        print(f"{p_bar}  {p_desc}", end='')


def convert_time(seconds: float, *, number_colors: str = None, separators_color: str = None) -> str:
    r"""
    **Converts seconds to hours:minutes:seconds.**

    Arguments:
    ----------
    - **seconds** : (*float*)
        The elapsed seconds.
    - **number_colors** : (*str*), default=None
        The number colors.
    - **seperator_colors** : (*str*), default=None
        The time separator colors.

    Returns:
    ----------
    - **time** : (*str*)
        The converted time.

    Example:
    ----------
    >>> import time
    >>> from gardenpy.utils.helper_functions import convert_time
    >>> start_time = time.time()
    >>> time.sleep(0.5)
    >>> convert_time(time.time() - start_time)
    """
    # get ansi formats
    if not number_colors:
        number_colors = ansi['reset']
    if not separators_color:
        separators_color = ansi['reset']
    # round seconds
    seconds = int(seconds)
    # find minutes and hours
    minutes = int(seconds / 60)
    hours = int(minutes / 60)
    # adjust times
    minutes -= hours * 60
    seconds -= minutes * 60
    # return time
    return f"{number_colors}{hours:01}{separators_color}:{number_colors}{minutes:02}{separators_color}:{number_colors}{seconds:02}{ansi['reset']}"


def print_contributors(*, who: list = None) -> None:
    r"""
    **Prints the contributors for GardenPy.**

    Parameters:
    ----------
    - **who** : (*list*) {'*authors*', '*contributors*'}
        What types of contributors to print.

    Returns:
    ----------
    None.

    Example:
    ----------
    >>> from gardenpy.utils.helper_functions import print_contributors
    >>> print_contributors()
    """
    # all contributors
    all_contributors = ['authors', 'artists']
    if who is None:
        # set default who
        who = all_contributors
    elif isinstance(who, list):
        # get who
        who = set(list(who))
        for con in who:
            if con not in all_contributors:
                warnings.warn(
                    f"\nInvalid parameter for 'who': '{con}'\n"
                    f"Choose from: '{[con for con in all_contributors]}'",
                    UserWarning
                )
    else:
        # invalid contributor specifications
        raise TypeError(
            f"'who' is not a list: '{who}'\n"
            f"Choose from: '{[con for con in all_contributors]}'"
        )

    printed = False
    if 'authors' in who:
        # print authors
        if printed:
            print()
        print(f"{ansi['bold']}{ansi['green']}GardenPy{ansi['reset']}")
        print(f"    {ansi['bold']}Authors{ansi['reset']}")
        print(f"    Christian SW Host-Madsen", end='')
        print(f"    {ansi['white']}Punahou School CO '25{ansi['reset']}", end='')
        print(f"    {ansi['bright_black']}<chost-madsen25@punahou.edu>{ansi['reset']}",)
        print(f"    Mason YY Morales", end='')
        print(f"            {ansi['white']}Punahou School CO '25{ansi['reset']}", end='')
        print(f"    {ansi['bright_black']}<mmorales25@punahou.edu>{ansi['reset']}")
        print(f"    Isaac P Verbrugge", end='')
        print(f"           {ansi['white']}Punahou School CO '25{ansi['reset']}", end='')
        print(f"    {ansi['bright_black']}<isaacverbrugge@gmail.com>{ansi['reset']}")
        print(f"    Derek S Yee", end='')
        print(f"                 {ansi['white']}Punahou School CO '25{ansi['reset']}", end='')
        print(f"    {ansi['bright_black']}<dyee25@punahou.edu>{ansi['reset']}")
        printed = True
    if 'artists' in who:
        # print artists
        if printed:
            print()
        print(f"    {ansi['bold']}Artists{ansi['reset']}")
        print(f"    Kamalau Kimata", end='')
        print(f"              {ansi['white']}Punahou School CO '25{ansi['reset']}", end='')
        print(f"    {ansi['bright_black']}<kkimata25@punahou.edu>{ansi['reset']}", )
        printed = True


status = True
max_iter = 10000

print()
print_contributors()
print()

time.sleep(1.0)

print("Test 1")
for i in range(int(max_iter / 10)):
    time.sleep(0.001)
    if status:
        progress(i, int(max_iter / 10))
print()

print("Test 2")
start = time.time()
for i in range(max_iter):
    time.sleep(0.001)
    if status:
        desc = (
            f"{str(i + 1).zfill(len(str(max_iter)))}{ansi['white']}it{ansi['reset']}/{max_iter}{ansi['white']}it{ansi['reset']}  "
            f"{(100 * (i + 1) / max_iter):05.1f}{ansi['white']}%{ansi['reset']}  "
            f"{convert_time(time.time() - start)}{ansi['white']}et{ansi['reset']}  "
            f"{convert_time((time.time() - start) * max_iter / (i + 1) - (time.time() - start))}{ansi['white']}eta{ansi['reset']}  "
            f"{round((i + 1) / (time.time() - start), 1)}{ansi['white']}it/s{ansi['reset']}"
        )
        progress(i, max_iter, desc=desc)
print("\n")
