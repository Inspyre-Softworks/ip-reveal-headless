from inspy_logger import InspyLogger, Loggable
from inspy_logger.constants import LEVEL_MAP


LOG_LEVELS = [level.upper() for level in LEVEL_MAP.keys()]


debug_mode = None


def in_debug_mode():
    from sys import argv
    global debug_mode
    cli_args = argv

    if debug_mode is None:
        found_match = None
        for arg in cli_args:
            if arg in ['-l', '--log-level']:
                next_spot = cli_args.index(arg) + 1
                if cli_args[next_spot].lower() == 'debug':
                    found_match = True

        debug_mode = bool(found_match)

    return debug_mode


in_debug_mode()


ANNOUNCEMENT_TEMPLATE = '{name} '


INIT_LOG_LEVEL = 'debug' if debug_mode else 'info'


PROG_LOGGER = InspyLogger('IPRevealHeadless', console_level=INIT_LOG_LEVEL)
