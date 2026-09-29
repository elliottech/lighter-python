# ReferralStat


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_timestamp** | **int** |  | 
**end_timestamp** | **int** |  | 
**trade_stats** | [**TradeStats**](TradeStats.md) |  | 

## Example

```python
from lighter.models.referral_stat import ReferralStat

# TODO update the JSON string below
json = "{}"
# create an instance of ReferralStat from a JSON string
referral_stat_instance = ReferralStat.from_json(json)
# print the JSON string representation of the object
print(ReferralStat.to_json())

# convert the object into a dict
referral_stat_dict = referral_stat_instance.to_dict()
# create an instance of ReferralStat from a dict
referral_stat_from_dict = ReferralStat.from_dict(referral_stat_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


