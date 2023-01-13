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
import subprocess
import sys
import typing


def hello():
    return "world"


# This class provides a way to execute UNIX subprocesses with the same ease of
# use as is provided by the POSIX shell backtick (`) feature. The goal is to
# make sure that
#
# x = Exec("find", ".", "-type", "f")
#
# has the exact same result as
#
# x=`find . -type f`
#
# which implies that the output should print to stdout when the variable is not
# assigned to anything.
class Exec:
    argv: typing.Tuple[str, ...]
    pending: bool

    # * argv is, of course, the argv that will be passed on to the subcommand.
    # * input is either a string or byte sequence, and if provided it will
    # become the subcommand's STDIN stream.
    # * pending means "is this command still waiting to be run". Keeping track
    # of this allows Exec objects to behave flexibly -- like a string when
    # assigned, and like a print operation when not assigned.
    def __init__(self, *argv: str,
                 input: typing.Optional[typing.Union[str, bytes]] = None,
                 pass_fds: typing.Optional[typing.Tuple[int, ...]] = None):
        self.argv = argv
        self.input = input
        self.pending = True
        self.pass_fds = pass_fds

    # Raise this if a caller attempts to get the subcomand's stdout *after* the
    # subcommand has been run. That's always a programming error, so this
    # exception allows us to fail quick without wondering why.
    class Expired(Exception):
        pass

    # This is only used by the unit tests, but giving a synonym to Python's
    # CalledProcessError makes it a bit easier to work with Exec when you
    # intend it to fail (as is the case when testing edge conditions).
    Failed = subprocess.CalledProcessError

    # Execute the subcommand.  This is tricky, and requires knowledge of
    # Python's subprocess module [1].  Here's what is being expressed:
    #
    # * We always "check" the subcommand -- if it doesn't return 0, throw an
    # exception
    # * If an `input` field was provided to Exec, we want to treat that as the
    # stdin of the subcommand.
    # * If `input` was provided AND that input was a string, we assume that the
    # subcommand's output will also be a string. That isn't necessarily always
    # the case, but when it isn't, we make the caller deal with it.
    #
    # [1]: https://docs.python.org/3.7/library/subprocess.html
    def _run(self, **kwargs):
        kwargs['check'] = True
        if self.input:
            kwargs['input'] = self.input
            if type(self.input) == str:
                kwargs['text'] = True
        if self.pass_fds:
            kwargs['pass_fds'] = self.pass_fds
        return subprocess.run(self.argv,  **kwargs)

    # Execute the subcommand and return its stdout. If the subcommand has
    # already been executed (like, if this function has already been called),
    # that's an error, so raise an exception.
    @property
    def stdout(self):
        if not self.pending:
            raise Exec.Expired()
        try:
            return self._run(capture_output=True).stdout
        finally:
            self.pending = False

    # This wrapper allows us to iterate over an Exec object like so:
    #
    #   for commit in Exec('git', 'log'):
    #       print(f"{commit} was a pretty good commit")
    #
    # This mirrors the way backticks behave in the shell.
    def __iter__(self):
        for line in str(self).splitlines():
            yield line

    # Convert stdout into a utf8 string if the process returned binary data.
    def __str__(self):
        stdout = self.stdout
        return str(stdout, encoding='utf-8')

    # If the Exec object was not assigned to any variable, or did not get
    # consumed by a call to stdout, then we execute the subcommand here
    # *without* trying to capture its stdout. That means khef's stdout
    # descriptor (probably the terminal) will get passed to the subcommand, and
    # whatever it does will just be printed to the terminal. This allows us to
    # write expressions like:
    #
    #   print("Here are my pubkeys")
    #   Exec("find",".ssh","-name","*.pub")
    #
    # which will print a list of ssh public keys when run from a user's home
    # directory.
    def __del__(self):
        if self.pending:
            return self._run()


# The man in black fled across the desert, and the gunslinger followed.
#
# This is where our journey begins. In fact, because this is Python, it already
# began in a footnote at the bottom of this file: a little hook to tell the
# interpreter to call this function when khef is being used as a program, but
# to do nothing when khef is being imported as a library (i.e.  when it is
# undergoing tests).
#
# The `argv` at the top is just a list of strings, the arguments provided to
# khef by its parent process -- probably your shell. A caveat here that may
# seem unusual for some: this list includes *only* the arguments, and does not
# (as is the case in most other places) begin with the program name.
def main(argv: typing.List[str]) -> None:
    print(" ".join(argv))


# Invoke the `main` function (top of this file) with all of the arguments given
# on the command line. The first item in argv (the program name) is skipped,
# since this is the convention used by Python's built-in argparse module.
if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
