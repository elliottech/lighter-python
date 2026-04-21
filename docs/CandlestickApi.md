# lighter.CandlestickApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**candles**](CandlestickApi.md#candles) | **GET** /api/v1/candles | candles
[**fundings**](CandlestickApi.md#fundings) | **GET** /api/v1/fundings | fundings


# **candles**
> Candles candles(market_id, resolution, start_timestamp, end_timestamp, count_back, set_timestamp_to_end=set_timestamp_to_end)

candles

Get candles data. Returns at most 500 candles per call. Zero values are omitted from the response.

### Example


```python
import lighter
from lighter.models.candles import Candles
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
    api_instance = lighter.CandlestickApi(api_client)
    market_id = 56 # int | 
    resolution = 'resolution_example' # str | 
    start_timestamp = 56 # int | 
    end_timestamp = 56 # int | 
    count_back = 56 # int | 
    set_timestamp_to_end = False # bool |  (optional) (default to False)

    try:
        # candles
        api_response = await api_instance.candles(market_id, resolution, start_timestamp, end_timestamp, count_back, set_timestamp_to_end=set_timestamp_to_end)
        print("The response of CandlestickApi->candles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CandlestickApi->candles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_id** | **int**|  | 
 **resolution** | **str**|  | 
 **start_timestamp** | **int**|  | 
 **end_timestamp** | **int**|  | 
 **count_back** | **int**|  | 
 **set_timestamp_to_end** | **bool**|  | [optional] [default to False]

### Return type

[**Candles**](Candles.md)

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

# **fundings**
> Fundings fundings(market_id, resolution, start_timestamp, end_timestamp, count_back)

fundings

Get fundings

### Example


```python
import lighter
from lighter.models.fundings import Fundings
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
    api_instance = lighter.CandlestickApi(api_client)
    market_id = 56 # int | 
    resolution = 'resolution_example' # str | 
    start_timestamp = 56 # int | 
    end_timestamp = 56 # int | 
    count_back = 56 # int | 

    try:
        # fundings
        api_response = await api_instance.fundings(market_id, resolution, start_timestamp, end_timestamp, count_back)
        print("The response of CandlestickApi->fundings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CandlestickApi->fundings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_id** | **int**|  | 
 **resolution** | **str**|  | 
 **start_timestamp** | **int**|  | 
 **end_timestamp** | **int**|  | 
 **count_back** | **int**|  | 

### Return type

[**Fundings**](Fundings.md)

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

