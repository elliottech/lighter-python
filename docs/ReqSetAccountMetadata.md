# ReqSetAccountMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**master_account_index** | **int** |  | 
**target_account_index** | **int** |  | 
**api_key_index** | **int** |  | 
**metadata** | **str** |  | 
**auth** | **str** |  | [optional] 

## Example

```python
from lighter.models.req_set_account_metadata import ReqSetAccountMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ReqSetAccountMetadata from a JSON string
req_set_account_metadata_instance = ReqSetAccountMetadata.from_json(json)
# print the JSON string representation of the object
print(ReqSetAccountMetadata.to_json())

# convert the object into a dict
req_set_account_metadata_dict = req_set_account_metadata_instance.to_dict()
# create an instance of ReqSetAccountMetadata from a dict
req_set_account_metadata_from_dict = ReqSetAccountMetadata.from_dict(req_set_account_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


