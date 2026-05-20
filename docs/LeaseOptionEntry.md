# LeaseOptionEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**duration_days** | **int** | Lease duration in days | 
**annual_rate** | **float** | Annual rate as a percentage (e.g. 25.0 means 25%) | 

## Example

```python
from lighter.models.lease_option_entry import LeaseOptionEntry

# TODO update the JSON string below
json = "{}"
# create an instance of LeaseOptionEntry from a JSON string
lease_option_entry_instance = LeaseOptionEntry.from_json(json)
# print the JSON string representation of the object
print(LeaseOptionEntry.to_json())

# convert the object into a dict
lease_option_entry_dict = lease_option_entry_instance.to_dict()
# create an instance of LeaseOptionEntry from a dict
lease_option_entry_from_dict = LeaseOptionEntry.from_dict(lease_option_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


