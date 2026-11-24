# ApiKeySeries

A market series, such as binary options, identified by its creator and tag.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**creator_account_index** | **int** |  | 
**tag** | **str** |  | 

## Example

```python
from lighter.models.api_key_series import ApiKeySeries

# TODO update the JSON string below
json = "{}"
# create an instance of ApiKeySeries from a JSON string
api_key_series_instance = ApiKeySeries.from_json(json)
# print the JSON string representation of the object
print(ApiKeySeries.to_json())

# convert the object into a dict
api_key_series_dict = api_key_series_instance.to_dict()
# create an instance of ApiKeySeries from a dict
api_key_series_from_dict = ApiKeySeries.from_dict(api_key_series_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


