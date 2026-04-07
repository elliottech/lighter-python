# RespGetMakerOnlyApiKeys


## Properties

Name | Type          | Description | Notes
------------ |---------------| ------------- | -------------
**code** | **int**       |  | 
**message** | **str**       |  | [optional] 
**api_key_indexes** | **List[int]** |  | 

## Example

```python
from lighter.models.resp_get_maker_only_api_keys import RespGetMakerOnlyApiKeys

# TODO update the JSON string below
json = "{}"
# create an instance of RespGetMakerOnlyApiKeys from a JSON string
resp_get_maker_only_api_keys_instance = RespGetMakerOnlyApiKeys.from_json(json)
# print the JSON string representation of the object
print(RespGetMakerOnlyApiKeys.to_json())

# convert the object into a dict
resp_get_maker_only_api_keys_dict = resp_get_maker_only_api_keys_instance.to_dict()
# create an instance of RespGetMakerOnlyApiKeys from a dict
resp_get_maker_only_api_keys_from_dict = RespGetMakerOnlyApiKeys.from_dict(resp_get_maker_only_api_keys_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


