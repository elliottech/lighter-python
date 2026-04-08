# ReqGetPartnerStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_index** | **int** |  | 
**start_timestamp** | **int** |  | [optional] 
**end_timestamp** | **int** |  | [optional] 

## Example

```python
from lighter.models.req_get_partner_stats import ReqGetPartnerStats

# TODO update the JSON string below
json = "{}"
# create an instance of ReqGetPartnerStats from a JSON string
req_get_partner_stats_instance = ReqGetPartnerStats.from_json(json)
# print the JSON string representation of the object
print(ReqGetPartnerStats.to_json())

# convert the object into a dict
req_get_partner_stats_dict = req_get_partner_stats_instance.to_dict()
# create an instance of ReqGetPartnerStats from a dict
req_get_partner_stats_from_dict = ReqGetPartnerStats.from_dict(req_get_partner_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


