# lighter.ReferralApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**referral_has_referee_by_address**](ReferralApi.md#referral_has_referee_by_address) | **GET** /api/v1/referral/hasRefereeByAddress | referral_hasRefereeByAddress
[**referral_points**](ReferralApi.md#referral_points) | **GET** /api/v1/referral/points | referral_points


# **referral_has_referee_by_address**
> HasRefereeCode referral_has_referee_by_address(l1_address)

referral_hasRefereeByAddress

Does L1 address have referee code?

### Example


```python
import lighter
from lighter.models.has_referee_code import HasRefereeCode
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
    api_instance = lighter.ReferralApi(api_client)
    l1_address = 'l1_address_example' # str | 

    try:
        # referral_hasRefereeByAddress
        api_response = await api_instance.referral_has_referee_by_address(l1_address)
        print("The response of ReferralApi->referral_has_referee_by_address:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferralApi->referral_has_referee_by_address: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **l1_address** | **str**|  | 

### Return type

[**HasRefereeCode**](HasRefereeCode.md)

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

# **referral_points**
> ReferralPoints referral_points(account_index, authorization=authorization, auth=auth)

referral_points

Get referral points

### Example


```python
import lighter
from lighter.models.referral_points import ReferralPoints
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
    api_instance = lighter.ReferralApi(api_client)
    account_index = 56 # int | 
    authorization = 'authorization_example' # str |  make required after integ is done (optional)
    auth = 'auth_example' # str |  made optional to support header auth clients (optional)

    try:
        # referral_points
        api_response = await api_instance.referral_points(account_index, authorization=authorization, auth=auth)
        print("The response of ReferralApi->referral_points:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferralApi->referral_points: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **authorization** | **str**|  make required after integ is done | [optional] 
 **auth** | **str**|  made optional to support header auth clients | [optional] 

### Return type

[**ReferralPoints**](ReferralPoints.md)

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

