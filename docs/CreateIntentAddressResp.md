# CreateIntentAddressResp


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**intent_address** | **str** |  | 

## Example

```python
from lighter.models.create_intent_address_resp import CreateIntentAddressResp

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIntentAddressResp from a JSON string
create_intent_address_resp_instance = CreateIntentAddressResp.from_json(json)
# print the JSON string representation of the object
print(CreateIntentAddressResp.to_json())

# convert the object into a dict
create_intent_address_resp_dict = create_intent_address_resp_instance.to_dict()
# create an instance of CreateIntentAddressResp from a dict
create_intent_address_resp_from_dict = CreateIntentAddressResp.from_dict(create_intent_address_resp_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


