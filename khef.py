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
import abc
import argparse
import dataclasses
import functools
import os
import subprocess
import sys
import textwrap
import typing


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
    Subcommand.dispatch(argv, prog='khef', version='0.1.0',
                        description='Share secrets with your Ka-tet')


# This is the class of objects which represent 'subcommands': actions that can
# be invoked form the command line interface, such as `khef init` and `khef
# share`. This class is sortof peculiar, in that it is used primarily as a
# function decorator. This makes it easy to define subcommands (do check out
# the "init" function below), but it requires some subtleties that may not be
# obvious to the casual Python programmer.
#
# The goal is to make it as easy as possible to create new subcommands and
# define their arguments. Python's builtin argparse module is good, but a bit
# awkward. Our Subcommand class makes it a bit easier to enjoy the handful of
# features that we really need for khef.
class Subcommand:
    instances: typing.Dict[str, typing.Any] = {}

    # Define a new subcommand basd on `f`. The subcommand name will follow the
    # global name of the function `f`, but with underscores replaced by dashes.
    # For example, consider the following definition:
    #
    # 	@Subcommand
    # 	def long_days_pleasant_nights(the_number: int):
    # 	    print(the_number * 2)
    #
    # This will produce the following subcommand:
    #
    # 	$ khef long-days-pleasant-nights 19
    #
    # Where '19' is the number of long days which we would like to wish upon
    # someone.
    #
    # Each subcommand is stored (in the `Subcommand` class object itself)
    # according to its underlying function name.
    def __init__(self, f: typing.Callable):
        self.f = f
        functools.wraps(f)(self)
        Subcommand.instances[f.__name__] = self

    def __repr__(self) -> str:  # pragma: no cover
        return self.f.__name__

    # This function determines the names of the arguments expected by the
    # subcommand definition (that is, the function definition decorated by the
    # Subcommand class).
    def argument_names(self) -> typing.List[str]:
        keys = self.f.__annotations__.keys()
        return [k for k in keys if k != 'return']

    # This is a syntactic-sugar kind of command, which just makes it easier to
    # access the annotations (the argument names and their types) of the
    # function `f`.
    def annotations(self) -> typing.Dict[str, type]:
        return self.f.__annotations__

    # Convert the provided `args` into a list of Python objects which can be
    # used as arguments for the underlying function `self.f`.
    def argv(self, args: argparse.Namespace) -> typing.List[typing.Any]:
        names = self.argument_names()
        values = vars(args)
        return [values[n] for n in names]

    # Invokes the underlying function `self.f` with the unpacked command-line
    # arguments. This is the function that is actually invoked by the argparse
    # framework in the following Subcommand.dispatch mehod.
    def __call__(self, args: argparse.Namespace) -> None:
        arguments = self.argv(args)
        self.f(*arguments)

    # This function extracts the help and description text from the docstring
    # of a Subcommand-decorated function.
    @staticmethod
    def parse_doc(doc: str) -> typing.Tuple[str, str]:
        lines = doc.splitlines()
        help_text = lines[0]
        desc_text = "\n".join(lines[1:])
        return (help_text, desc_text)

    # This function expects to be called with the contents of sys.argv,
    # omitting the application name. Its job is to parse those arguments, and
    # invoke an appropriate subroutine to handle them. This is designed
    # entirely around Python3's built-in argparse module, so refer to its
    # documentation for details.
    @classmethod
    def dispatch(self, argv: typing.List[str], prog: str = "",
                 version: str = "", description: str = ""):
        usage = f"{prog} [options]"
        epilog = """For more information on any subcommand, simply run `khef
        <subcommand> -h`"""
        parser = argparse.ArgumentParser(prog=prog, description=description,
                                         usage=usage, epilog=epilog)
        parser.add_argument('--version', action='version', version=version)
        # By default, we want to print the parser-level help message. That is,
        # if the user invokes 'khef' without providing any subcommand argument,
        # we want argparse to present a list of all the subcommands and their
        # high-level description.
        parser.set_defaults(f=lambda x: parser.print_help())
        subparsers = parser.add_subparsers(title='subcommands',
                                           metavar='(many other functions)')

        # For each function that has been decorated with @Subcommand, take its
        # name and replace all the underscores with hyphens:
        epilog_formatter = argparse.RawDescriptionHelpFormatter
        for name, func in self.instances.items():
            hyphenated_name = name.replace('_', '-')
            (help_text, desc_text) = Subcommand.parse_doc(func.__doc__)
            sp = subparsers.add_parser(
                hyphenated_name,
                help=help_text,
                formatter_class=epilog_formatter,
                epilog=textwrap.dedent(desc_text)
            )
            # For each annotated variable of this function (each function
            # argument) add a *required* argument to the subcommand's subparser
            # -- subcommand arguments must be of a type that can double as a
            # string constructor. That is to say, they must expect a string as
            # the one and only constructor input. Like int or PosixPath or
            # something.
            #
            # However, since the help message for this argument will be derived
            # from the pydoc of the class of the type of this argument, it is
            # better to create a custom subclass for each argument, so that you
            # can describe its usage with a docstring:
            #
            # class GithubUsername(str):
            #     """Your username on github.com""""
            #     pass
            for name, cls in func.annotations().items():
                sp.add_argument(name, type=cls, help=cls.__doc__)
            sp.set_defaults(f=func)

        # Parse the provided arguments into Python objects, and pass them as
        # arguments to the underlying function for the selected (by the user)
        # subcommand object. In other words, if the user types:
        #
        # $ khef long-days-pleasant-nights 19
        #
        # We would then invoke the function `long_days_pleasant_nights` with
        # the sole argument (int("19")).
        args = parser.parse_args(argv)
        args.f(args)


