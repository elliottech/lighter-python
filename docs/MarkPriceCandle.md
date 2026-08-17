# MarkPriceCandle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**t** | **int** |  timestamp | 
**o** | **float** |  open | 
**h** | **float** |  high | 
**l** | **float** |  low | 
**c** | **float** |  close | 
**sc** | **int** |  sample_count | 

## Example

```python
from lighter.models.mark_price_candle import MarkPriceCandle

# TODO update the JSON string below
json = "{}"
# create an instance of MarkPriceCandle from a JSON string
mark_price_candle_instance = MarkPriceCandle.from_json(json)
# print the JSON string representation of the object
print(MarkPriceCandle.to_json())

# convert the object into a dict
mark_price_candle_dict = mark_price_candle_instance.to_dict()
# create an instance of MarkPriceCandle from a dict
mark_price_candle_from_dict = MarkPriceCandle.from_dict(mark_price_candle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


