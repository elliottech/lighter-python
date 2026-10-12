# BoOutcomePnL


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**market_id** | **int** |  | 
**symbol** | **str** |  | 
**outcome** | **int** |  | 
**end_timestamp** | **int** |  | 
**settlement_pnl** | **str** |  | 
**last_trade_id** | **int** |  | 
**total_pnl** | **str** |  | 

## Example

```python
from lighter.models.bo_outcome_pn_l import BoOutcomePnL

# TODO update the JSON string below
json = "{}"
# create an instance of BoOutcomePnL from a JSON string
bo_outcome_pn_l_instance = BoOutcomePnL.from_json(json)
# print the JSON string representation of the object
print(BoOutcomePnL.to_json())

# convert the object into a dict
bo_outcome_pn_l_dict = bo_outcome_pn_l_instance.to_dict()
# create an instance of BoOutcomePnL from a dict
bo_outcome_pn_l_from_dict = BoOutcomePnL.from_dict(bo_outcome_pn_l_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


