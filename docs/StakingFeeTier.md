# StakingFeeTier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**required_lit_stakes** | **int** |  | 
**fee_rate** | **float** |  | 

## Example

```python
from lighter.models.staking_fee_tier import StakingFeeTier

# TODO update the JSON string below
json = "{}"
# create an instance of StakingFeeTier from a JSON string
staking_fee_tier_instance = StakingFeeTier.from_json(json)
# print the JSON string representation of the object
print(StakingFeeTier.to_json())

# convert the object into a dict
staking_fee_tier_dict = staking_fee_tier_instance.to_dict()
# create an instance of StakingFeeTier from a dict
staking_fee_tier_from_dict = StakingFeeTier.from_dict(staking_fee_tier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


