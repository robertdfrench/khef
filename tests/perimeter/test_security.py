# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import uuid


# Show that we fail to find a credential after it has been removed from the
# keychain.
def test_credential_does_not_exist():
    request = khef.KeychainRequest(
        host='khef.invalid',
        username='perimeter-test',
    )
    khef.Git.credential_reject(request)
    assert not khef.Security.find_internet_password(request)


# Show that we do find a credential after it has been inserted into the
# keychain.
def test_credential_exists():
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
    assert khef.Security.find_internet_password(request)
