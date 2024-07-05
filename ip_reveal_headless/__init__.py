import socket
import sys
from platform import node
from socket import gaierror
from urllib.error import URLError

from requests import get
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError

from ip_reveal_headless.config import PARSED_ARGS, CONFIG, CMD_ALIASES
from ip_reveal_headless.log_engine import PROG_LOGGER
from ip_reveal_headless.tools import commify, is_repl
from ip_reveal_headless.version import VERSION
from rich import print as rprint

LOG_DEVICE = PROG_LOGGER.get_child('ip_reveal_headless.ip_reveal')


cached_ext_ip = None
ip_hist = []

inet_down = False
log_device = None
args = PARSED_ARGS

config = CONFIG


def get_hostname():
    """
    get_hostname

    Fetch the system's apparent hostname and return it to the caller

    Returns:
        str: The system's apparent hostname contained within a string.
    """

    # Prepare the logger
    _log = LOG_DEVICE.get_child(f'{log_name}.get_hostname')
    _debug = _log.debug

    # Fetch the hostname from platform.node
    hostname = node()
    _debug(f'Checked hostname and found it is: {hostname}')

    # Return this to the caller
    return hostname


def get_external():
    """
    get_external

    Fetch the system's apparent hostname and return it to the caller in the form of a string.

    Returns:
        str: The system's apparent external IP-Address in the form of a string.
    """
    global cached_ext_ip, inet_down, ip_hist

    # Prepare the logger
    _log = LOG_DEVICE.add_child(log_name + '.get_external')
    _debug = _log.debug

    # Try contacting IPIFY.org with a basic request and read the returned text.
    #
    # If we are unable to connect to this outside service, it's likely that Internet connection has dropped. There
    # are - however, instances where this service is down, and for these reasons we want to have at least one
    # alternative to control for failure on a Singular -free- AI API.

    # Fetch the external IP-Address from IPIFY.org
    try:
        external = get('https://api.ipify.org').text
        _debug(f'Checked external IP and found it is: {external}')

    # Catch the "ConnectionError" exception that is raised when the "requests" package is unable to reach
    # "IPIFY.org", simply reporting this occurred (if the logger is listening) before (maybe first; attempt connection
    # to another service?)
    except (ConnectionError, MaxRetryError, gaierror, URLError):
        if not inet_down:
            _log.warning("Unable to establish an internet connection.")
            inet_down = True
        external = None

    if external is None:
        return False

    if not cached_ext_ip:
        cached_ext_ip = external
        if cached_ext_ip != external:
            cached_ext_ip = external
    return external


def get_internal():
    """
    get_internal

    Fetch the system's local IP-Address and return it to the caller in the form of a string.

    Returns:
        str: The system's local IP-Address contained within a string.
    """

    # Set up a logger
    _log = LOG_DEVICE.add_child(log_name + '.get_internal')

    # Alias the debug entry call
    _debug = _log.debug

    # Start a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Attempt a connection to an arbitrary host
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))

        # Fetch our IP from this socket's metadata
        IP = s.getsockname()[0]

    # Should we raise an exception we won't bother handling it, we'll just return the loopback address to the caller.
    except Exception:
        IP = '127.0.0.1'

    # No matter the result, let's remember to close the socket.
    finally:
        s.close()

    # Announce that we've found an IP
    _debug(f'Checked internal IP and found: {IP}')

    # Return a string containing the result to the caller.
    return IP


# Set up a name for our log_engine device
log_name = "IPReveal"


# Set up two variables that will act as caches for the external and internal IPs
# cached_ext_ip = None
# cached_int_ip = None


def main():
    """

    This is the main function to run the IP-Reveal program

    Returns:
        None

    """
    global log_device, args

    log = LOG_DEVICE.add_child(f'{log_name}.Main')
    # Alias the log.debug signature for ease-of-use
    debug = log.debug

    debug(f'Received arguments: {args}')
    if args.subcommands:
        debug(f'Running subcommand: {args.subcommands}')

    tbr = None

    if args.subcommands in CMD_ALIASES.print_version_info:
        VERSION.print_version_info(check_for_update=PARSED_ARGS.update)

    # See if we got one of the subcommands assigned.
    elif args.subcommands in CMD_ALIASES.get_public:
        tbr = get_external()

    elif args.subcommands in CMD_ALIASES.get_host:
        tbr = get_hostname()

    elif args.subcommands in CMD_ALIASES.get_local:
        tbr = get_internal()

    elif args.subcommands in CMD_ALIASES.get_all:
        tbr = f"{get_hostname()}@({get_internal()}|{get_external()})"

    else:
        print('No valid subcommand was given, exiting...')

    if tbr:
        debug(f'Returning: {tbr}')
        if args.use_rich:
            debug('Using rich to print result...')
            rprint(tbr)
        else:
            debug('Using print to print result...')
            print(tbr)

    if not is_repl():
        debug('Not in REPL, exiting...')
        sys.exit()

    debug('Entering interactive mode...')

    LOG_DEVICE.info('Interactive session detected, entering interactive mode...')


if __name__ == '__main__':
    main()
