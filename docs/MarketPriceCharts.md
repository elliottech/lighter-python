# MarketPriceCharts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**resolution** | **str** |  | 
**price_charts** | [**List[MarketPriceChart]**](MarketPriceChart.md) |  | 

## Example

```python
from lighter.models.market_price_charts import MarketPriceCharts

# TODO update the JSON string below
json = "{}"
# create an instance of MarketPriceCharts from a JSON string
market_price_charts_instance = MarketPriceCharts.from_json(json)
# print the JSON string representation of the object
print(MarketPriceCharts.to_json())

# convert the object into a dict
market_price_charts_dict = market_price_charts_instance.to_dict()
# create an instance of MarketPriceCharts from a dict
market_price_charts_from_dict = MarketPriceCharts.from_dict(market_price_charts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


