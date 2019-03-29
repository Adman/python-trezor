import binascii
from datetime import datetime
from . import messages as proto
from .tools import CallException, expect, session, b58decode


def int_to_big_endian(value):
    return value.to_bytes((value.bit_length() + 7) // 8, "big")


def name_to_number(name):
    length = len(name)
    value = 0

    for i in range(0, 13):
        c = 0
        if i < length and i < 13:
            c = char_to_symbol(name[i])

        if i < 12:
            c &= 0x1f
            c <<= 64 - 5 * (i + 1)
        else:
            c &= 0x0f

        value |= c

    return value


def asset_to_number(asset):
    amount_str, symbol_str = asset.split(' ')
    dot_pos = amount_str.find('.')

    # parse symbol
    if dot_pos != -1:
        precision_digit = len(amount_str) - dot_pos - 1
    else:
        precision_digit = 0

    sym = symbol_from_string(precision_digit, symbol_str)

    # parse amount
    if dot_pos != -1:
        int_part = int(amount_str[:dot_pos])
        fract_part = int(amount_str[dot_pos + 1:])
        if int_part < 0:
            fract_part *= -1
    else:
        int_part = int(amount_str)
        fract_part = 0

    amount = int_part
    amount *= symbol_precision(sym)
    amount += fract_part

    return amount, sym


def char_to_symbol(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 6
    if '1' <= c <= '5':
        return ord(c) - ord('1') + 1
    return 0


def symbol_from_string(p, name):
    length = len(name)
    result = 0
    for i in range(0, length):
        result |= ord(name[i]) << (8 * (i + 1))

    result |= p
    return result


def symbol_precision(sym):
    return pow(10, (sym & 0xff))


def public_key_to_buffer(pub_key):
    _t = 0
    if pub_key[:3] == 'ONEGRAM':
        pub_key = pub_key[3:]
        _t = 0
    elif pub_key[:7] == 'PUB_K1_':
        pub_key = pub_key[7:]
        _t = 0
    elif pub_key[:7] == 'PUB_R1_':
        pub_key = pub_key[7:]
        _t = 1

    return _t, b58decode(pub_key, None)[:-4]


# ====== Client functions ====== #

@expect(proto.OnegramPublicKey)
def get_public_key(client, n, show_display=False, multisig=None):
    response = client.call(proto.OnegramGetPublicKey(address_n=n, show_display=show_display))
    return response


@expect(proto.OnegramSignedTx)
def sign_tx(client, address_n, sign_tx_msg):
    sign_tx_msg.address_n = address_n
    return client.call(sign_tx_msg)
