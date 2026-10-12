# lighter.EventApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**events**](EventApi.md#events) | **GET** /api/v1/events | events


# **events**
> RespGetEvents events(event_ids=event_ids, market_ids=market_ids, creator_account_index=creator_account_index, cursor=cursor, active=active, limit=limit, tag=tag, event_kind=event_kind, start_from=start_from, start_before=start_before, sort=sort, order=order)

events

Get events and registered order books, including scheduled events with no books. event_ids and market_ids accept up to 50 comma-separated positive IDs, are mutually exclusive, and use the same filters, sorting and pagination. market_ids returns each related event once with all its order books. Defaults to descending id. Occurrence sorting uses (occurrence_start_at, event_id); cursor identifies an existing event and excludes it in the requested direction. tag filters across creators; creator_account_index is an optional additional filter. active=true requires a tradeable outcome; active=false includes scheduled and closed events.

### Example


```python
import lighter
from lighter.models.resp_get_events import RespGetEvents
from lighter.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://mainnet.zklighter.elliot.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = lighter.Configuration(
    host = "https://mainnet.zklighter.elliot.ai"
)


# Enter a context with an instance of the API client
async with lighter.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = lighter.EventApi(api_client)
    event_ids = 'event_ids_example' # str |  comma-separated positive IDs, max 50 (optional)
    market_ids = 'market_ids_example' # str |  comma-separated positive IDs, max 50 (optional)
    creator_account_index = 56 # int |  (optional)
    cursor = 56 # int |  (optional)
    active = True # bool |  true: at least one outcome still tradeable; false: none (optional)
    limit = 56 # int |  (optional)
    tag = 'tag_example' # str |  series tag; creator filter is optional (optional)
    event_kind = 'event_kind_example' # str |  (optional)
    start_from = 56 # int |  inclusive occurrence start, Unix milliseconds (optional)
    start_before = 56 # int |  exclusive occurrence start, Unix milliseconds (optional)
    sort = id # str |  (optional) (default to id)
    order = desc # str |  (optional) (default to desc)

    try:
        # events
        api_response = await api_instance.events(event_ids=event_ids, market_ids=market_ids, creator_account_index=creator_account_index, cursor=cursor, active=active, limit=limit, tag=tag, event_kind=event_kind, start_from=start_from, start_before=start_before, sort=sort, order=order)
        print("The response of EventApi->events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event_ids** | **str**|  comma-separated positive IDs, max 50 | [optional] 
 **market_ids** | **str**|  comma-separated positive IDs, max 50 | [optional] 
 **creator_account_index** | **int**|  | [optional] 
 **cursor** | **int**|  | [optional] 
 **active** | **bool**|  true: at least one outcome still tradeable; false: none | [optional] 
 **limit** | **int**|  | [optional] 
 **tag** | **str**|  series tag; creator filter is optional | [optional] 
 **event_kind** | **str**|  | [optional] 
 **start_from** | **int**|  inclusive occurrence start, Unix milliseconds | [optional] 
 **start_before** | **int**|  exclusive occurrence start, Unix milliseconds | [optional] 
 **sort** | **str**|  | [optional] [default to id]
 **order** | **str**|  | [optional] [default to desc]

### Return type

[**RespGetEvents**](RespGetEvents.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

