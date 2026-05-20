# Candle

Abbreviated candle format. Zero values are omitted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**t** | **int** | Timestamp | 
**o** | **float** | Open price | 
**h** | **float** | High price | 
**l** | **float** | Low price | 
**c** | **float** | Close price | 
**v** | **float** | Base token volume (volume0) | 
**v** | **float** | Quote token volume (volume1) | 
**i** | **int** | Last trade ID | 
**c** | **float** |  close_raw | [optional] 
**h** | **float** |  high_raw | [optional] 
**l** | **float** |  low_raw | [optional] 
**o** | **float** |  open_raw | [optional] 

## Example

```python
from lighter.models.candle import Candle

# TODO update the JSON string below
json = "{}"
# create an instance of Candle from a JSON string
candle_instance = Candle.from_json(json)
# print the JSON string representation of the object
print(Candle.to_json())

# convert the object into a dict
candle_dict = candle_instance.to_dict()
# create an instance of Candle from a dict
candle_from_dict = Candle.from_dict(candle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


