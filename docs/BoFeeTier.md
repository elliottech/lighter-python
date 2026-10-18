# BoFeeTier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**required_volume** | **int** |  | 
**fee_rate** | **float** |  | 

## Example

```python
from lighter.models.bo_fee_tier import BoFeeTier

# TODO update the JSON string below
json = "{}"
# create an instance of BoFeeTier from a JSON string
bo_fee_tier_instance = BoFeeTier.from_json(json)
# print the JSON string representation of the object
print(BoFeeTier.to_json())

# convert the object into a dict
bo_fee_tier_dict = bo_fee_tier_instance.to_dict()
# create an instance of BoFeeTier from a dict
bo_fee_tier_from_dict = BoFeeTier.from_dict(bo_fee_tier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


