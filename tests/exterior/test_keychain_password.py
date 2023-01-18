# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import uuid


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
