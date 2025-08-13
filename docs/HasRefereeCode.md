# HasRefereeCode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**has_referee** | **bool** |  | 

## Example

```python
from lighter.models.has_referee_code import HasRefereeCode

# TODO update the JSON string below
json = "{}"
# create an instance of HasRefereeCode from a JSON string
has_referee_code_instance = HasRefereeCode.from_json(json)
# print the JSON string representation of the object
print(HasRefereeCode.to_json())

# convert the object into a dict
has_referee_code_dict = has_referee_code_instance.to_dict()
# create an instance of HasRefereeCode from a dict
has_referee_code_from_dict = HasRefereeCode.from_dict(has_referee_code_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


