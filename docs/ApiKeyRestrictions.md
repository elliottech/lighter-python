# ApiKeyRestrictions

Returned only when the request carries auth for the account. A key without restrictions returns empty lists and valid_until 0.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**market_ids** | **List[int]** | Public market ids the key may trade. Empty, with series also empty, means no market whitelist. | 
**series** | [**List[ApiKeySeries]**](ApiKeySeries.md) | Market series the key may trade, in addition to market_ids. | 
**allowed_ips** | **List[str]** | IP addresses the key may be used from. Empty allows any IP. | 
**valid_until** | **int** | Unix seconds when the key expires. 0 means no expiry. | 

## Example

```python
from lighter.models.api_key_restrictions import ApiKeyRestrictions

# TODO update the JSON string below
json = "{}"
# create an instance of ApiKeyRestrictions from a JSON string
api_key_restrictions_instance = ApiKeyRestrictions.from_json(json)
# print the JSON string representation of the object
print(ApiKeyRestrictions.to_json())

# convert the object into a dict
api_key_restrictions_dict = api_key_restrictions_instance.to_dict()
# create an instance of ApiKeyRestrictions from a dict
api_key_restrictions_from_dict = ApiKeyRestrictions.from_dict(api_key_restrictions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


