# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef

def test_create():
    cred = khef.KeychainRecord(
        host='khef.invalid',
        username='interior-test',
        password='password'
    )
    assert cred.host == 'khef.invalid'
    assert cred.username == 'interior-test'
    assert cred.password == 'password'

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
