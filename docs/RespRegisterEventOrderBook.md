# RespRegisterEventOrderBook


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**success** | **bool** |  | 

## Example

```python
from lighter.models.resp_register_event_order_book import RespRegisterEventOrderBook

# TODO update the JSON string below
json = "{}"
# create an instance of RespRegisterEventOrderBook from a JSON string
resp_register_event_order_book_instance = RespRegisterEventOrderBook.from_json(json)
# print the JSON string representation of the object
print(RespRegisterEventOrderBook.to_json())

# convert the object into a dict
resp_register_event_order_book_dict = resp_register_event_order_book_instance.to_dict()
# create an instance of RespRegisterEventOrderBook from a dict
resp_register_event_order_book_from_dict = RespRegisterEventOrderBook.from_dict(resp_register_event_order_book_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


