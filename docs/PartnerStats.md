# PartnerStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**total_fees_earned** | **str** |  | 
**total_taker_fees_earned** | **str** |  | 
**total_maker_fees_earned** | **str** |  | 
**total_volume** | **str** |  | 
**total_taker_volume** | **str** |  | 
**total_maker_volume** | **str** |  | 
**total_trades** | **int** |  | 
**total_taker_trades** | **int** |  | 
**total_maker_trades** | **int** |  | 
**unique_clients** | **int** |  | 

## Example

```python
from lighter.models.partner_stats import PartnerStats

# TODO update the JSON string below
json = "{}"
# create an instance of PartnerStats from a JSON string
partner_stats_instance = PartnerStats.from_json(json)
# print the JSON string representation of the object
print(PartnerStats.to_json())

# convert the object into a dict
partner_stats_dict = partner_stats_instance.to_dict()
# create an instance of PartnerStats from a dict
partner_stats_from_dict = PartnerStats.from_dict(partner_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


