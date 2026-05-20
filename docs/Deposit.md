# Deposit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**source** | **str** |  | 
**source_chain_id** | **str** |  | 
**fast_bridge_tx_hash** | **str** |  | 
**batch_claim_tx_hash** | **str** |  | 
**cctp_burn_tx_hash** | **str** |  | 
**amount** | **str** |  | 
**intent_address** | **str** |  | 
**status** | **str** |  | 
**step** | **str** |  | 
**description** | **str** |  | 
**created_at** | **int** |  | 
**updated_at** | **int** |  | 
**is_external_deposit** | **bool** |  | 
**is_next_bridge_fast** | **bool** |  | 

## Example

```python
from lighter.models.deposit import Deposit

# TODO update the JSON string below
json = "{}"
# create an instance of Deposit from a JSON string
deposit_instance = Deposit.from_json(json)
# print the JSON string representation of the object
print(Deposit.to_json())

# convert the object into a dict
deposit_dict = deposit_instance.to_dict()
# create an instance of Deposit from a dict
deposit_from_dict = Deposit.from_dict(deposit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


