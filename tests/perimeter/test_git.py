# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef

def test_print_version():
    khef.Git.print_version()

def test_credential_approve():
    cred = khef.KeychainRecord(
        host='khef.invalid',
        username='perimeter-test',
        password='password'
    )
    khef.Git.credential_approve(cred)

    request = khef.KeychainRequest(
        host='khef.invalid',
        username='perimeter-test',
    )
    cred = khef.Git.credential_fill(request)
    assert cred.password == 'password'

def test_credential_reject():
    cred = khef.KeychainRecord(
        host='khef.invalid',
        username='perimeter-test',
        password='password'
    )
    khef.Git.credential_approve(cred)

    request = khef.KeychainRequest(
        host='khef.invalid',
        username='perimeter-test',
    )
    khef.Git.credential_reject(request)
