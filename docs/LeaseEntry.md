# LeaseEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Lease ID | 
**master_account_index** | **int** | Master account index | 
**lease_amount** | **int** | Leased LIT amount in raw units (1 LIT &#x3D; 1e8) | 
**fee_amount** | **int** | Fee paid in raw units | 
**start** | **int** | Lease start time (Unix milliseconds) | 
**end** | **int** | Lease end time (Unix milliseconds) | 
**status** | **str** | Lease status | 
**error** | **str** | Error message if lease was canceled | 

## Example

```python
from lighter.models.lease_entry import LeaseEntry

# TODO update the JSON string below
json = "{}"
# create an instance of LeaseEntry from a JSON string
lease_entry_instance = LeaseEntry.from_json(json)
# print the JSON string representation of the object
print(LeaseEntry.to_json())

# convert the object into a dict
lease_entry_dict = lease_entry_instance.to_dict()
# create an instance of LeaseEntry from a dict
lease_entry_from_dict = LeaseEntry.from_dict(lease_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


