# MarketPriceChart


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**market_id** | **int** |  | 
**prices** | **List[str]** |  | 

## Example

```python
from lighter.models.market_price_chart import MarketPriceChart

# TODO update the JSON string below
json = "{}"
# create an instance of MarketPriceChart from a JSON string
market_price_chart_instance = MarketPriceChart.from_json(json)
# print the JSON string representation of the object
print(MarketPriceChart.to_json())

# convert the object into a dict
market_price_chart_dict = market_price_chart_instance.to_dict()
# create an instance of MarketPriceChart from a dict
market_price_chart_from_dict = MarketPriceChart.from_dict(market_price_chart_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


