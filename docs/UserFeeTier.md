# UserFeeTier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**level** | **int** |  | 
**maker_fee_ticks** | **int** |  | 
**taker_fee_ticks** | **int** |  | 
**required_lit_stakes** | **int** |  | 
**required_volume** | **int** |  | 

## Example

```python
from lighter.models.user_fee_tier import UserFeeTier

# TODO update the JSON string below
json = "{}"
# create an instance of UserFeeTier from a JSON string
user_fee_tier_instance = UserFeeTier.from_json(json)
# print the JSON string representation of the object
print(UserFeeTier.to_json())

# convert the object into a dict
user_fee_tier_dict = user_fee_tier_instance.to_dict()
# create an instance of UserFeeTier from a dict
user_fee_tier_from_dict = UserFeeTier.from_dict(user_fee_tier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


