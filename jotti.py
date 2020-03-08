import argparse

NO_JOTT = 'no_jott'

parser = argparse.ArgumentParser(description='Take notes')
g = parser.add_mutually_exclusive_group()
g.add_argument('--jott', '--take-note', type=str, help='Stores the given note.', default=NO_JOTT)
g.add_argument('--auth', '--login', dest='auth', action='store_true', default=False,
               help='stores jotti.in credentials for future use.')
g.add_argument('--notes', '--view-notes', '--jotts', dest='view_notes', action='store_true', default=False,
               help='Shows the latest notes.')

args = parser.parse_args()

if not args.jott == NO_JOTT:
    print(args.jott)

if args.view_notes:
    print('view notes')

if args.auth:
    print('auth')
