# EventDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_id** | **int** |  | 
**title** | **str** |  | 
**description** | **str** |  | 
**creator_account_index** | **int** |  | 
**created_at** | **int** |  | 
**tag** | **str** |  | 
**event_kind** | **str** |  | 
**recurrence_period_seconds** | **int** |  | 
**occurrence_start_at** | **int** |  | 
**occurrence_end_at** | **int** |  | 
**metadata** | **Dict[str, object]** |  | 
**order_books** | [**List[EventOrderBookEntry]**](EventOrderBookEntry.md) |  | 
**lifetime_quote_token_volume** | **float** |  | 

## Example

```python
from lighter.models.event_detail import EventDetail

# TODO update the JSON string below
json = "{}"
# create an instance of EventDetail from a JSON string
event_detail_instance = EventDetail.from_json(json)
# print the JSON string representation of the object
print(EventDetail.to_json())

# convert the object into a dict
event_detail_dict = event_detail_instance.to_dict()
# create an instance of EventDetail from a dict
event_detail_from_dict = EventDetail.from_dict(event_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


