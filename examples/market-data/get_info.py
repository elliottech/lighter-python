import asyncio
import datetime
import lighter
import logging

logging.basicConfig(level=logging.INFO)


# The address provided belongs to a dummy account registered on Testnet.
L1_ADDRESS = "0x8D7f03FdE1A626223364E592740a233b72395235"
ACCOUNT_INDEX = 65


async def print_api(method, *args, **kwargs):
    logging.info(f"{method.__name__}: {await method(*args, **kwargs)}")


async def account_apis(client: lighter.ApiClient):
    logging.info("ACCOUNT APIS")
    account_instance = lighter.AccountApi(client)
    await print_api(account_instance.account, by="l1_address", value=L1_ADDRESS)
    await print_api(account_instance.account, by="index", value=str(ACCOUNT_INDEX))
    await print_api(account_instance.accounts_by_l1_address, l1_address=L1_ADDRESS)
    await print_api(account_instance.apikeys, account_index=ACCOUNT_INDEX, api_key_index=3)



async def candlestick_apis(client: lighter.ApiClient):
    logging.info("CANDLESTICK APIS")
    candlestick_instance = lighter.CandlestickApi(client)
    await print_api(
        candlestick_instance.candles,
        market_id=0,
        resolution="1h",
        start_timestamp=int(datetime.datetime.now().timestamp() - 60 * 60 * 24),
        end_timestamp=int(datetime.datetime.now().timestamp()),
        count_back=2,
    )
    await print_api(
        candlestick_instance.fundings,
        market_id=0,
        resolution="1h",
        start_timestamp=int(datetime.datetime.now().timestamp() - 60 * 60 * 24),
        end_timestamp=int(datetime.datetime.now().timestamp()),
        count_back=2,
    )


async def order_apis(client: lighter.ApiClient):
    logging.info("ORDER APIS")
    order_instance = lighter.OrderApi(client)
    await print_api(order_instance.exchange_stats)
    await print_api(order_instance.order_book_details, market_id=0)
    await print_api(order_instance.order_books)
    await print_api(order_instance.recent_trades, market_id=0, limit=2)


async def transaction_apis(client: lighter.ApiClient):
    logging.info("TRANSACTION APIS")
    transaction_instance = lighter.TransactionApi(client)
    # ....
    
async def funding_apis(client: lighter.ApiClient):
    logging.info("FUNDING APIS")
    account_instance = lighter.FundingApi(client)
    await print_api(account_instance.funding_rates)

async def main():
    client = lighter.ApiClient(configuration=lighter.Configuration(host="https://testnet.zklighter.elliot.ai"))
    await account_apis(client)
    await candlestick_apis(client)
    await order_apis(client)
    await transaction_apis(client)
    await funding_apis(client)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
