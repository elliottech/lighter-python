# lighter.UpdownApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**up_down_candles**](UpdownApi.md#up_down_candles) | **GET** /api/v1/upDownCandles | upDownCandles


# **up_down_candles**
> RespGetUpDownCandles up_down_candles(symbol, duration, start_timestamp, end_timestamp, resolution=resolution, limit=limit)

upDownCandles

Get the OHLC candles (1s = the exact price observations, or 30s) of an up/down market series (symbol + duration, e.g. btc/5m) in a bounded time range (at most 24h), oldest first. Pass next_cursor as start_timestamp to page forward; live candles are on the up_down_candle/<symbol>/<duration>/<resolution> websocket channel.

### Example


```python
import lighter
from lighter.models.resp_get_up_down_candles import RespGetUpDownCandles
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
    api_instance = lighter.UpdownApi(api_client)
    symbol = 'symbol_example' # str |  market series: underlying (case-insensitive) ...
    duration = 'duration_example' # str |  ... and market duration, e.g. 30s or 5m
    start_timestamp = 56 # int |  inclusive bucket start, seconds
    end_timestamp = 56 # int |  inclusive, seconds; at most 24h after start_timestamp
    resolution = 1s # str |  1s candles are the observations themselves (optional) (default to 1s)
    limit = 56 # int |  (optional)

    try:
        # upDownCandles
        api_response = await api_instance.up_down_candles(symbol, duration, start_timestamp, end_timestamp, resolution=resolution, limit=limit)
        print("The response of UpdownApi->up_down_candles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UpdownApi->up_down_candles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**|  market series: underlying (case-insensitive) ... | 
 **duration** | **str**|  ... and market duration, e.g. 30s or 5m | 
 **start_timestamp** | **int**|  inclusive bucket start, seconds | 
 **end_timestamp** | **int**|  inclusive, seconds; at most 24h after start_timestamp | 
 **resolution** | **str**|  1s candles are the observations themselves | [optional] [default to 1s]
 **limit** | **int**|  | [optional] 

### Return type

[**RespGetUpDownCandles**](RespGetUpDownCandles.md)

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

