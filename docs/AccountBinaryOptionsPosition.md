# AccountBinaryOptionsPosition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**market_id** | **int** |  | 
**entry_quote** | **str** |  | 
**avg_entry_price** | **str** |  average price paid for the held outcome (YES price for sign 1, NO price for sign -1) | 
**sign** | **int** |  1 holds the YES outcome, -1 holds the NO outcome | 
**size** | **str** |  magnitude only; combine with sign | 

## Example

```python
from lighter.models.account_binary_options_position import AccountBinaryOptionsPosition

# TODO update the JSON string below
json = "{}"
# create an instance of AccountBinaryOptionsPosition from a JSON string
account_binary_options_position_instance = AccountBinaryOptionsPosition.from_json(json)
# print the JSON string representation of the object
print(AccountBinaryOptionsPosition.to_json())

# convert the object into a dict
account_binary_options_position_dict = account_binary_options_position_instance.to_dict()
# create an instance of AccountBinaryOptionsPosition from a dict
account_binary_options_position_from_dict = AccountBinaryOptionsPosition.from_dict(account_binary_options_position_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


