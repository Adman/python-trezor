# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib.onegram import get_public_key
from trezorlib.tools import parse_path

from .common import TrezorTest


@pytest.mark.onegram
@pytest.mark.skip_t1
class TestMsgOnegramGetPublicKey(TrezorTest):
    def test_onegram_get_public_key(self):
        self.setup_mnemonic_allallall()

        path = parse_path("m/48'/10'/0'/0'/0'")
        pk = get_public_key(self.client, path)
        assert (
            pk.raw_public_key.hex()
            == "02b139a33b197ae8b4c9170a595a81370eec52c649a99d9fae617e093966fce5d1"
        )
        assert (
            pk.wif_public_key
            == "OGC6EYLDdby3RAFbyPKnJpVGN6S67ApYpvyyxTooMU3r2xTu75jiW"
        )

        path2 = parse_path("m/48'/10'/0'/1'/0'")
        pk2 = get_public_key(self.client, path2)
        assert (
            pk2.raw_public_key.hex()
            == "0258d2ddbca90ffe1b956a30a86339e0056d20bc01753127988c0675750387033b"
        )
        assert (
            pk2.wif_public_key
            == "OGC5ZcEdH7G58CMtWxN3EMgMq299j4ziwZFZJ5od1EmsGUfVsyT7x"
        )
