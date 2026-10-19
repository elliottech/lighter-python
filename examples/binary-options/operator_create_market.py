import asyncio
import json
import time
import lighter
from examples.utils import default_example_setup

# Binary options operator flow (requires Lighter to have assigned MARKET_SLOT to this account).
# Slots are 1000..2000; a slot hosts one market at a time.
MARKET_SLOT = 1900
SYMBOL = "BTC-UPDOWN-TEST"
DURATION_MS = 5 * 60 * 1000


async def main():
    client, api_client, _ = default_example_setup()

    start_ms = int(time.time() * 1000)
    # size_decimals=4, price_decimals=2: 1 share pays settlement_cap=100 ticks = 1 USDC when it wins,
    # prices are 0..100 (implied probability in %).
    tx, tx_hash, err = await client.binary_options_operator_create_market(
        market_slot=MARKET_SLOT,
        start_timestamp_ms=start_ms,
        end_timestamp_ms=start_ms + DURATION_MS,
        settlement_cap=100,
        settlement_type=client.BINARY_OPTIONS_SETTLEMENT_TYPE_DISCRETE,  # or BINARY_OPTIONS_SETTLEMENT_TYPE_CONTINUOUS (settles at any price in [0, cap])
        default_price=50,  # price used when the market is refunded
        taker_fee=0,
        maker_fee=0,
        min_base_amount=1,
        min_quote_amount=1_000_000,
        order_quote_limit=(1 << 48) - 1,
        open_interest_limit=(1 << 48) - 1,
        is_frozen=0,
        symbol=SYMBOL,
        size_decimals=4,
        price_decimals=2,
    )
    print(f"Create Market {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    # the public market index (used by create_order / update / settle) is in the tx event;
    # the tx shows up in the indexer a few seconds after it is accepted
    tx_api = lighter.TransactionApi(api_client)
    for _ in range(30):
        await asyncio.sleep(1)
        try:
            executed = await tx_api.tx(by="hash", value=tx_hash.tx_hash)
        except lighter.ApiException:
            continue
        print(f"market index: {json.loads(executed.event_info)['m']}")
        break

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
