# ReferralStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**stats** | [**List[ReferralStat]**](ReferralStat.md) |  | 

## Example

```python
from lighter.models.referral_stats import ReferralStats

# TODO update the JSON string below
json = "{}"
# create an instance of ReferralStats from a JSON string
referral_stats_instance = ReferralStats.from_json(json)
# print the JSON string representation of the object
print(ReferralStats.to_json())

# convert the object into a dict
referral_stats_dict = referral_stats_instance.to_dict()
# create an instance of ReferralStats from a dict
referral_stats_from_dict = ReferralStats.from_dict(referral_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


