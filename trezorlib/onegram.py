from . import messages
from .tools import expect


@expect(messages.OnegramPublicKey)
def get_public_key(client, n, show_display=False):
    response = client.call(messages.OnegramGetPublicKey(
        address_n=n, show_display=show_display)
    )
    return response


@expect(messages.OnegramSignedTx)
def sign_tx(client, address_n, sign_tx_msg):
    sign_tx_msg.address_n = address_n
    return client.call(sign_tx_msg)
