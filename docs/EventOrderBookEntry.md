# EventOrderBookEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** |  | 
**market_id** | **int** |  | 
**market_type** | **str** |  | 
**base_asset_id** | **int** |  | 
**quote_asset_id** | **int** |  | 
**status** | **str** |  waiting-for-settlement and settled are binary options only | 
**taker_fee** | **str** |  | 
**is_taker_fee_enabled** | **bool** |  | 
**maker_fee** | **str** |  | 
**is_maker_fee_enabled** | **bool** |  | 
**liquidation_fee** | **str** |  | 
**min_base_amount** | **str** |  | 
**min_quote_amount** | **str** |  | 
**order_quote_limit** | **str** |  | 
**supported_size_decimals** | **int** |  | 
**supported_price_decimals** | **int** |  | 
**supported_quote_decimals** | **int** |  | 
**created_at** | **str** |  | 
**multiplier** | **str** |  | 
**start_timestamp** | **int** |  | 
**end_timestamp** | **int** |  | 
**open_interest** | **str** |  | 
**outcome** | **int** |  | 
**operator_account_index** | **int** |  | 
**settlement_cap** | **int** |  | 
**settlement_type** | **int** |  | 
**settlement_price** | **int** |  | 
**default_price** | **int** |  | 
**is_frozen** | **bool** |  | 
**size_decimals** | **int** |  | 
**price_decimals** | **int** |  | 
**stats** | [**BinaryOptionMarketStats**](BinaryOptionMarketStats.md) |  | 

## Example

```python
from lighter.models.event_order_book_entry import EventOrderBookEntry

# TODO update the JSON string below
json = "{}"
# create an instance of EventOrderBookEntry from a JSON string
event_order_book_entry_instance = EventOrderBookEntry.from_json(json)
# print the JSON string representation of the object
print(EventOrderBookEntry.to_json())

# convert the object into a dict
event_order_book_entry_dict = event_order_book_entry_instance.to_dict()
# create an instance of EventOrderBookEntry from a dict
event_order_book_entry_from_dict = EventOrderBookEntry.from_dict(event_order_book_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


