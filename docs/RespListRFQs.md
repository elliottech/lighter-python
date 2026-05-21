# RespListRFQs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**rfqs** | [**List[RFQEntry]**](RFQEntry.md) |  | 
**next_cursor** | **str** |  | [optional] 

## Example

```python
from lighter.models.resp_list_rfqs import RespListRFQs

# TODO update the JSON string below
json = "{}"
# create an instance of RespListRFQs from a JSON string
resp_list_rfqs_instance = RespListRFQs.from_json(json)
# print the JSON string representation of the object
print(RespListRFQs.to_json())

# convert the object into a dict
resp_list_rfqs_dict = resp_list_rfqs_instance.to_dict()
# create an instance of RespListRFQs from a dict
resp_list_rfqs_from_dict = RespListRFQs.from_dict(resp_list_rfqs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


