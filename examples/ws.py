import json
import logging
import lighter

logging.basicConfig(level=logging.INFO)


def on_order_book(message):
    logging.info(
        f"Order book {message['channel']}:\n"
        f"{json.dumps(message.get('order_book'), indent=2)}"
    )


def on_account(message):
    logging.info(
        f"Account {message['channel']}:\n{json.dumps(message, indent=2)}"
    )


client = lighter.WsClient()
for market_id in [0, 1]:
    client.subscribe(f"order_book/{market_id}", on_update=on_order_book)
for account_id in [1, 2]:
    client.subscribe(f"account_all/{account_id}", on_update=on_account)

client.run()