# This is the class of all Subcommand Arguments. This class doesn't do anything
# on its own, it just makes it easier to identify classes that are used to
# represent command-line arguments for Subcommands.  Effectively, these class
# exists just to provide the help documentation for Subcommand objects
class Argument(str, abc.ABC):
    pass


# Keychain Records
# ----------------
#
# These classes support interacting with the system keychain through,
# curiously, git's `credential` subcommand (see git-credential(1) for more
# information). In text format, a request to retrieve a keychain item looks
# like this:
#
#   protocol=https
#   host=example.com
#   username=will.dearborn
#
# Both the respose to such a request AND a command to *set* a keychain record
# will look like this:
#
#   protocol=https
#   host=example.com
#   username=will.dearborn
#   password=nineteen
#
# These classes are able to parse, store, and produce records of this format.
@dataclasses.dataclass
class AbstractKeychainRecord(abc.ABC):
    host: str
    username: str

    # Serialize the current record into the format described above. Note the
    # use of `dataclasses.asdict` from the python stdlib -- that produces a
    # dictionary representation of all and only the named fields of this and
    # any child class. The upshot is that we get a password field only when the
    # KeychainRecord class is involved, and we don't get a password field when
    # the KeychainRequest class is used.
    def __str__(self):
        d = dataclasses.asdict(self)
        return "protocol=https\n" + \
               "\n".join([f"{k}={v}" for (k, v) in d.items()])


# Same as above, but include a 'password' field which will contain either the
# value of the password as currently stored in the system keychain (for
# reading) or the value of the password as it *should* be stored in the system
# keychain (for writing).
@dataclasses.dataclass
class KeychainRecord(AbstractKeychainRecord):
    password: str

    @staticmethod
    def parse(raw: str) -> "KeychainRecord":
        # One dictionary entry per line, so split
        lines = raw.splitlines()
        # splitting 'k=v' on the '=' produces a collection of [k, v] arrays
        d = {p[0]: p[1] for p in [line.split('=') for line in lines]}
        return KeychainRecord(d['host'], d['username'], d['password'])


