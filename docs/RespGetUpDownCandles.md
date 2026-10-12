# RespGetUpDownCandles


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**candles** | [**List[UpDownCandle]**](UpDownCandle.md) |  ascending by timestamp | 
**next_cursor** | **int** |  start_timestamp of the next page; 0 when the range is exhausted | [optional] 

## Example

```python
from lighter.models.resp_get_up_down_candles import RespGetUpDownCandles

# TODO update the JSON string below
json = "{}"
# create an instance of RespGetUpDownCandles from a JSON string
resp_get_up_down_candles_instance = RespGetUpDownCandles.from_json(json)
# print the JSON string representation of the object
print(RespGetUpDownCandles.to_json())

# convert the object into a dict
resp_get_up_down_candles_dict = resp_get_up_down_candles_instance.to_dict()
# create an instance of RespGetUpDownCandles from a dict
resp_get_up_down_candles_from_dict = RespGetUpDownCandles.from_dict(resp_get_up_down_candles_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


