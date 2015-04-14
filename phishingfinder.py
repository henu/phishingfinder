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

	# Now start forming different combinations. All combinations consist of three different
	# modifications: conversion of letters, adding of letters and removing of letters.
	# What varies is the amounts of these modifications. The following variable is used to
	# track the combinations of these amounts
	modcounts = [1, 0, 0]
	while True:
		# These are the amount of conversions we will make
		mod_convs = modcounts[0]
		mod_adds = modcounts[1]
		mod_removes = modcounts[2]

		# Do modificationms
		# TODO: Code this!

		modcounts = getNextModCountsCombination(modcounts)


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


def getNextModCountsCombination(modcounts):
	total_mods  = sum(modcounts)

	# In case of final combination with these
	# counts, increase the number of counts
	if modcounts[2] == total_mods:
		return [total_mods + 1, 0, 0]

	# If we should lower the first number
	if modcounts[0] + modcounts[2] == total_mods:
		return [modcounts[0] - 1, total_mods - modcounts[0] + 1, 0]

	# Decrease middle number
	return [modcounts[0], modcounts[1] - 1, modcounts[2] + 1]


if __name__ == '__main__':
	main()
	sys.exit(0)
