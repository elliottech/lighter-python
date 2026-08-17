# ReferralProgramKickback


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **int** |  | 
**percentage** | **str** |  | 

## Example

```python
from lighter.models.referral_program_kickback import ReferralProgramKickback

# TODO update the JSON string below
json = "{}"
# create an instance of ReferralProgramKickback from a JSON string
referral_program_kickback_instance = ReferralProgramKickback.from_json(json)
# print the JSON string representation of the object
print(ReferralProgramKickback.to_json())

# convert the object into a dict
referral_program_kickback_dict = referral_program_kickback_instance.to_dict()
# create an instance of ReferralProgramKickback from a dict
referral_program_kickback_from_dict = ReferralProgramKickback.from_dict(referral_program_kickback_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


