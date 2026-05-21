# RFQEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**account_index** | **int** |  | 
**market_index** | **int** |  | 
**direction** | **int** |  | 
**base_amount** | **str** |  | 
**quote_amount** | **str** |  | 
**status** | **str** |  | 
**metadata** | [**RFQMetadata**](RFQMetadata.md) |  | 
**responses** | [**List[RFQResponseEntry]**](RFQResponseEntry.md) |  | 
**created_at** | **int** |  | 
**updated_at** | **int** |  | 

## Example

```python
from lighter.models.rfq_entry import RFQEntry

# TODO update the JSON string below
json = "{}"
# create an instance of RFQEntry from a JSON string
rfq_entry_instance = RFQEntry.from_json(json)
# print the JSON string representation of the object
print(RFQEntry.to_json())

# convert the object into a dict
rfq_entry_dict = rfq_entry_instance.to_dict()
# create an instance of RFQEntry from a dict
rfq_entry_from_dict = RFQEntry.from_dict(rfq_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


