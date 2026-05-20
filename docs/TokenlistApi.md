# lighter.TokenlistApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tokenlist**](TokenlistApi.md#tokenlist) | **GET** /api/v1/tokenlist | tokenlist


# **tokenlist**
> TokenList tokenlist()

tokenlist

Get token list and their metadata

### Example


```python
import lighter
from lighter.models.token_list import TokenList
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
    api_instance = lighter.TokenlistApi(api_client)

    try:
        # tokenlist
        api_response = await api_instance.tokenlist()
        print("The response of TokenlistApi->tokenlist:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TokenlistApi->tokenlist: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TokenList**](TokenList.md)

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

