# lighter.LivepointsApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**live_points_total**](LivepointsApi.md#live_points_total) | **GET** /api/v1/livePoints/total | livePoints_total


# **live_points_total**
> LivePointsTotal live_points_total(account_index, authorization=authorization)

livePoints_total

Get live points total for an account

### Example


```python
import lighter
from lighter.models.live_points_total import LivePointsTotal
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
    api_instance = lighter.LivepointsApi(api_client)
    account_index = 56 # int | 
    authorization = 'authorization_example' # str |  (optional)

    try:
        # livePoints_total
        api_response = await api_instance.live_points_total(account_index, authorization=authorization)
        print("The response of LivepointsApi->live_points_total:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LivepointsApi->live_points_total: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **authorization** | **str**|  | [optional] 

### Return type

[**LivePointsTotal**](LivePointsTotal.md)

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

