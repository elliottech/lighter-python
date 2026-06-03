import asyncio
from utils import default_example_setup


# Self-trade prevention (STP) on order creation / modification.
#
# self_trade_behavior_mode: what happens when your incoming order would match
#   one of your own resting orders.
#     EXPIRE_MAKER (0, default) - cancel your resting (maker) order
#     EXPIRE_TAKER (1)          - cancel the incoming (taker) order
#     EXPIRE_BOTH  (2)          - cancel both
#     REDUCE       (3)          - net the two against each other (no booked self-fill)
#
# self_trade_equality_mode: what counts as "yourself" for the check above.
#     ACCOUNT_INDEX        (0, default) - only the exact same account
#     MASTER_ACCOUNT_INDEX (1)          - any sub-account under the same master
#
# Notes:
#   * Defaults (EXPIRE_MAKER + ACCOUNT_INDEX) reproduce the previous behavior and
#     do not change the signed payload.
#   * REDUCE is not allowed together with MASTER_ACCOUNT_INDEX.
#   * Self-trade modes cannot be combined with integrator fees on the same tx.
async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    market_index = 0

    # create order: cancel the incoming order if it would hit our own resting order
    api_key_index, nonce = client.nonce_manager.next_nonce()
    tx, tx_hash, err = await client.create_order(
        market_index=market_index,
        client_order_index=123,
        base_amount=1000,  # 0.1 ETH
        price=4050_00,  # $4050
        is_ask=True,
        order_type=client.ORDER_TYPE_LIMIT,
        time_in_force=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        reduce_only=False,
        trigger_price=0,
        self_trade_behavior_mode=client.SELF_TRADE_BEHAVIOR_EXPIRE_TAKER,
        self_trade_equality_mode=client.SELF_TRADE_EQUALITY_MASTER_ACCOUNT_INDEX,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Create Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    # modify order: self-trade modes can be re-specified on modify as well
    api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
    tx, tx_hash, err = await client.modify_order(
        market_index=market_index,
        order_index=123,
        base_amount=1100,  # 0.11 ETH
        price=4100_00,  # $4100
        trigger_price=0,
        self_trade_behavior_mode=client.SELF_TRADE_BEHAVIOR_EXPIRE_BOTH,
        self_trade_equality_mode=client.SELF_TRADE_EQUALITY_ACCOUNT_INDEX,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Modify Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
