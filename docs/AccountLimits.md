# AccountLimits


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**max_llp_percentage** | **int** |  | 
**user_tier** | **str** |  | 
**can_create_public_pool** | **bool** |  | 
**max_llp_amount** | **str** |  | 
**current_maker_fee_tick** | **int** |  | 
**current_taker_fee_tick** | **int** |  | 
**effective_lit_stakes** | **str** | Effective staked LIT shares including active leases. | 
**leased_lit** | **str** | Total actively leased LIT. | 
**user_tier_name** | **str** |  | 
**user_tier_last_update** | **int** |  | [optional] 

## Example

```python
from lighter.models.account_limits import AccountLimits

# TODO update the JSON string below
json = "{}"
# create an instance of AccountLimits from a JSON string
account_limits_instance = AccountLimits.from_json(json)
# print the JSON string representation of the object
print(AccountLimits.to_json())

# convert the object into a dict
account_limits_dict = account_limits_instance.to_dict()
# create an instance of AccountLimits from a dict
account_limits_from_dict = AccountLimits.from_dict(account_limits_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


