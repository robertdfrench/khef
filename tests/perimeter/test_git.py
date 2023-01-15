# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef


def test_print_version():
    khef.Git.print_version()


# Show that we can write (approve) a new record into the system keychain, and
# that we can read it back out by *filling* a request:
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


# Show that we can write (approve) a new record into the system keychain, and
# that we can delete (reject) it without raising an error. This test does not
# actually confirm that the specified entry will be absent from the keychain,
# because attempting to fill a request for a missing keychain item results in
# an interactive prompt (causing the CI system to hang). So, this effect is
# actually confirmed by hand, and the point of this test is just to ensure that
# issuing the 'reject' command does not result in an error code.
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
