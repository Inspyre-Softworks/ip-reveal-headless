
def commify(num):
    """

    Add commas in their necessary places to provided integer. Returns result as a string.

    Args:
        num (int): An integer you'd like returned with commas

    Returns:
        (str): The integer (as a string) that you provided with commas added.

    """
    num = int(num)
    res = "{:,}".format(num)

    return res


def is_repl():
    try:
        if __builtins__['__IPYTHON__']:
            return True
    except KeyError:
        return False
