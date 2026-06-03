import asyncio
from utils import default_example_setup


# Scope a cancel-all to a single market.
#
# cancel_all_market_index:
#   NIL_MARKET_INDEX (255, default) - cancel resting orders across ALL markets
#   0..254                          - cancel resting orders only in that perp market
#
# Note: a non-nil market index is only valid for an immediate cancel-all
# (TIME_IN_FORCE_IMMEDIATE_OR_CANCEL), not for a scheduled / dead-man's-switch one.
async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    market_index = 0

    # cancel all of our resting orders, but only in market 0 (immediate uses timestamp_ms=0)
    api_key_index, nonce = client.nonce_manager.next_nonce()
    tx, tx_hash, err = await client.cancel_all_orders(
        time_in_force=client.CANCEL_ALL_TIF_IMMEDIATE,
        timestamp_ms=0,
        cancel_all_market_index=market_index,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Cancel All (market {market_index}) {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    # for reference: omit cancel_all_market_index (defaults to all markets)
    api_key_index, nonce = client.nonce_manager.next_nonce(api_key_index)
    tx, tx_hash, err = await client.cancel_all_orders(
        time_in_force=client.CANCEL_ALL_TIF_IMMEDIATE,
        timestamp_ms=0,
        nonce=nonce,
        api_key_index=api_key_index,
    )
    print(f"Cancel All (all markets) {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
