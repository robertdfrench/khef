# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import os
import pathlib
import uuid


# Show that running `khef init` creates a config file in the expected place in
# the user's home directory.
def test_download():
    absolute_source = pathlib.Path.cwd() / "source.txt"
    with open(absolute_source, "w") as f:
        f.write("source")
    source_url = f"file://{absolute_source}"
    dest = "dest.txt"
    khef.main("x-download", source_url, dest)
    with open(dest, "r") as f:
        assert f.read() == "source"


# Show that running `khef init` creates a config file in the expected place in
# the user's home directory.
def test_config_home(capsys):
    khef.main("x-environment-config")
    output = capsys.readouterr().out.rstrip()
    assert output.endswith("/.config/nkhef")


# Show that running `khef init` creates a config file in the expected place in
# the user's home directory.
def test_config_xdg_home(capsys):
    khef.main("x-environment-config", XDG_CONFIG_HOME="~/.xdg")
    output = capsys.readouterr().out.rstrip()
    assert output.endswith("/.xdg/nkhef")


def test_cipher_algorithms(capsys):
    khef.main("x-list-ciphers")
    output = capsys.readouterr().out
    assert "ChaCha" in output


def test_encrypt_symmetric():
    # Generate a random plaintext string
    plaintext = str(uuid.uuid4())

    # Write our plaintext to disk
    with open("plain.txt","w") as f:
        f.write(plaintext)

    # Encrypt that plaintext
    khef.main("x-encrypt-symmetric", "plain.txt", "password", "cipher.txt")

    # Remove the original plaintext file
    os.unlink("plain.txt")

    # Decrypt the ciphertext, thereby recovering the plain.txt file
    khef.main("x-decrypt-symmetric", "cipher.txt", "password", "plain.txt")

    # Read and compare new plain.txt file
    with open("plain.txt","r") as f:
        assert plaintext == f.read().rstrip()

    # Cleanup
    os.unlink("plain.txt")
    os.unlink("cipher.txt")


def test_git_version(capsys):
    khef.main("x-git-version")


def test_openssl_version(capsys):
    khef.main("x-openssl-version")
    output = capsys.readouterr().out
    assert "LibreSSL" in output


def test_x_keychain_delete(capsys):
    khef.main("x-keychain-delete", "khef.invalid", "exterior-test")
    khef.main("x-keychain-exists", "khef.invalid", "exterior-test")
    output = capsys.readouterr().out.rstrip()
    assert output == 'False'


# Show how a user could (though they should not) manually interact with the
# keychain password. This commands may be removed as the app stabilizes, or
# they may require the use of a '--debug' flag or similar.
def test_x_keychain_create(capsys):
    keychain_password = str(uuid.uuid4())
    khef.main("x-keychain-create", "khef.invalid", "exterior-test", keychain_password)
    khef.main("x-keychain-exists", "khef.invalid", "exterior-test")
    output = capsys.readouterr().out.rstrip()
    assert output == 'True'
    khef.main("x-keychain-read", "khef.invalid", "exterior-test")
    output = capsys.readouterr().out.rstrip()
    assert output == keychain_password
