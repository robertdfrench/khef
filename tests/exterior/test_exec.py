# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import os
import uuid


def test_cipher_algorithms(capsys):
    khef.main(["x-list-ciphers"])
    output = capsys.readouterr().out
    assert "ChaCha" in output


def test_encrypt_symmetric():
    # Generate a random plaintext string
    plaintext = str(uuid.uuid4())

    # Write our plaintext to disk
    with open("plain.txt","w") as f:
        f.write(plaintext)

    # Encrypt that plaintext
    khef.main(["x-encrypt-symmetric", "plain.txt", "password", "cipher.txt"])

    # Remove the original plaintext file
    os.unlink("plain.txt")

    # Decrypt the ciphertext, thereby recovering the plain.txt file
    khef.main(["x-decrypt-symmetric", "cipher.txt", "password", "plain.txt"])

    # Read and compare new plain.txt file
    with open("plain.txt","r") as f:
        assert plaintext == f.read().rstrip()

    # Cleanup
    os.unlink("plain.txt")
    os.unlink("cipher.txt")


def test_git_version(capsys):
    khef.main(["x-git-version"])


def test_openssl_version(capsys):
    khef.main(["x-openssl-version"])
    output = capsys.readouterr().out
    assert "LibreSSL" in output
