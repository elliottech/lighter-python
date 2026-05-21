# RFQResponseEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_index** | **int** |  | 
**status** | **str** |  | 
**responded_at** | **int** |  | 
**updated_at** | **int** |  | 

## Example

```python
from lighter.models.rfq_response_entry import RFQResponseEntry

# TODO update the JSON string below
json = "{}"
# create an instance of RFQResponseEntry from a JSON string
rfq_response_entry_instance = RFQResponseEntry.from_json(json)
# print the JSON string representation of the object
print(RFQResponseEntry.to_json())

# convert the object into a dict
rfq_response_entry_dict = rfq_response_entry_instance.to_dict()
# create an instance of RFQResponseEntry from a dict
rfq_response_entry_from_dict = RFQResponseEntry.from_dict(rfq_response_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


