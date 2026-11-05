# lighter.EventApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**event_create**](EventApi.md#event_create) | **POST** /api/v1/event/create | event_create
[**event_register_order_book**](EventApi.md#event_register_order_book) | **POST** /api/v1/event/registerOrderBook | event_registerOrderBook
[**event_update**](EventApi.md#event_update) | **POST** /api/v1/event/update | event_update
[**events**](EventApi.md#events) | **GET** /api/v1/events | events


# **event_create**
> RespCreateEvent event_create(authorization, account_index, title, start_at, end_at, description=description, tag=tag, event_kind=event_kind, recurrence_period_seconds=recurrence_period_seconds, metadata=metadata)

event_create

Create a binary options event

### Example


```python
import lighter
from lighter.models.resp_create_event import RespCreateEvent
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
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    title = 'title_example' # str | 
    start_at = 56 # int |  Unix milliseconds; observation time, not trading time
    end_at = 56 # int |  Unix milliseconds; must be after start_at
    description = 'description_example' # str |  (optional)
    tag = 'tag_example' # str |  series tag; may be shared by different creators (optional)
    event_kind = one_off # str |  (optional) (default to one_off)
    recurrence_period_seconds = 56 # int |  0 for one-off events (optional)
    metadata = 'metadata_example' # str |  JSON object, max 16 KiB; presentation only (optional)

    try:
        # event_create
        api_response = await api_instance.event_create(authorization, account_index, title, start_at, end_at, description=description, tag=tag, event_kind=event_kind, recurrence_period_seconds=recurrence_period_seconds, metadata=metadata)
        print("The response of EventApi->event_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **title** | **str**|  | 
 **start_at** | **int**|  Unix milliseconds; observation time, not trading time | 
 **end_at** | **int**|  Unix milliseconds; must be after start_at | 
 **description** | **str**|  | [optional] 
 **tag** | **str**|  series tag; may be shared by different creators | [optional] 
 **event_kind** | **str**|  | [optional] [default to one_off]
 **recurrence_period_seconds** | **int**|  0 for one-off events | [optional] 
 **metadata** | **str**|  JSON object, max 16 KiB; presentation only | [optional] 

### Return type

[**RespCreateEvent**](RespCreateEvent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_register_order_book**
> RespRegisterEventOrderBook event_register_order_book(authorization, account_index, event_id, market_index)

event_registerOrderBook

Register an already deployed order book to an event

### Example


```python
import lighter
from lighter.models.resp_register_event_order_book import RespRegisterEventOrderBook
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
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    event_id = 56 # int | 
    market_index = 56 # int | 

    try:
        # event_registerOrderBook
        api_response = await api_instance.event_register_order_book(authorization, account_index, event_id, market_index)
        print("The response of EventApi->event_register_order_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_register_order_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **event_id** | **int**|  | 
 **market_index** | **int**|  | 

### Return type

[**RespRegisterEventOrderBook**](RespRegisterEventOrderBook.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_update**
> ResultCode event_update(authorization, account_index, title, start_at, end_at, event_id, description=description, tag=tag, event_kind=event_kind, recurrence_period_seconds=recurrence_period_seconds, metadata=metadata)

event_update

Replace event details as its creator; rejected while any attached unsettled market is within its trading window. Market bindings are unchanged.

### Example


```python
import lighter
from lighter.models.result_code import ResultCode
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
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    title = 'title_example' # str | 
    start_at = 56 # int |  Unix milliseconds; observation time, not trading time
    end_at = 56 # int |  Unix milliseconds; must be after start_at
    event_id = 56 # int | 
    description = 'description_example' # str |  (optional)
    tag = 'tag_example' # str |  series tag; may be shared by different creators (optional)
    event_kind = one_off # str |  (optional) (default to one_off)
    recurrence_period_seconds = 56 # int |  0 for one-off events (optional)
    metadata = 'metadata_example' # str |  JSON object, max 16 KiB; presentation only (optional)

    try:
        # event_update
        api_response = await api_instance.event_update(authorization, account_index, title, start_at, end_at, event_id, description=description, tag=tag, event_kind=event_kind, recurrence_period_seconds=recurrence_period_seconds, metadata=metadata)
        print("The response of EventApi->event_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **title** | **str**|  | 
 **start_at** | **int**|  Unix milliseconds; observation time, not trading time | 
 **end_at** | **int**|  Unix milliseconds; must be after start_at | 
 **event_id** | **int**|  | 
 **description** | **str**|  | [optional] 
 **tag** | **str**|  series tag; may be shared by different creators | [optional] 
 **event_kind** | **str**|  | [optional] [default to one_off]
 **recurrence_period_seconds** | **int**|  0 for one-off events | [optional] 
 **metadata** | **str**|  JSON object, max 16 KiB; presentation only | [optional] 

### Return type

[**ResultCode**](ResultCode.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **events**
> RespGetEvents events(event_ids=event_ids, market_ids=market_ids, creator_account_index=creator_account_index, cursor=cursor, active=active, limit=limit, tag=tag, event_kind=event_kind, start_from=start_from, start_before=start_before, sort=sort, order=order)

events

Get events and registered order books, including scheduled events with no books. event_ids and market_ids accept up to 50 comma-separated positive IDs, are mutually exclusive, and use the same filters, sorting and pagination. market_ids returns each related event once with all its order books. Defaults to descending id. start_at sorting uses (start_at, event_id); cursor identifies an existing event and excludes it in the requested direction. tag filters across creators; creator_account_index is an optional additional filter. active=true requires a tradeable outcome; active=false includes scheduled and closed events.

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
    start_from = 56 # int |  inclusive start_at, Unix milliseconds (optional)
    start_before = 56 # int |  exclusive start_at, Unix milliseconds (optional)
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
 **start_from** | **int**|  inclusive start_at, Unix milliseconds | [optional] 
 **start_before** | **int**|  exclusive start_at, Unix milliseconds | [optional] 
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

