# RFQMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requested_est_price** | **str** |  | 
**requested_max_slippage** | **str** |  | 
**requested_slippage** | **str** |  | 
**worst_price** | **str** |  | 

## Example

```python
from lighter.models.rfq_metadata import RFQMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of RFQMetadata from a JSON string
rfq_metadata_instance = RFQMetadata.from_json(json)
# print the JSON string representation of the object
print(RFQMetadata.to_json())

# convert the object into a dict
rfq_metadata_dict = rfq_metadata_instance.to_dict()
# create an instance of RFQMetadata from a dict
rfq_metadata_from_dict = RFQMetadata.from_dict(rfq_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


