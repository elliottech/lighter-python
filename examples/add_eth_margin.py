import asyncio
import lighter
from utils import default_example_setup


async def fetch(api_client, idx):
    return (await lighter.AccountApi(api_client).account(by="index", value=str(idx))).accounts[0]

def eth_spot(a):
    for x in a.assets:
        if x.symbol == "ETH":
            return float(x.balance)
    return 0.0

def show(label, a):
    print(f"\n[{label}] mode={a.account_trading_mode} tav={a.total_asset_value}")
    for x in a.assets:
        extra = getattr(x, "additional_properties", {}) or {}
        mb = getattr(x, "margin_balance", None) or extra.get("margin_balance", "-")
        mm = getattr(x, "margin_mode", None) or extra.get("margin_mode", "-")
        print(f"  {x.symbol:<6} spot={x.balance} margin={mb} mode={mm}")


async def wait_for_change(api_client, idx, prev, timeout=60):
    for i in range(timeout * 2):
        await asyncio.sleep(0.5)
        a = await fetch(api_client, idx)
        if abs(eth_spot(a) - prev) > 1e-9:
            print(f"state updated after {(i+1)*0.5:.1f}s")
            return a
    print(f"timeout {timeout}s — state didn't change")
    return await fetch(api_client, idx)

async def main():
    client, api_client, _ = default_example_setup()
    before = await fetch(api_client, client.account_index)
    show("BEFORE", before)

    await client.update_account_config(account_trading_mode=1)
    await client.update_account_asset_config(
        asset_index=client.ASSET_ID_ETH,
        asset_margin_mode=client.ASSET_MARGIN_MODE_ENABLED,
    )
    await client.transfer_same_master_account(
        to_account_index=client.account_index,
        asset_id=client.ASSET_ID_ETH,
        amount=1.0,
        route_from=client.ROUTE_SPOT,
        route_to=client.ROUTE_PERP,
        fee=0,
        memo="0x" + "00" * 32,
    )

    after = await wait_for_change(api_client, client.account_index, eth_spot(before))
    show("AFTER", after)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())