# RespGetLeases


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**leases** | [**List[LeaseEntry]**](LeaseEntry.md) |  | 
**next_cursor** | **str** | Cursor to pass as the cursor param to fetch the next page. Absent if no more pages. | [optional] 

## Example

```python
from lighter.models.resp_get_leases import RespGetLeases

# TODO update the JSON string below
json = "{}"
# create an instance of RespGetLeases from a JSON string
resp_get_leases_instance = RespGetLeases.from_json(json)
# print the JSON string representation of the object
print(RespGetLeases.to_json())

# convert the object into a dict
resp_get_leases_dict = resp_get_leases_instance.to_dict()
# create an instance of RespGetLeases from a dict
resp_get_leases_from_dict = RespGetLeases.from_dict(resp_get_leases_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