# The KeychainRequest class is for requesting keychain records from the system
# keychain database, and does not need any capabilities beyond what's present
# in the AbstractKeychainRecord class -- we differentiate only for the sake of
# having meaningful data types.
@dataclasses.dataclass
class KeychainRequest(AbstractKeychainRecord):
    pass


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
        if 'capture_status' in kwargs:
            kwargs['check'] = False
            del kwargs['capture_status']
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
            raise Exec.Expired()  # pragma: no cover
        try:
            return self._run(capture_output=True).stdout
        finally:
            self.pending = False

    @property
    def returncode(self):
        if not self.pending:
            raise Exec.Expired()  # pragma: no cover
        try:
            return self._run(capture_status=True).returncode
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


# This is our wrapper for the git utility.
class Git:

    # Print the version of git that we are running. There is no particular
    # reason to do it this way (allowing the Exec object to be reaped by the
    # destructor) other than it is currently our only way of testing that
    # particular behavior.
    #
    # TODO: return a normal version string once something else uses this
    # destructor printing behavior
    @staticmethod
    def print_version():
        Exec("/usr/bin/git", "--version")

    # Write a KeychainRecord object into the system keychain, or replace an
    # existing one.
    @staticmethod
    def credential_approve(cred: KeychainRecord):
        Exec('/usr/bin/git', 'credential', 'approve', input=str(cred))

    # Retrieve a KeychainRecord object from the system keychain, if it exists.
    # Be advised that if such an object does not exist in the system keychain,
    # macOS will interactively prompt the user to supply the password --
    # Apple's understanding of this use case is slightly different than Git's
    # understanding of it, but since we are using `git-credential(1)` rather
    # than Apple's (much flakier) `security(1)`, we are stuck with this edge
    # case.
    @staticmethod
    def credential_fill(request: KeychainRequest) -> KeychainRecord:
        output = Exec('/usr/bin/git', 'credential', 'fill', input=str(request))
        return KeychainRecord.parse(output.stdout)

    # Remove the item specified in the KeychainRequest from the system
    # keychain. The macOS system keychain is not version-controlled, so even if
    # you use iCloud to sync your keychain contents, deleting it from one host
    # will cause it to be deleted from all others as soon as they talk to
    # iCloud.
    @staticmethod
    def credential_reject(request: KeychainRequest):
        Exec('/usr/bin/git', 'credential', 'reject', input=str(request))


# This wraps Apple's security(1) utility
class Security:
    @staticmethod
    def exists(request: KeychainRequest) -> bool:
        rc = Exec(
            '/usr/bin/security', 'find-internet-password',
            '-a', request.username,
            '-s', request.host
        ).returncode
        return rc == 0


# This is our wrapper for the OpenSSL utility
class OpenSSL:

    # Return the OpenSSL version as a string
    @staticmethod
    def version() -> str:
        return str(Exec("/usr/bin/openssl", "version"))

    # Create a pipe with nonblocking read. Such a pipe will be correctly
    # configured for use as an 'fd' argument to the 'enc' subcommand, allowing
    # us to interact with OpenSSL through something other than stdin (which, in
    # the case of 'enc', will be occupied by the input data).
    @staticmethod
    def pipe_with_nonblocking_read() -> typing.Tuple[int, int]:
        (r, w) = os.pipe()
        os.set_blocking(r, False)
        return (r, w)

    # Encrypt a plaintext string using the provided password, producing a
    # Base64-encoded ciphertext string.
    @staticmethod
    def symmetric_encrypt(plaintext: str, password: str) -> str:
        (r, w) = OpenSSL.pipe_with_nonblocking_read()
        os.write(w, bytes(password, 'utf-8'))
        ciphertext = Exec(
                '/usr/bin/openssl', 'enc', '-A', '-chacha',
                '-base64', '-pass', f"fd:{r}", input=plaintext, pass_fds=(r,))
        return ciphertext.stdout.rstrip()

    # Decrypt a Base64-encoded ciphertext string using the provided password.
    @staticmethod
    def symmetric_decrypt(ciphertext: str, password: str) -> str:
        (r, w) = OpenSSL.pipe_with_nonblocking_read()
        os.write(w, bytes(password, 'utf-8'))
        plaintext = Exec(
                '/usr/bin/openssl', 'enc', '-d', '-A', '-chacha',
                '-base64', '-pass', f"fd:{r}", input=ciphertext, pass_fds=(r,))
        return plaintext.stdout.rstrip()


