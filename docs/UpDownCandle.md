# UpDownCandle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** |  | 
**duration** | **str** |  | 
**resolution** | **str** |  | 
**timestamp** | **int** |  bucket start, unix seconds | 
**open** | **str** |  exact provider prices, decimal strings | 
**high** | **str** |  | 
**low** | **str** |  | 
**close** | **str** |  | 
**sample_count** | **int** |  observations in the candle: orders live updates of the same bucket, not served | 
**provider** | **str** |  provider feed of the last observation of the candle | 
**feed_id** | **str** |  | 

## Example

```python
from lighter.models.up_down_candle import UpDownCandle

# TODO update the JSON string below
json = "{}"
# create an instance of UpDownCandle from a JSON string
up_down_candle_instance = UpDownCandle.from_json(json)
# print the JSON string representation of the object
print(UpDownCandle.to_json())

# convert the object into a dict
up_down_candle_dict = up_down_candle_instance.to_dict()
# create an instance of UpDownCandle from a dict
up_down_candle_from_dict = UpDownCandle.from_dict(up_down_candle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


