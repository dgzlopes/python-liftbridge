import argparse

from python_liftbridge import Lift
from python_liftbridge import Message


def parse_arguments():
    '''Argument parsing for the script'''
    parser = argparse.ArgumentParser(
        description='Liftbridge pub script.',
    )
    parser.add_argument(
        'subject',
        metavar='subject',
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

    return parser.parse_args()


def main():

    args = parse_arguments()
    client = Lift(ip_address=args.server)
    client.publish(Message(value=args.msg, subject=args.subject))
    print("Published [{}]: '{}'".format(args.subject, args.msg))


main()
