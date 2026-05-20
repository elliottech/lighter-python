# lighter.InfoApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**layer1_basic_info**](InfoApi.md#layer1_basic_info) | **GET** /api/v1/layer1BasicInfo | layer1BasicInfo
[**system_config**](InfoApi.md#system_config) | **GET** /api/v1/systemConfig | systemConfig
[**transfer_fee_info**](InfoApi.md#transfer_fee_info) | **GET** /api/v1/transferFeeInfo | transferFeeInfo
[**withdrawal_delay**](InfoApi.md#withdrawal_delay) | **GET** /api/v1/withdrawalDelay | withdrawalDelay


# **layer1_basic_info**
> Layer1BasicInfo layer1_basic_info()

layer1BasicInfo

Get zklighter l1 general info, including contract address and rpc info

### Example


```python
import lighter
from lighter.models.layer1_basic_info import Layer1BasicInfo
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
    api_instance = lighter.InfoApi(api_client)

    try:
        # layer1BasicInfo
        api_response = await api_instance.layer1_basic_info()
        print("The response of InfoApi->layer1_basic_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InfoApi->layer1_basic_info: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Layer1BasicInfo**](Layer1BasicInfo.md)

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

# **system_config**
> SystemConfig system_config()

systemConfig

Get system config

### Example


```python
import lighter
from lighter.models.system_config import SystemConfig
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
    api_instance = lighter.InfoApi(api_client)

    try:
        # systemConfig
        api_response = await api_instance.system_config()
        print("The response of InfoApi->system_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InfoApi->system_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SystemConfig**](SystemConfig.md)

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

# **transfer_fee_info**
> TransferFeeInfo transfer_fee_info(authorization, account_index, to_account_index=to_account_index)

transferFeeInfo

Transfer fee info

### Example


```python
import lighter
from lighter.models.transfer_fee_info import TransferFeeInfo
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
    api_instance = lighter.InfoApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    to_account_index = 56 # int |  (optional)

    try:
        # transferFeeInfo
        api_response = await api_instance.transfer_fee_info(authorization, account_index, to_account_index=to_account_index)
        print("The response of InfoApi->transfer_fee_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InfoApi->transfer_fee_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **to_account_index** | **int**|  | [optional] 

### Return type

[**TransferFeeInfo**](TransferFeeInfo.md)

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

# **withdrawal_delay**
> RespWithdrawalDelay withdrawal_delay()

withdrawalDelay

Withdrawal delay in seconds

### Example


```python
import lighter
from lighter.models.resp_withdrawal_delay import RespWithdrawalDelay
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
    api_instance = lighter.InfoApi(api_client)

    try:
        # withdrawalDelay
        api_response = await api_instance.withdrawal_delay()
        print("The response of InfoApi->withdrawal_delay:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InfoApi->withdrawal_delay: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RespWithdrawalDelay**](RespWithdrawalDelay.md)

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

