# Token


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** |  | 
**name** | **str** |  | 
**logo** | **str** |  | 
**logo_extension** | **str** |  | 
**description_key** | **str** |  | 
**gecko_id** | **str** |  | 
**paprika_id** | **str** |  | 
**market** | **str** |  | 
**asset_type** | **str** |  | 
**categories** | **List[str]** |  | 
**is_allowed_mainnet** | **bool** |  | 
**is_asset_allowed_mainnet** | **bool** |  | 

## Example

```python
from lighter.models.token import Token

# TODO update the JSON string below
json = "{}"
# create an instance of Token from a JSON string
token_instance = Token.from_json(json)
# print the JSON string representation of the object
print(Token.to_json())

# convert the object into a dict
token_dict = token_instance.to_dict()
# create an instance of Token from a dict
token_from_dict = Token.from_dict(token_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


