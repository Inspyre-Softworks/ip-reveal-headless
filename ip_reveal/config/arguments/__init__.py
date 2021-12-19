from argparse import ArgumentParser
from inspyre_toolbox.spanners.span_arg_parse import SubparserActionAliases

from inspy_logger import LEVELS as LOG_LEVELS


class ParsedArgs(object):
    
    class Aliases(object):
        def __init__(self):
            self.get_public = [
                    'get-external',
                    'external',
                    'public',
                    'ip',
                    'get-ip',
                    'internet',
                    'get-internet']
            self.test_audio = [
                    'audio-test',
                    'audiotest',
                    'testaudio',
                    'test-audio'
                    ]
            self.get_host = [
                    'get-hostname',
                    'hostname',
                    'host',
                    'name',
                    'get-name'
                    ]
            
            self.get_local = [
                    'local',
                    'get-private',
                    'private',
                    'get-internal',
                    'internal'
                    ]
            
            self.get_all = [
                    'all',
                    'reveal'
                    ]
    
    
    def __init__(self, prog, description, ver_obj) :
        """

        Instantiate the argument parser.
        
        Members:
            parser (argparse.ArgumentParser): A prepared argparse.ArgumentParser object.
        """
        self.aliases = self.Aliases()
        
        self.parser = ArgumentParser(prog, description)
        
        self.parser.register('action', 'parsers', SubparserActionAliases)
        
        self.parser.add_argument(
                '-l', '--log-level',
                choices=LOG_LEVELS,
                default='info'
                )
        
        # Argument to mute sounds
        self.parser.add_argument(
                '-m', '--mute-all',
                action='store_true',
                required=False,
                help="Starts the program with all program audio muted.",
                default=False
                )
        
        # Argument to implicitly set the refresh rate
        self.parser.add_argument(
                '-r', '--refresh-interval',
                type=int,
                default=30,
                help='Specify the number of seconds you want to have pass before IP-Reveal refreshes your IP '
                     'information. (Defaults to 30)',
                action='store'
                )
        
        self.parser.add_argument(
                '-V', '--version', action='version', version=str(ver_obj)
                )
        
        self.parser.add_argument(
                "--no-alerts", required=False, action='store_true', default=False,
                help="If you use this flag it will set"
                )
        
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
                help='Do not let the logger print it\'s initialization information',
                action='store_true',
                default=False
                )


def load_subcommands(parser) :
    """
    
    Create sub-commands for the passed argparse.ArgumentParser object along with their alias commands.
    
    Args:
        parser (argparse.ArgumentParser): An already instantiated argparse.ArgumentParser object
        that you'd like to add subparsers to.

    Returns:
        parser (argparse.ArgumentParser): The same object that was passed but with the following
        sub-commands:
        
            get-public:
                Return the external IP to the command-line and nothing else.
                
                Aliases:
                
                    * [get-]external
                    * public
                    * [get-]ip
             
            get-host:
                Return the hostname to the command-line and nothing else.
            
                Aliases:
                
                    * [get-]host
                    * [get-]hostname
                    * name
                    
            get-local:
                Return the IP-Address to the command-line and nothing else.
                
                Aliases:
                    * [get-]local
                    * [get-]private
                    * [get-]internal
                    
            get-all:
                Return the public ip, private ip, and hostname to the command-line and immediately exits
                
                Aliases:
                    * [get-]all
                    * reveal

    """
    
    
    
    args = parser
    parser = args.parser
    
    aliases = args.aliases
    
    sub_commands = parser.add_subparsers(
            dest='subcommands',
            metavar='COMMANDS',
            help='The sub-commands for IP Reveal',
            description='Sub-Commands'
            )
    
    # Set up the 'get-public' command and it's aliases.
    sub_commands.add_parser(
            'get-public',
            help='Return the external IP to the command-line and nothing else.',
            aliases=aliases.get_public)
    
    # Set up the 'get-host' command and it's aliases.
    sub_commands.add_parser(
            'get-host',
            help='Return the hostname to the command-line and nothing else.',
            aliases=aliases.get_host)
    
    # Set up the 'get-local' command and it's aliases.
    sub_commands.add_parser(
            'get-local',
            help='Return the local IP-Address to the command-line and nothing '
                 'else.',
            aliases=aliases.get_local)
    
    # Set up the 'get-all' command and it's aliases.
    sub_commands.add_parser(
            'get-all',
            help='Return the local IP, external IP, and computer hostname before exiting.',
            aliases=aliases.get_all)
    
    # Create the 'test-audio' command and it's aliases
    test_audio_parse = sub_commands.add_parser(
            'test-audio',
            help="To ensure you get notifications you can test IP-Reveal's audio "
                 "engine with this command.",
            aliases=aliases.test_audio)
    
    # Set up the countdown argument.
    test_audio_parse.add_argument(
            '-c', '--countdown',
            action='store',
            type=int,
            default=3,
            help="Enter the number to countdown from before starting the test."
            )
    
    # Set up the full test argument
    test_audio_parse.add_argument(
            '-f', '--full',
            help='Run the full range of audio tests provided by the audio engine',
            action='store_true',
            default=False,
            )
