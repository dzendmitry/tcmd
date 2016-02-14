#!/usr/bin/env python3

import argparse
import subprocess as sp

import enumerate_interfaces as ei
from query_yes_no import query_yes_no

def execute(cmd, reraise=False):
	print('-->', ' '.join(cmd))
	try:
		sp.call(cmd, universal_newlines=True)
	except sp.SubprocessError as e:
		if reraise:
			raise e

def show(args):
	show_cmd = ['tc', args.t, 'show']
	if args.i:
		show_cmd += ['dev', args.i]
	execute(show_cmd)

def flush(args):
	flush_cmd = ['sudo', 'tc', 'qdisc', 'del', 'dev', '', 'root']
	if args.a:
		if not args.y and query_yes_no('Do you want flush all rules at all interfaces?', 'no'):
			try:
				for (interface, ip) in ei.all_interfaces():
					flush_cmd[-2] = interface
					execute(flush_cmd, True)
			except sp.SubprocessError:
				pass
	else:
		flush_cmd[-2] = args.i
		execute(flush_cmd)

def loss(args):
	pass

if __name__ == '__main__':
	cli_parser = argparse.ArgumentParser()
	cli_subparsers = cli_parser.add_subparsers()

	# Interface parser
	interface_parser = argparse.ArgumentParser(add_help=False)
	interface_parser.add_argument('interface', 
		help='interface (/eth0/eth1/ppp0/...)')

	# Show command
	parser_show = cli_subparsers.add_parser('show', 
		description='It shows rules for all interfaces by default.',
		help='show configuration of interface')
	parser_show.add_argument('-i', 
		help='interface (/eth0/eth1/ppp0/...)')
	parser_show.add_argument('-t', default='qdisc', choices=['qdisc', 'class', 'filter'],
		help='type [qdisc | class | filter]. qdisc by default')
	parser_show.set_defaults(func=show)

	# Flush command
	parser_flush = cli_subparsers.add_parser('flush',
		description='It flushs all rules from one or all interfaces', 
		help='flush rules from interface')
	if_group = parser_flush.add_mutually_exclusive_group(required=True)
	if_group.add_argument('-i', 
		help='interface (/eth0/eth1/ppp0/...)')
	if_group.add_argument('-a', action='store_true',
		help='flush all rules from all interfaces')
	parser_flush.add_argument('-y', action='store_true',
		help='default yes action in the case of an argument -a')
	parser_flush.set_defaults(func=flush)

	# Loss command
	parser_loss = cli_subparsers.add_parser('loss', parents=[interface_parser], 
		help='set the percentage of packet loss')
	parser_loss.add_argument('percent',
		help='percent of loss packets [0-100]')
	parser_loss.set_defaults(func=loss)

	args = cli_parser.parse_args()
	try:
		args.func(args)
	except AttributeError:
		cli_parser.parse_args(['-h'])