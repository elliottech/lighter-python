# Referral


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**l1_address** | **str** |  | 
**referral_code** | **str** |  | 
**used_at** | **int** |  | 
**trade_stats** | [**TradeStats**](TradeStats.md) |  | 

## Example

```python
from lighter.models.referral import Referral

# TODO update the JSON string below
json = "{}"
# create an instance of Referral from a JSON string
referral_instance = Referral.from_json(json)
# print the JSON string representation of the object
print(Referral.to_json())

# convert the object into a dict
referral_dict = referral_instance.to_dict()
# create an instance of Referral from a dict
referral_from_dict = Referral.from_dict(referral_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


