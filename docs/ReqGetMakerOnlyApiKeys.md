# ReqGetMakerOnlyApiKeys


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth** | **str** |  | [optional] 
**account_index** | **int** |  | 

## Example

```python
from lighter.models.req_get_maker_only_api_keys import ReqGetMakerOnlyApiKeys

# TODO update the JSON string below
json = "{}"
# create an instance of ReqGetMakerOnlyApiKeys from a JSON string
req_get_maker_only_api_keys_instance = ReqGetMakerOnlyApiKeys.from_json(json)
# print the JSON string representation of the object
print(ReqGetMakerOnlyApiKeys.to_json())

# convert the object into a dict
req_get_maker_only_api_keys_dict = req_get_maker_only_api_keys_instance.to_dict()
# create an instance of ReqGetMakerOnlyApiKeys from a dict
req_get_maker_only_api_keys_from_dict = ReqGetMakerOnlyApiKeys.from_dict(req_get_maker_only_api_keys_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


