from argparse import ArgumentParser
from inspyre_toolbox.spanners.span_arg_parse import SubparserActionAliases
from ip_reveal_headless.log_engine import LOG_LEVELS


class ParsedArgs(object):
    """
    A class to handle argument parsing for the IP Reveal command-line tool.

    Attributes:
        aliases (Aliases): An instance of the :class:`Aliases` class containing sub-command aliases.
        parser (ArgumentParser): An argument parser for the command-line interface.
    """

    class Aliases(object):
        """
        A class to define aliases for the sub-commands in the IP Reveal tool.

        Attributes:
            get_public (list):
                Aliases for the 'get-public' command.

            get_host (list):
                Aliases for the 'get-host' command.

            get_local (list):
                Aliases for the 'get-local' command.

            get_all (list):
                Aliases for the 'get-all' command.

            print_version_info (list):
                Aliases for the 'print-version-info' command.
        """
        def __init__(self):
            self.get_public = [
                'get-external',
                'external',
                'public',
                'ip',
                'get-ip',
                'internet',
                'get-internet',
                'get-public'
            ]
            self.get_host = [
                'get-hostname',
                'hostname',
                'host',
                'name',
                'get-name',
                'get-host'
            ]
            self.get_local = [
                'local',
                'get-private',
                'private',
                'get-internal',
                'internal',
                'get-local'
            ]
            self.get_all = [
                'all',
                'reveal',
                'get-all'
            ]
            self.print_version_info = [
                'version-info',
                'version',
                'print-version-table',
                'print-version-info'
            ]

    VALID_LOG_LEVELS = LOG_LEVELS + [level.lower() for level in LOG_LEVELS]

    def __init__(self, prog, description, ver_obj):
        """
        Instantiate the argument parser.

        Parameters:
            prog (str):
                The name of the program.

            description (str):
                A description of the program.

            ver_obj (object):
                An object representing the version information.

        Properties:
            parser (ArgumentParser):
                A prepared :class:`argparse.ArgumentParser` object.
        """
        self.aliases = self.Aliases()

        self.parser = ArgumentParser(prog, description)

        self.parser.register('action', 'parsers', SubparserActionAliases)

        self.parser.add_argument(
            '-l', '--log-level',
            choices=self.VALID_LOG_LEVELS,
            default='info'
        )

        self.parser.add_argument('-V', '--version', action='version', version=str(ver_obj))

        self.parser.add_argument(
            '-C', '--config-filepath',
            action='store',
            type=str,
            help='The path of a currently existing config file or where you want a new one written to.',
            default='~/Inspyre-Softworks/IP-Reveal/config/config.ini'
        )

        self.parser.add_argument(
            '-S', '--silence-log-start',
            required=False,
            help='Do not let the logger print its initialization information.',
            action='store_true',
            default=False
        )

        self.parser.add_argument(
            '-r', '--use-rich',
            required=False,
            help='Use the Rich library for output formatting.',
            action='store_true',
            default=False
        )


def load_subcommands(parser, aliases):
    """
    Create sub-commands for the passed :class:`argparse.ArgumentParser` object along with their alias commands.

    Parameters:
        parser (ArgumentParser):
            An already instantiated :class:`argparse.ArgumentParser` object that you'd like to add subparsers to.

        aliases (ParsedArgs.Aliases):
            An instance of the :class:`ParsedArgs.Aliases` class containing sub-command aliases.

    Returns:
        ArgumentParser:
            The same object that was passed but with the following sub-commands:

            - get-public:
                Return the external IP to the command-line and nothing else.

                Aliases:
                    * [get-]external
                    * public
                    * [get-]ip

            - get-host:
                Return the hostname to the command-line and nothing else.

                Aliases:
                    * [get-]host
                    * [get-]hostname
                    * name

            - get-local:
                Return the local IP-Address to the command-line and nothing else.

                Aliases:
                    * [get-]local
                    * [get-]private
                    * [get-]internal

            - get-all:
                Return the public IP, private IP, and hostname to the command-line and immediately exit.

                Aliases:
                    * [get-]all
                    * reveal

            - print-version-info:
                Print a pretty table of the version information for this program.

                Aliases:
                    * version-info
                    * version
                    * print-version-table
                    * print-version-info
    """
    sub_commands = parser.add_subparsers(
        dest='subcommands',
        metavar='COMMANDS',
        help='The sub-commands for IP Reveal',
        description='Sub-Commands'
    )

    # Set up the 'get-public' command and its aliases.
    sub_commands.add_parser(
        'get-public',
        help='Return the external IP to the command-line and nothing else.',
        aliases=aliases.get_public
    )

    # Set up the 'get-host' command and its aliases.
    sub_commands.add_parser(
        'get-host',
        help='Return the hostname to the command-line and nothing else.',
        aliases=aliases.get_host
    )

    # Set up the 'get-local' command and its aliases.
    sub_commands.add_parser(
        'get-local',
        help='Return the local IP-Address to the command-line and nothing else.',
        aliases=aliases.get_local
    )

    # Set up the 'get-all' command and its aliases.
    sub_commands.add_parser(
        'get-all',
        help='Return the local IP, external IP, and computer hostname before exiting.',
        aliases=aliases.get_all
    )

    # Set up the 'print-version-info' command and its aliases.
    pvi = sub_commands.add_parser(
        'print-version-info',
        help='Print a pretty table of the version information for this program.',
        aliases=aliases.print_version_info
    )

    pvi.add_argument(
        '-u', '--update',
        action='store_true',
        help='Check for an update to the program and print the results to the console.',
    )
