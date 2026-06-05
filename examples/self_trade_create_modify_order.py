import asyncio
import time
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
    market_index = 156

    try:
        client.check_client()

        base_client_order_index = int(time.time() * 1000)
        resting_bid_order_index = base_client_order_index
        incoming_ask_order_index = base_client_order_index + 1

        api_key_index, nonce = client.nonce_manager.next_nonce()
        tx, tx_hash, err = await client.create_order(
            market_index=market_index,
            client_order_index=resting_bid_order_index,
            base_amount=500,
            price=95_200,
            is_ask=False,
            order_type=client.ORDER_TYPE_LIMIT,
            time_in_force=client.ORDER_TIME_IN_FORCE_POST_ONLY,
            reduce_only=False,
            trigger_price=0,
            nonce=nonce,
            api_key_index=api_key_index,
        )
        print(f"Resting Bid {tx=} {tx_hash=} {err=}")
        if err is not None:
            raise Exception(err)

        api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
        tx, tx_hash, err = await client.create_order(
            market_index=market_index,
            client_order_index=incoming_ask_order_index,
            base_amount=500,
            price=95_200,
            is_ask=True,
            order_type=client.ORDER_TYPE_LIMIT,
            time_in_force=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
            reduce_only=False,
            trigger_price=0,
            self_trade_behavior_mode=client.SELF_TRADE_BEHAVIOR_EXPIRE_BOTH,
            self_trade_equality_mode=client.SELF_TRADE_EQUALITY_MASTER_ACCOUNT_INDEX,
            nonce=nonce,
            api_key_index=api_key_index,
        )
        print(f"Self-Cross Create {tx=} {tx_hash=} {err=}")
        if err is not None:
            raise Exception(err)
    finally:
        await client.close()
        await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
