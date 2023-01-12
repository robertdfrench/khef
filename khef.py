#!/usr/bin/python3
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Prologue
# --------
# This tool aims to help you communicate with a small group of friends. It is
# designed, primarily, to be easy to use correctly, and difficult to misuse.
# Secondarily, it is designed to be easy to audit. The reader should be able,
# with only a small amount of effort, to read and understand the program, and
# become convinced that the program behaves as advertised.
#
# The program is entirely self-contained, and is intended to be runnable after
# downloading, no installation or dependency-wrangling necessary. This is part
# of an overall motif of minimalism: after all, fewer features means less to
# screw up. To that end, you will notice that everything is done through the
# Python standard library or appeals to shell utilities, even when using an
# external package might have made things easier.
#
# There are two forms of comments used in the code: comments beginning with
# hash marks (as used in this Prologue), and Python "doctstrings", which begin
# and end with triple doublequotes: ("""). The former are used to convey
# meaning directly to you, the reader. The latter are used to construct the
# help menu system for this program, and are effectively end-user
# documentation. In most cases, these audiences will be one in the same, but we
# ask you to read the code wearing only one of these hats at a time.
#
# We hope you enjoy the program.
def hello():
    return "world"
