# RespGetLeaseOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**options** | [**List[LeaseOptionEntry]**](LeaseOptionEntry.md) |  | 
**lit_incentives_account_index** | **int** | Account index that receives the leasing fee | 

## Example

```python
from lighter.models.resp_get_lease_options import RespGetLeaseOptions

# TODO update the JSON string below
json = "{}"
# create an instance of RespGetLeaseOptions from a JSON string
resp_get_lease_options_instance = RespGetLeaseOptions.from_json(json)
# print the JSON string representation of the object
print(RespGetLeaseOptions.to_json())

# convert the object into a dict
resp_get_lease_options_dict = resp_get_lease_options_instance.to_dict()
# create an instance of RespGetLeaseOptions from a dict
resp_get_lease_options_from_dict = RespGetLeaseOptions.from_dict(resp_get_lease_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


