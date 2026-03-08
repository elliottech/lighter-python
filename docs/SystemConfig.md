# SystemConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**liquidity_pool_index** | **int** |  | 
**staking_pool_index** | **int** |  | 
**funding_fee_rebate_account_index** | **int** |  | 
**liquidity_pool_cooldown_period** | **int** |  | 
**staking_pool_lockup_period** | **int** |  | 
**max_integrator_spot_taker_fee** | **int** |  | 
**max_integrator_spot_maker_fee** | **int** |  | 
**max_integrator_perps_taker_fee** | **int** |  | 
**max_integrator_perps_maker_fee** | **int** |  | 

## Example

```python
from lighter.models.system_config import SystemConfig

# TODO update the JSON string below
json = "{}"
# create an instance of SystemConfig from a JSON string
system_config_instance = SystemConfig.from_json(json)
# print the JSON string representation of the object
print(SystemConfig.to_json())

# convert the object into a dict
system_config_dict = system_config_instance.to_dict()
# create an instance of SystemConfig from a dict
system_config_from_dict = SystemConfig.from_dict(system_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


