# BoEventPnL


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_id** | **int** |  | 
**event_title** | **str** |  | 
**event_description** | **str** |  | 
**total_pnl** | **str** |  | 
**outcomes** | [**List[BoOutcomePnL]**](BoOutcomePnL.md) |  | 

## Example

```python
from lighter.models.bo_event_pn_l import BoEventPnL

# TODO update the JSON string below
json = "{}"
# create an instance of BoEventPnL from a JSON string
bo_event_pn_l_instance = BoEventPnL.from_json(json)
# print the JSON string representation of the object
print(BoEventPnL.to_json())

# convert the object into a dict
bo_event_pn_l_dict = bo_event_pn_l_instance.to_dict()
# create an instance of BoEventPnL from a dict
bo_event_pn_l_from_dict = BoEventPnL.from_dict(bo_event_pn_l_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


