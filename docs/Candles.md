# Candles


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**r** | **str** | Resolution | 
**c** | [**List[Candle]**](Candle.md) | Array of candles (max 500 per call) | 
**message** | **str** |  | [optional] 

## Example

```python
from lighter.models.candles import Candles

# TODO update the JSON string below
json = "{}"
# create an instance of Candles from a JSON string
candles_instance = Candles.from_json(json)
# print the JSON string representation of the object
print(Candles.to_json())

# convert the object into a dict
candles_dict = candles_instance.to_dict()
# create an instance of Candles from a dict
candles_from_dict = Candles.from_dict(candles_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


