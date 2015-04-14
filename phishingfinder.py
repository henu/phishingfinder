#!/usr/bin/env python
import sys
import string


BASIC_CONV_TABLE = {
	'i': {
		'j': 4,
		'l': 4,
		'1': 3,
		't': 2
	},
	'o': {
		'0': 4,
		'e': 3,
		'a': 3,
	},
	'a': {
		'e': 3,
		'o': 2,
	},
	'c': {
		'o': 3,
		'e': 2,
	},
	't': {
		'7': 2,
	},
}

DOMAIN_LETTERS = [letter for letter in (string.lowercase + string.digits)]


def main():
	# Read domain
	if len(sys.argv) != 2:
		raise Exception('Invalid arguments! Usage: ' + sys.argv[0] + ' <domain>')
	domain = sys.argv[1].lower()

	conv_table = formCompleteConversionTable(domain, BASIC_CONV_TABLE)


def formCompleteConversionTable(domain, source_conversion_table):
	""" Forms complete conversion table, where every conversion from the letters of domain has score to every letter possible in domain names.

	source_conversion_table is used to get scores. For those without score, a default of 1 is used.
	"""

	# Find letters used in domain
	letters_in_domain = set([letter for letter in domain if letter != '.'])

	# Form complete conversion table
	conv_table = {}
	for frm in letters_in_domain:
		conv_table[frm] = {}
		for to in DOMAIN_LETTERS:
			if frm in source_conversion_table and to in source_conversion_table[frm]:
				conv_table[frm][to] = source_conversion_table[frm][to]
			elif to in source_conversion_table and frm in source_conversion_table[to]:
				conv_table[frm][to] = source_conversion_table[to][frm]
			else:
				conv_table[frm][to] = 1

	return conv_table

if __name__ == '__main__':
	main()
	sys.exit(0)
