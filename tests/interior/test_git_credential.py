# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef


# Show that we can create a KeychainRecord containing known values for each of
# its members.
def test_create():
    cred = khef.KeychainRecord(
        host='khef.invalid',
        username='interior-test',
        password='password'
    )
    assert cred.host == 'khef.invalid'
    assert cred.username == 'interior-test'
    assert cred.password == 'password'


# Show that a KeychainRecord object can be serialized into the data format
# expected by the `git-credential(1)` command.
def test_str():
    cred = khef.KeychainRecord(
        host='khef.invalid',
        username='interior-test',
        password='password'
    )
    assert str(cred) == "\n".join([
        "protocol=https",
        "host=khef.invalid",
        "username=interior-test",
        "password=password"
    ])


# Show that we can parse output from the `git-credential` command into a
# working KeychainRecord object.
def test_parse():
    output = "\n".join([
        "protocol=https",
        "host=khef.invalid",
        "username=interior-test",
        "password=password"
    ])
    cred = khef.KeychainRecord.parse(output)
    assert cred.host == 'khef.invalid'
    assert cred.username == 'interior-test'
    assert cred.password == 'password'
