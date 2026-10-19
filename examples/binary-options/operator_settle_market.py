import asyncio
from examples.utils import default_example_setup

MARKET_SLOT = 1900
MARKET_INDEX = 0  # from operator_create_market.py
SETTLEMENT_CAP = 100


async def main():
    client, api_client, _ = default_example_setup()

    # discrete market: settlement_price=SETTLEMENT_CAP -> YES (buyers) win, 0 -> NO (sellers) win.
    # To void the market instead: settlement_price=0, is_refund=1 (everyone is paid default_price).
    tx, tx_hash, err = await client.binary_options_operator_settle_market(
        market_slot=MARKET_SLOT,
        market_index=MARKET_INDEX,
        settlement_price=SETTLEMENT_CAP,
        is_refund=0,
    )
    print(f"Settle Market {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
