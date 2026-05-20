# ReferralCode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**referral_code** | **str** |  | 
**remaining_usage** | **int** |  | 

## Example

```python
from lighter.models.referral_code import ReferralCode

# TODO update the JSON string below
json = "{}"
# create an instance of ReferralCode from a JSON string
referral_code_instance = ReferralCode.from_json(json)
# print the JSON string representation of the object
print(ReferralCode.to_json())

# convert the object into a dict
referral_code_dict = referral_code_instance.to_dict()
# create an instance of ReferralCode from a dict
referral_code_from_dict = ReferralCode.from_dict(referral_code_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


