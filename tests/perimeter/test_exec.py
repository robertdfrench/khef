# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import pytest
import os

def test_exec():
    khef.Exec("/usr/bin/true")

def test_exec_capture():
    output = khef.Exec("/bin/echo","-n","Hello","World")
    assert str(output) == "Hello World"

def test_exec_exception():
    with pytest.raises(khef.Exec.Failed):
        output = str(khef.Exec("/usr/bin/false"))

def test_exec_already_spent():
    output = khef.Exec("/bin/echo","-n","Hello","World")
    str(output)
    with pytest.raises(khef.Exec.Expired):
        str(output)

def test_exec_input():
    output = khef.Exec("/bin/cat","/dev/stdin", input=b'Hello, World!')
    assert str(output) == "Hello, World!"

def test_exec_iterate_output():
    for line in khef.Exec("/bin/echo","Hello\nHello\nHello"):
        assert str(line) == "Hello"

def test_exec_io_bytes():
    output = khef.Exec("/usr/bin/rev", input=b'12345')
    assert output.stdout.rstrip() == b'54321'

def test_filedescriptors():
    password="password"
    plaintext_1="plaintext"
    (r, w) = os.pipe()
    os.set_blocking(r, False)
    os.write(w, bytes(password, 'utf-8'))
    ciphertext = khef.Exec('/usr/bin/openssl', 'enc', '-A', '-chacha',
            '-base64', '-pass', f"fd:{r}", input=plaintext_1, pass_fds=(r,))
    ciphertext = ciphertext.stdout.rstrip()
    (r, w) = os.pipe()
    os.set_blocking(r, False)
    os.write(w, bytes(password, 'utf-8'))
    plaintext_2 = khef.Exec('/usr/bin/openssl', 'enc', '-d', '-A', '-chacha',
            '-base64', '-pass', f"fd:{r}", input=ciphertext, pass_fds=(r,))
    plaintext_2 = plaintext_2.stdout.rstrip()
    assert plaintext_1 == plaintext_2
