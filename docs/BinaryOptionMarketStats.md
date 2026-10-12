# BinaryOptionMarketStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** |  | 
**market_id** | **int** |  | 
**mid_price** | **str** |  | 
**best_ask_price** | **str** |  | 
**best_bid_price** | **str** |  | 
**last_trade_price** | **str** |  | 
**daily_base_token_volume** | **float** |  | 
**daily_quote_token_volume** | **float** |  | 
**daily_price_low** | **float** |  | 
**daily_price_high** | **float** |  | 
**daily_price_change** | **float** |  | 
**lifetime_quote_token_volume** | **float** |  | 
**lifetime_base_token_volume** | **float** |  outcome shares traded over the market&#39;s life | 
**open_interest** | **str** |  | 
**status** | **str** |  inactive once the trading window closes | 
**outcome** | **int** |  | 

## Example

```python
from lighter.models.binary_option_market_stats import BinaryOptionMarketStats

# TODO update the JSON string below
json = "{}"
# create an instance of BinaryOptionMarketStats from a JSON string
binary_option_market_stats_instance = BinaryOptionMarketStats.from_json(json)
# print the JSON string representation of the object
print(BinaryOptionMarketStats.to_json())

# convert the object into a dict
binary_option_market_stats_dict = binary_option_market_stats_instance.to_dict()
# create an instance of BinaryOptionMarketStats from a dict
binary_option_market_stats_from_dict = BinaryOptionMarketStats.from_dict(binary_option_market_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


