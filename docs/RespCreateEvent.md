# RespCreateEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**event_id** | **int** |  | 

## Example

```python
from lighter.models.resp_create_event import RespCreateEvent

# TODO update the JSON string below
json = "{}"
# create an instance of RespCreateEvent from a JSON string
resp_create_event_instance = RespCreateEvent.from_json(json)
# print the JSON string representation of the object
print(RespCreateEvent.to_json())

# convert the object into a dict
resp_create_event_dict = resp_create_event_instance.to_dict()
# create an instance of RespCreateEvent from a dict
resp_create_event_from_dict = RespCreateEvent.from_dict(resp_create_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


