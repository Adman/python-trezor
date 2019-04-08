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

from trezorlib import messages, onegram
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path

from .common import TrezorTest

ONEGRAM_PATH = parse_path("m/48'/10'/0'/0'/0'")


@pytest.mark.onegram
@pytest.mark.skip_t1
class TestMsgOnegramSignTx(TrezorTest):
    def test_onegram_sign_tx_transaction(self):
        self.setup_mnemonic_allallall()

        resp = onegram.sign_tx(
            self.client,
            ONEGRAM_PATH,
            dict_to_proto(
                messages.OnegramSignTx,
                {
                    "chain_id": "10ba5bd926fc0541dcfea83593fad914cde23978f01445192b174db51899f633",
                    "header": {
                        "head_block_number": 3062865,
                        "head_block_id": "002ebc5179132a54a837b33f6489501c047276cb",
                        "expiration": 1554448699
                    },
                    "fee": {
                        "amount": 10000,
                        "asset_id": "1.3.0"
                    },
                    "source": "1.2.1305",
                    "destination": "1.2.1296",
                    "amount": {
                        "amount": 1000000,
                        "asset_id": "1.3.0"
                    },
                    "memo": ""
                },
            ),
        )
        assert (
            resp.signature.hex()
            == "2008214b63885393a9f89164659e9f06aa9361db5b016f257bd2142034901ee44c05355a97a394432737bacd844b4468b2775d01906a183f48941979291fb51109"
        )
        assert (
            resp.tx_hash == "da2d1b86c6bb6d1f36d08a008f711e3c27f0277c"
        )
