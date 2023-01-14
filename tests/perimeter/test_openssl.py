# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import os


def test_version():
    assert 'LibreSSL' in khef.OpenSSL.version()


def test_nb_readpipe():
    (r, w) = khef.OpenSSL.pipe_with_nonblocking_read()
    assert not os.get_blocking(r)
    assert os.get_blocking(w)


def test_encryption():
    plaintext = "Hello, world!"
    password = "hunter2"
    ciphertext = khef.OpenSSL.symmetric_encrypt(plaintext, password)
    assert plaintext == khef.OpenSSL.symmetric_decrypt(ciphertext, password)
