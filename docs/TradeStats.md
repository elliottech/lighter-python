# TradeStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**volume** | **str** |  | 
**web_count** | **int** |  | 
**web_volume** | **str** |  | 
**mobile_app_count** | **int** |  | 
**mobile_app_volume** | **str** |  | 
**mobile_browser_count** | **int** |  | 
**mobile_browser_volume** | **str** |  | 

## Example

```python
from lighter.models.trade_stats import TradeStats

# TODO update the JSON string below
json = "{}"
# create an instance of TradeStats from a JSON string
trade_stats_instance = TradeStats.from_json(json)
# print the JSON string representation of the object
print(TradeStats.to_json())

# convert the object into a dict
trade_stats_dict = trade_stats_instance.to_dict()
# create an instance of TradeStats from a dict
trade_stats_from_dict = TradeStats.from_dict(trade_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


