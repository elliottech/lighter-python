# RespRespondToRFQ


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
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
from lighter.models.resp_respond_to_rfq import RespRespondToRFQ

# TODO update the JSON string below
json = "{}"
# create an instance of RespRespondToRFQ from a JSON string
resp_respond_to_rfq_instance = RespRespondToRFQ.from_json(json)
# print the JSON string representation of the object
print(RespRespondToRFQ.to_json())

# convert the object into a dict
resp_respond_to_rfq_dict = resp_respond_to_rfq_instance.to_dict()
# create an instance of RespRespondToRFQ from a dict
resp_respond_to_rfq_from_dict = RespRespondToRFQ.from_dict(resp_respond_to_rfq_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


