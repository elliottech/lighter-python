import asyncio
from lighter.signer_client import CreateOrderTxReq
from utils import default_example_setup


# Self-trade prevention applied to a grouped (OTOCO) order.
#
# For grouped orders the self-trade modes are specified once at the group level
# (a single value for the whole batch), matching the underlying signer.
async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    ioc_order = CreateOrderTxReq(
        MarketIndex=0,
        ClientOrderIndex=0,
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
        MarketIndex=0,
        ClientOrderIndex=0,
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
        MarketIndex=0,
        ClientOrderIndex=0,
        BaseAmount=0,
        Price=5050_00,
        IsAsk=0,
        Type=client.ORDER_TYPE_STOP_LOSS_LIMIT,
        TimeInForce=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        ReduceOnly=1,
        TriggerPrice=5000_00,
        OrderExpiry=-1,
    )

    transaction = await client.create_grouped_orders(
        grouping_type=client.GROUPING_TYPE_ONE_TRIGGERS_A_ONE_CANCELS_THE_OTHER,
        orders=[ioc_order, take_profit_order, stop_loss_order],
        self_trade_behavior_mode=client.SELF_TRADE_BEHAVIOR_EXPIRE_TAKER,
        self_trade_equality_mode=client.SELF_TRADE_EQUALITY_ACCOUNT_INDEX,
    )

    print("Create Grouped Order Tx:", transaction)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