# TODO: Wrap this in print() once we have something else that uses this
@Subcommand
def x_git_version():
    """Print the version of git on this host."""
    Git.print_version()


# TODO: Remove this when we have real functionality that converts Exec objects
# into strings.
@Subcommand
def x_openssl_version():
    """Print the version of OpenSSL on this host."""
    print(OpenSSL.version())


class PlaintextFile(Argument):
    """A (sensitive) file which contains human-readable text"""
    pass


class RawPassword(Argument):
    """A(n unsafe) password, which may be visible to others on this system"""
    pass


class CiphertextFile(Argument):
    """An encrypted file"""
    pass


@Subcommand
def x_encrypt_symmetric(
        plaintext_file: PlaintextFile,
        password: RawPassword,
        ciphertext_file: CiphertextFile):
    """Encrypt a plaintext file using a password provided on the command line.

    It is unsafe, and should not be used. Its only use is to test how Exec
    objects are created with file descriptors and input text."""
    with open(plaintext_file, "r") as p:
        with open(ciphertext_file, "w") as c:
            plaintext = p.read()
            ciphertext = OpenSSL.symmetric_encrypt(plaintext, password)
            c.write(ciphertext)


@Subcommand
def x_decrypt_symmetric(
        ciphertext_file: CiphertextFile,
        password: RawPassword,
        plaintext_file: PlaintextFile):
    """Decrypt a ciphertext file using a password provided on the command line.

    It is unsafe, and should not be used. Its only use is to test how Exec
    objects are created with file descriptors and input text."""
    with open(ciphertext_file, "r") as c:
        with open(plaintext_file, "w") as p:
            ciphertext = c.read()
            plaintext = OpenSSL.symmetric_decrypt(ciphertext, password)
            p.write(plaintext)


@Subcommand
def x_list_ciphers():
    """List all available OpenSSL ciphers on this system.

    Its only use is to test how Exec objects behave as iterables. """
    for cipher in Exec("/usr/bin/openssl", "list-cipher-algorithms"):
        print(cipher)


class Host(Argument):
    """DNS record applicable to the password"""
    pass


class Username(Argument):
    """Username associatd with the account"""
    pass


@Subcommand
def x_keystone_create(host: Host, username: Username, password: RawPassword):
    """Manually set your keystone password.

    This is unsafe. The keystone password should only ever be generated for you
    by khef. There is no reason to know its contents."""
    Git.credential_approve(
        KeychainRecord(
            host=host,
            username=username,
            password=password
        )
    )


@Subcommand
def x_keystone_read(host: Host, username: Username):
    """Print your keystone password.

    This is unsafe. The keystone password should only ever be handled by khef.
    There is no reason to know its contents."""
    record = Git.credential_fill(
        KeychainRequest(
            host=host,
            username=username
        )
    )
    print(record.password)


@Subcommand
def x_keystone_delete(host: Host, username: Username):
    """Delete your keystone password.

    This is unsafe. It will permanently lock you out of khef."""
    Git.credential_reject(
        KeychainRequest(
            host=host,
            username=username
        )
    )


@Subcommand
def x_keystone_exists(host: Host, username: Username):
    """Delete your keystone password.

    This is unsafe. It will permanently lock you out of khef."""
    print(Security.exists(
        KeychainRequest(
            host=host,
            username=username
        )
    ))


# Invoke the `main` function (top of this file) with all of the arguments given
# on the command line. The first item in argv (the program name) is skipped,
# since this is the convention used by Python's built-in argparse module.
if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
