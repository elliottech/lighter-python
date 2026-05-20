# lighter.OrderApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**account_active_orders**](OrderApi.md#account_active_orders) | **GET** /api/v1/accountActiveOrders | accountActiveOrders
[**account_inactive_orders**](OrderApi.md#account_inactive_orders) | **GET** /api/v1/accountInactiveOrders | accountInactiveOrders
[**asset_details**](OrderApi.md#asset_details) | **GET** /api/v1/assetDetails | assetDetails
[**exchange_metrics**](OrderApi.md#exchange_metrics) | **GET** /api/v1/exchangeMetrics | exchangeMetrics
[**exchange_stats**](OrderApi.md#exchange_stats) | **GET** /api/v1/exchangeStats | exchangeStats
[**execute_stats**](OrderApi.md#execute_stats) | **GET** /api/v1/executeStats | executeStats
[**export**](OrderApi.md#export) | **GET** /api/v1/export | export
[**order_book_details**](OrderApi.md#order_book_details) | **GET** /api/v1/orderBookDetails | orderBookDetails
[**order_book_orders**](OrderApi.md#order_book_orders) | **GET** /api/v1/orderBookOrders | orderBookOrders
[**order_books**](OrderApi.md#order_books) | **GET** /api/v1/orderBooks | orderBooks
[**recent_trades**](OrderApi.md#recent_trades) | **GET** /api/v1/recentTrades | recentTrades
[**trades**](OrderApi.md#trades) | **GET** /api/v1/trades | trades


# **account_active_orders**
> Orders account_active_orders(authorization, account_index, market_id=market_id, market_type=market_type)

accountActiveOrders

Get account active orders. `auth` can be generated using the SDK.

### Example


```python
import lighter
from lighter.models.orders import Orders
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
    api_instance = lighter.OrderApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    market_id = 56 # int | If not specified, returns active orders for all markets. (optional)
    market_type = all # str |  (optional) (default to all)

    try:
        # accountActiveOrders
        api_response = await api_instance.account_active_orders(authorization, account_index, market_id=market_id, market_type=market_type)
        print("The response of OrderApi->account_active_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->account_active_orders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **market_id** | **int**| If not specified, returns active orders for all markets. | [optional] 
 **market_type** | **str**|  | [optional] [default to all]

### Return type

[**Orders**](Orders.md)

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

# **account_inactive_orders**
> Orders account_inactive_orders(authorization, account_index, limit, market_id=market_id, ask_filter=ask_filter, between_timestamps=between_timestamps, cursor=cursor, market_type=market_type)

accountInactiveOrders

Get account inactive orders. `auth` can be generated using the SDK.

### Example


```python
import lighter
from lighter.models.orders import Orders
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
    api_instance = lighter.OrderApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    limit = 56 # int | 
    market_id = 56 # int |  (optional)
    ask_filter = 56 # int |  (optional)
    between_timestamps = 'between_timestamps_example' # str |  (optional)
    cursor = 'cursor_example' # str |  (optional)
    market_type = all # str |  (optional) (default to all)

    try:
        # accountInactiveOrders
        api_response = await api_instance.account_inactive_orders(authorization, account_index, limit, market_id=market_id, ask_filter=ask_filter, between_timestamps=between_timestamps, cursor=cursor, market_type=market_type)
        print("The response of OrderApi->account_inactive_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->account_inactive_orders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **limit** | **int**|  | 
 **market_id** | **int**|  | [optional] 
 **ask_filter** | **int**|  | [optional] 
 **between_timestamps** | **str**|  | [optional] 
 **cursor** | **str**|  | [optional] 
 **market_type** | **str**|  | [optional] [default to all]

### Return type

[**Orders**](Orders.md)

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

# **asset_details**
> AssetDetails asset_details(asset_id=asset_id)

assetDetails

Get asset details for a specific asset or all assets

### Example


```python
import lighter
from lighter.models.asset_details import AssetDetails
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
    api_instance = lighter.OrderApi(api_client)
    asset_id = 56 # int |  (optional)

    try:
        # assetDetails
        api_response = await api_instance.asset_details(asset_id=asset_id)
        print("The response of OrderApi->asset_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->asset_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**|  | [optional] 

### Return type

[**AssetDetails**](AssetDetails.md)

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

# **exchange_metrics**
> RespGetExchangeMetrics exchange_metrics(period, kind, filter=filter, value=value)

exchangeMetrics

Get exchange metrics. When filtering by market, use the market symbol as a value.

### Example


```python
import lighter
from lighter.models.resp_get_exchange_metrics import RespGetExchangeMetrics
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
    api_instance = lighter.OrderApi(api_client)
    period = 'period_example' # str | 
    kind = 'kind_example' # str | 
    filter = 'filter_example' # str |  (optional)
    value = 'value_example' # str |  (optional)

    try:
        # exchangeMetrics
        api_response = await api_instance.exchange_metrics(period, kind, filter=filter, value=value)
        print("The response of OrderApi->exchange_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->exchange_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period** | **str**|  | 
 **kind** | **str**|  | 
 **filter** | **str**|  | [optional] 
 **value** | **str**|  | [optional] 

### Return type

[**RespGetExchangeMetrics**](RespGetExchangeMetrics.md)

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

# **exchange_stats**
> ExchangeStats exchange_stats()

exchangeStats

Get exchange stats

### Example


```python
import lighter
from lighter.models.exchange_stats import ExchangeStats
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
    api_instance = lighter.OrderApi(api_client)

    try:
        # exchangeStats
        api_response = await api_instance.exchange_stats()
        print("The response of OrderApi->exchange_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->exchange_stats: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ExchangeStats**](ExchangeStats.md)

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

# **execute_stats**
> RespGetExecuteStats execute_stats(period)

executeStats

Get execute stats

### Example


```python
import lighter
from lighter.models.resp_get_execute_stats import RespGetExecuteStats
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
    api_instance = lighter.OrderApi(api_client)
    period = 'period_example' # str | 

    try:
        # executeStats
        api_response = await api_instance.execute_stats(period)
        print("The response of OrderApi->execute_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->execute_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period** | **str**|  | 

### Return type

[**RespGetExecuteStats**](RespGetExecuteStats.md)

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

# **export**
> ExportData export(authorization, type, account_index=account_index, market_id=market_id, start_timestamp=start_timestamp, end_timestamp=end_timestamp, side=side, role=role, trade_type=trade_type)

export

Export trades and funding payments, limited to 12 months or 1M trades. END_TS_IN_MS - START_TS_IN_MS should not be larger than 12 months in milliseconds, both timestamps should be greater than or equal to 17 January 2025 00:00:00 UTC (lighter's mainnet genesis)

### Example


```python
import lighter
from lighter.models.export_data import ExportData
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
    api_instance = lighter.OrderApi(api_client)
    authorization = 'authorization_example' # str | 
    type = 'type_example' # str | 
    account_index = 56 # int |  (optional)
    market_id = 56 # int |  (optional)
    start_timestamp = 56 # int |  (optional)
    end_timestamp = 56 # int |  (optional)
    side = all # str |  (optional) (default to all)
    role = all # str |  (optional) (default to all)
    trade_type = all # str |  (optional) (default to all)

    try:
        # export
        api_response = await api_instance.export(authorization, type, account_index=account_index, market_id=market_id, start_timestamp=start_timestamp, end_timestamp=end_timestamp, side=side, role=role, trade_type=trade_type)
        print("The response of OrderApi->export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **type** | **str**|  | 
 **account_index** | **int**|  | [optional] 
 **market_id** | **int**|  | [optional] 
 **start_timestamp** | **int**|  | [optional] 
 **end_timestamp** | **int**|  | [optional] 
 **side** | **str**|  | [optional] [default to all]
 **role** | **str**|  | [optional] [default to all]
 **trade_type** | **str**|  | [optional] [default to all]

### Return type

[**ExportData**](ExportData.md)

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

# **order_book_details**
> OrderBookDetails order_book_details(market_id=market_id, filter=filter)

orderBookDetails

Get order books metadata

### Example


```python
import lighter
from lighter.models.order_book_details import OrderBookDetails
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
    api_instance = lighter.OrderApi(api_client)
    market_id = 56 # int |  (optional)
    filter = all # str | Filter order books by type (optional) (default to all)

    try:
        # orderBookDetails
        api_response = await api_instance.order_book_details(market_id=market_id, filter=filter)
        print("The response of OrderApi->order_book_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->order_book_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_id** | **int**|  | [optional] 
 **filter** | **str**| Filter order books by type | [optional] [default to all]

### Return type

[**OrderBookDetails**](OrderBookDetails.md)

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

# **order_book_orders**
> OrderBookOrders order_book_orders(market_id, limit)

orderBookOrders

Get order book orders

### Example


```python
import lighter
from lighter.models.order_book_orders import OrderBookOrders
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
    api_instance = lighter.OrderApi(api_client)
    market_id = 56 # int | 
    limit = 56 # int | 

    try:
        # orderBookOrders
        api_response = await api_instance.order_book_orders(market_id, limit)
        print("The response of OrderApi->order_book_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->order_book_orders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_id** | **int**|  | 
 **limit** | **int**|  | 

### Return type

[**OrderBookOrders**](OrderBookOrders.md)

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

# **order_books**
> OrderBooks order_books(market_id=market_id, filter=filter)

orderBooks

Get order books metadata.<hr>**Response Description:**<br><br>1) **Taker and maker fees** are in percentage.<br>2) **Min base amount:** The amount of base token that can be traded in a single order.<br>3) **Min quote amount:** The amount of quote token that can be traded in a single order.<br>4) **Supported size decimals:** The number of decimal places that can be used for the size of the order.<br>5) **Supported price decimals:** The number of decimal places that can be used for the price of the order.<br>6) **Supported quote decimals:** Size Decimals + Quote Decimals.

### Example


```python
import lighter
from lighter.models.order_books import OrderBooks
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
    api_instance = lighter.OrderApi(api_client)
    market_id = 56 # int |  (optional)
    filter = all # str |  (optional) (default to all)

    try:
        # orderBooks
        api_response = await api_instance.order_books(market_id=market_id, filter=filter)
        print("The response of OrderApi->order_books:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->order_books: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_id** | **int**|  | [optional] 
 **filter** | **str**|  | [optional] [default to all]

### Return type

[**OrderBooks**](OrderBooks.md)

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

# **recent_trades**
> Trades recent_trades(market_id, limit)

recentTrades

Get recent trades

### Example


```python
import lighter
from lighter.models.trades import Trades
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
    api_instance = lighter.OrderApi(api_client)
    market_id = 56 # int | 
    limit = 56 # int | 

    try:
        # recentTrades
        api_response = await api_instance.recent_trades(market_id, limit)
        print("The response of OrderApi->recent_trades:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->recent_trades: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_id** | **int**|  | 
 **limit** | **int**|  | 

### Return type

[**Trades**](Trades.md)

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

# **trades**
> Trades trades(sort_by, limit, authorization=authorization, market_id=market_id, market_type=market_type, account_index=account_index, order_index=order_index, sort_dir=sort_dir, cursor=cursor, var_from=var_from, ask_filter=ask_filter, role=role, type=type, aggregate=aggregate, skip_ask_order_id=skip_ask_order_id, skip_bid_order_id=skip_bid_order_id)

trades

Get trades for lighter accounts, including sub-accounts and public pools. `auth` is required for master accounts and sub accounts.

### Example


```python
import lighter
from lighter.models.trades import Trades
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
    api_instance = lighter.OrderApi(api_client)
    sort_by = 'sort_by_example' # str | 
    limit = 56 # int | 
    authorization = 'authorization_example' # str |  (optional)
    market_id = 56 # int |  (optional)
    market_type = all # str |  (optional) (default to all)
    account_index = 56 # int |  (optional)
    order_index = 56 # int |  (optional)
    sort_dir = desc # str |  (optional) (default to desc)
    cursor = 'cursor_example' # str |  (optional)
    var_from = 56 # int |  (optional)
    ask_filter = 56 # int |  (optional)
    role = all # str |  (optional) (default to all)
    type = all # str |  (optional) (default to all)
    aggregate = False # bool |  (optional) (default to False)
    skip_ask_order_id = 'skip_ask_order_id_example' # str |  (optional)
    skip_bid_order_id = 'skip_bid_order_id_example' # str |  (optional)

    try:
        # trades
        api_response = await api_instance.trades(sort_by, limit, authorization=authorization, market_id=market_id, market_type=market_type, account_index=account_index, order_index=order_index, sort_dir=sort_dir, cursor=cursor, var_from=var_from, ask_filter=ask_filter, role=role, type=type, aggregate=aggregate, skip_ask_order_id=skip_ask_order_id, skip_bid_order_id=skip_bid_order_id)
        print("The response of OrderApi->trades:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->trades: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sort_by** | **str**|  | 
 **limit** | **int**|  | 
 **authorization** | **str**|  | [optional] 
 **market_id** | **int**|  | [optional] 
 **market_type** | **str**|  | [optional] [default to all]
 **account_index** | **int**|  | [optional] 
 **order_index** | **int**|  | [optional] 
 **sort_dir** | **str**|  | [optional] [default to desc]
 **cursor** | **str**|  | [optional] 
 **var_from** | **int**|  | [optional] 
 **ask_filter** | **int**|  | [optional] 
 **role** | **str**|  | [optional] [default to all]
 **type** | **str**|  | [optional] [default to all]
 **aggregate** | **bool**|  | [optional] [default to False]
 **skip_ask_order_id** | **str**|  | [optional] 
 **skip_bid_order_id** | **str**|  | [optional] 

### Return type

[**Trades**](Trades.md)

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

