# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import uuid


# Show how a user could (though they should not) manually interact with the
# keystone password. This commands may be removed as the app stabilizes, or
# they may require the use of a '--debug' flag or similar.
def test_x_keystone_create(capsys):
    keystone_password = str(uuid.uuid4())
    khef.main(["x-keystone-delete", "khef.invalid", "exterior-test"])
    khef.main(["x-keystone-create", "khef.invalid", "exterior-test", keystone_password])
    khef.main(["x-keystone-read", "khef.invalid", "exterior-test"])
    output = capsys.readouterr().out.rstrip()
    assert output == keystone_password
