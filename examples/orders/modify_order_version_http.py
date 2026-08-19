import asyncio
import time
from examples.utils import default_example_setup


# Versioned order modification.
#
# order_version: a client-supplied, strictly increasing version guard for modify order.
#   * A modify with order_version=V is applied only if V is greater than the order's
#     current version. On success, the order's version becomes V.
#   * The default (NIL_ORDER_VERSION = 0) skips the check and always applies.
#   * A stale modify (version <= current) is rejected, which protects against
#     out-of-order or retried modifies overwriting a newer one.
#
# A common pattern is to use a millisecond timestamp as the version.
async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    # Note: change this to 2048 to trade spot ETH. Make sure you have at least 0.1 ETH to trade spot.
    market_index = 0
    client_order_index = int(time.time() * 1000)

    # create order
    api_key_index, nonce = client.nonce_manager.next_nonce()
    tx, tx_hash, err = await client.create_order(
        market_index=market_index,
        client_order_index=client_order_index,
        base_amount=1000,  # 0.1 ETH
        price=4050_00,  # $4050
        is_ask=True,
        order_type=client.ORDER_TYPE_LIMIT,
        time_in_force=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        reduce_only=False,
        trigger_price=0,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Create Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    ## modify order with version 100
    # use the same API key so the TX goes after the create order TX
    api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
    tx, tx_hash, err = await client.modify_order(
        market_index=market_index,
        order_index=client_order_index,
        base_amount=1100,  # 0.11 ETH
        price=4100_00,  # $4100
        trigger_price=0,
        order_version=100,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Modify Order (version=100) {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    ## stale modify: version 100 is not greater than the order's current version (100),
    ## so this modify is rejected by the exchange and the order keeps its previous state
    api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
    tx, tx_hash, err = await client.modify_order(
        market_index=market_index,
        order_index=client_order_index,
        base_amount=1200,  # 0.12 ETH
        price=4150_00,  # $4150
        trigger_price=0,
        order_version=100,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Stale Modify Order (version=100, expected to be rejected) {tx=} {tx_hash=} {err=}")

    ## modify order with a higher version (200) succeeds
    api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
    tx, tx_hash, err = await client.modify_order(
        market_index=market_index,
        order_index=client_order_index,
        base_amount=1200,  # 0.12 ETH
        price=4150_00,  # $4150
        trigger_price=0,
        order_version=200,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Modify Order (version=200) {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    ## cancel order
    api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
    tx, tx_hash, err = await client.cancel_order(
        market_index=market_index,
        order_index=client_order_index,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Cancel Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
