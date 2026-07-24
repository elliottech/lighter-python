import asyncio
from examples.utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    market_index = 0
    margin = 100 # usdc
    leverage = 7

    tx, tx_hash, err = await client.update_leverage(
        market_index=market_index,
        leverage=leverage,
        margin_mode=client.CROSS_MARGIN_MODE
    )
    quote_amount = margin * leverage
    print(f"Update Leverage {tx=} {tx_hash=} {err=}")

    # Note: this also works for spot
    tx, tx_hash, err = await client.create_market_order_quote_amount(
        market_index=market_index,
        client_order_index=0,
        quote_amount=quote_amount,
        max_slippage=0.001,
        is_ask=False
    )
    print(f"Create Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
