#!/usr/bin/env python3
# 
# pycman-query - A Python implementation of Pacman
# Copyright (C) 2011 Rémy Oudompheng <remy@archlinux.org>
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
A Python implementation of pacman -Q

This script displays information about installed packages.
"""

import sys
import pyalpm
from . import config

def display_pkginfo(pkg):
	pass

def display_pkg(pkg, options):
	if options.info > 0:
		display_pkginfo(pkg, options.info)
	elif not options.listfiles:
		if options.quiet:
			print(pkg.name)
		else:
			print(pkg.name, pkg.version)

	if options.listfiles:
		if options.quiet:
			[print('/' + f) for f in pkg.files]
		else:
			[print(pkg.name, '/' + f) for f in pkg.files]

def main(rawargs):
	parser = config.make_parser(prog = 'pycman-query')
	group = parser.add_argument_group("Query options")
	group.add_argument('-i', '--info',
			action = 'count', dest = 'info', default = 0,
			help = 'view package information')
	group.add_argument('-l', '--list',
			action = 'store_true', dest = 'listfiles', default = False,
			help = 'list the contents of the queried package')
	group.add_argument('-q', '--quiet',
			action = 'store_true', dest = 'quiet', default = False,
			help = 'show less information for query and search')
	group.add_argument('pkgnames', metavar = 'pkg', nargs = '*',
			help = 'packages to show (show all packages if no arguments)')

	args = parser.parse_args(rawargs)
	config.init_with_config(args)

	if args.verbose:
		print("query " + " ".join(rawargs), file = sys.stderr)

	db = pyalpm.get_localdb()
	if len(args.pkgnames) > 0:
		# a list of package names was specified
		for pkgname in args.pkgnames:
			pkg = db.get_pkg(pkgname)
			if pkg is None:
				print('error: package "%s" not found' % pkgname)
			else:
				display_pkg(pkg, args)
	else:
		# no package was specified, display all
		for pkg in db.pkgcache:
			display_pkg(pkg, args)

	return 0

if __name__ == "__main__":
	ret = main(sys.argv[1:])
	sys.exit(ret)

# vim: set ts=4 sw=4 tw=0 noet: