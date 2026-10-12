# RespGetBoPnL


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**events** | [**List[BoEventPnL]**](BoEventPnL.md) |  | 
**next_cursor** | **int** |  | [optional] 

## Example

```python
from lighter.models.resp_get_bo_pn_l import RespGetBoPnL

# TODO update the JSON string below
json = "{}"
# create an instance of RespGetBoPnL from a JSON string
resp_get_bo_pn_l_instance = RespGetBoPnL.from_json(json)
# print the JSON string representation of the object
print(RespGetBoPnL.to_json())

# convert the object into a dict
resp_get_bo_pn_l_dict = resp_get_bo_pn_l_instance.to_dict()
# create an instance of RespGetBoPnL from a dict
resp_get_bo_pn_l_from_dict = RespGetBoPnL.from_dict(resp_get_bo_pn_l_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


