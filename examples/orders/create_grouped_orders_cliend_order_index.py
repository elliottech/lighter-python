import asyncio
import time
from lighter.signer_client import CreateOrderTxReq
from examples.utils import default_example_setup

BASE_CID = int(time.time()) % (2 ** 48 - 10)

CID_PARENT = BASE_CID
CID_TP = BASE_CID + 1
CID_SL = BASE_CID + 2


async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    market_index = 0

    parent_order = CreateOrderTxReq(
        MarketIndex=market_index,
        ClientOrderIndex=CID_PARENT,
        BaseAmount=1000,  # 0.1 ETH
        Price=2500_00,  # $2500
        IsAsk=1,  # sell
        Type=client.ORDER_TYPE_LIMIT,
        TimeInForce=client.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
        ReduceOnly=0,
        TriggerPrice=0,
        OrderExpiry=0,
    )

    take_profit_order = CreateOrderTxReq(
        MarketIndex=market_index,
        ClientOrderIndex=CID_TP,
        BaseAmount=0,
        Price=1550_00,
        IsAsk=0,
        Type=client.ORDER_TYPE_TAKE_PROFIT_LIMIT,
        TimeInForce=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        ReduceOnly=1,
        TriggerPrice=1500_00,
        OrderExpiry=-1,
    )

    stop_loss_order = CreateOrderTxReq(
        MarketIndex=market_index,
        ClientOrderIndex=CID_SL,
        BaseAmount=0,
        Price=5050_00,
        IsAsk=0,
        Type=client.ORDER_TYPE_STOP_LOSS_LIMIT,
        TimeInForce=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        ReduceOnly=1,
        TriggerPrice=5000_00,
        OrderExpiry=-1,
    )

    result = await client.create_grouped_orders(
        grouping_type=client.GROUPING_TYPE_ONE_TRIGGERS_A_ONE_CANCELS_THE_OTHER,
        orders=[parent_order, take_profit_order, stop_loss_order],
    )
    print(f"Create Grouped Order: {result}")
    if result[2] is not None:
        print(f"  ERROR: {result[2]}")
    else:
        print("  OK")

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())