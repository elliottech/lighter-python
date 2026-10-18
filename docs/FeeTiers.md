# FeeTiers


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_tiers** | [**List[UserFeeTier]**](UserFeeTier.md) |  | 
**bo_tiers** | [**List[BoFeeTier]**](BoFeeTier.md) |  | 
**staking_tiers** | [**List[StakingFeeTier]**](StakingFeeTier.md) |  | 

## Example

```python
from lighter.models.fee_tiers import FeeTiers

# TODO update the JSON string below
json = "{}"
# create an instance of FeeTiers from a JSON string
fee_tiers_instance = FeeTiers.from_json(json)
# print the JSON string representation of the object
print(FeeTiers.to_json())

# convert the object into a dict
fee_tiers_dict = fee_tiers_instance.to_dict()
# create an instance of FeeTiers from a dict
fee_tiers_from_dict = FeeTiers.from_dict(fee_tiers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


