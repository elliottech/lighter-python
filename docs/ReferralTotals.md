# ReferralTotals


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**volume** | **str** |  | 
**free_maker_volume** | **str** |  | 
**free_taker_volume** | **str** |  | 
**non_free_maker_volume** | **str** |  | 
**non_free_taker_volume** | **str** |  | 
**maker_fees_paid** | **str** |  | 
**taker_fees_paid** | **str** |  | 
**total_referrals** | **int** |  | 
**total_premium_referrals** | **int** |  | 

## Example

```python
from lighter.models.referral_totals import ReferralTotals

# TODO update the JSON string below
json = "{}"
# create an instance of ReferralTotals from a JSON string
referral_totals_instance = ReferralTotals.from_json(json)
# print the JSON string representation of the object
print(ReferralTotals.to_json())

# convert the object into a dict
referral_totals_dict = referral_totals_instance.to_dict()
# create an instance of ReferralTotals from a dict
referral_totals_from_dict = ReferralTotals.from_dict(referral_totals_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


