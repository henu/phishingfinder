#!/usr/bin/env python
import sys

def main():
	# Read domain
	if len(sys.argv) != 2:
		raise Exception('Invalid arguments! Usage: ' + sys.argv[0] + ' <domain>')
	domain = sys.argv[1]


if __name__ == '__main__':
	main()
	sys.exit(0)
