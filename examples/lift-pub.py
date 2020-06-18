import argparse
import logging

from python_liftbridge import Lift
from python_liftbridge import Message


def parse_arguments():
    '''Argument parsing for the script'''
    parser = argparse.ArgumentParser(
        description='Liftbridge pub script.',
    )
    parser.add_argument(
        'stream',
        metavar='stream',
    )
    parser.add_argument(
        'msg',
        metavar='msg',
    )
    parser.add_argument(
        '-s',
        '--server',
        metavar='s',
        nargs='?',
        default='127.0.0.1:9292',
        help='(default: %(default)s)',
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Shows debug logs',
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    client = Lift(ip_address=args.server)
    client.publish(Message(value=args.msg, subject=args.stream))
    print("Published [{}]: '{}'".format(args.stream, args.msg))


main()
