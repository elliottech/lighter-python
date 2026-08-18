# MarkPriceCandles


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**r** | **str** |  resolution | 
**c** | [**List[MarkPriceCandle]**](MarkPriceCandle.md) |  candles | 

## Example

```python
from lighter.models.mark_price_candles import MarkPriceCandles

# TODO update the JSON string below
json = "{}"
# create an instance of MarkPriceCandles from a JSON string
mark_price_candles_instance = MarkPriceCandles.from_json(json)
# print the JSON string representation of the object
print(MarkPriceCandles.to_json())

# convert the object into a dict
mark_price_candles_dict = mark_price_candles_instance.to_dict()
# create an instance of MarkPriceCandles from a dict
mark_price_candles_from_dict = MarkPriceCandles.from_dict(mark_price_candles_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


