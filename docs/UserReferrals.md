# UserReferrals


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**cursor** | **str** |  | 
**referrals** | [**List[Referral]**](Referral.md) |  | 
**used_code** | **str** |  | 

## Example

```python
from lighter.models.user_referrals import UserReferrals

# TODO update the JSON string below
json = "{}"
# create an instance of UserReferrals from a JSON string
user_referrals_instance = UserReferrals.from_json(json)
# print the JSON string representation of the object
print(UserReferrals.to_json())

# convert the object into a dict
user_referrals_dict = user_referrals_instance.to_dict()
# create an instance of UserReferrals from a dict
user_referrals_from_dict = UserReferrals.from_dict(user_referrals_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


