#!/usr/bin/env python
import sys
import string
import socket
from time import sleep


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

	# The variable at the end is the score that will be added to those that
	# the user has not supplied any value. If it's zero, those cases are not
	# even tested. If you really want to test all possible letter conversions,
	# set this to one, but better idea is to improve the conversion table.
	conv_table = formCompleteConversionTable(domain, BASIC_CONV_TABLE, 0)

	# Now start forming different combinations. All combinations consist of three different
	# modifications: conversion of letters, adding of letters and removing of letters.
	# What varies is the amounts of these modifications. The following variable is used to
	# track the combinations of these amounts
	modcounts = [1, 0, 0]
	while True:
		# Do modifications
		modifyAndCheckDomain(domain, modcounts, [0, 0, 0], conv_table)

		modcounts = getNextModCountsCombination(modcounts)


def modifyAndCheckDomain(domain, modcounts, modpositions, conv_table):

	# If there is no conversion options left, then check the domain
	if sum(modcounts) == 0:
		try:
			socket.gethostbyname(domain)
			print domain + ' EXISTS!'
		except socket.gaierror:
			pass
		# Sleep a little to not spam DNS server
		sleep(0.01)
		return

	# Do letter removing
	if modcounts[2] > 0:
		for pos in rangeFromCenter(modpositions[0], len(domain)):
			letter = domain[pos]
			if letter != '.':
				converted_domain = domain[:pos] + domain[pos + 1:]
				# TODO: Do not accept domains with invalid TLD
				modcounts2 = [modcounts[0], modcounts[1], modcounts[2] - 1]
				modpositions2 = [modpositions[0], modpositions[1], pos + 1]
				modifyAndCheckDomain(converted_domain, modcounts2, modpositions2, conv_table)
		return

	# Do letter conversions
	if modcounts[0] > 0:

		# Letter conversion is started from those letters,
		# that are easiest to confuse to some other letters.
		highest_score = 0
		for letter in domain[modpositions[0]:]:
			if letter != '.':
				for to, score in conv_table[letter].items():
					if score > highest_score:
						highest_score = score
		if highest_score == 0:
			return

		# Now that the highest score is known, we go all
		# conversions using it, then the second highest, etc.
		for score in range(highest_score, 0, -1):
			for pos in rangeFromCenter(modpositions[0], len(domain)):
				letter = domain[pos]
				if letter != '.':
					convs = conv_table[letter]
					for conv, conv_score in convs.items():
						if conv_score == score:
							converted_domain = domain[:pos] + conv + domain[pos + 1:]
							# TODO: Do not accept domains with invalid TLD
							modcounts2 = [modcounts[0] - 1, modcounts[1], modcounts[2]]
							modpositions2 = [pos + 1, modpositions[1], modpositions[2]]
							modifyAndCheckDomain(converted_domain, modcounts2, modpositions2, conv_table)
		return

	# TODO: Do letter addings!


def formCompleteConversionTable(domain, source_conversion_table, default_value):
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
				conv_table[frm][to] = default_value

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


class rangeFromCenter(object):
		def __init__(self, start, end):
			self.start = start
			self.end = end
			# Begin is not used when selecting center
			self.center = end / 2
			self.diff = 0
			self.next_is_negative = True
		def __iter__(self):
			return self
		def __next__(self):
			return self.next()
		def next(self):
			while self.center - self.diff >= self.start or self.center + self.diff < self.end:
				pos = self.center + (-self.diff if self.next_is_negative else self.diff)
				if self.next_is_negative and self.diff > 0:
					self.next_is_negative = False
				else:
					self.next_is_negative = True
					self.diff += 1
				if pos >= self.start and pos < self.end:
					return pos
			raise StopIteration()


if __name__ == '__main__':
	main()
	sys.exit(0)
