# RespGetEvents


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**next_cursor** | **int** |  | [optional] 
**events** | [**List[EventDetail]**](EventDetail.md) |  | 

## Example

```python
from lighter.models.resp_get_events import RespGetEvents

# TODO update the JSON string below
json = "{}"
# create an instance of RespGetEvents from a JSON string
resp_get_events_instance = RespGetEvents.from_json(json)
# print the JSON string representation of the object
print(RespGetEvents.to_json())

# convert the object into a dict
resp_get_events_dict = resp_get_events_instance.to_dict()
# create an instance of RespGetEvents from a dict
resp_get_events_from_dict = RespGetEvents.from_dict(resp_get_events_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


