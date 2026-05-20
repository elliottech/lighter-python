# lighter.BridgeApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_intent_address**](BridgeApi.md#create_intent_address) | **POST** /api/v1/createIntentAddress | createIntentAddress
[**deposit_latest**](BridgeApi.md#deposit_latest) | **GET** /api/v1/deposit/latest | deposit_latest
[**deposit_networks**](BridgeApi.md#deposit_networks) | **GET** /api/v1/deposit/networks | deposit_networks
[**fastbridge_info**](BridgeApi.md#fastbridge_info) | **GET** /api/v1/fastbridge/info | fastbridge_info
[**fastwithdraw**](BridgeApi.md#fastwithdraw) | **POST** /api/v1/fastwithdraw | fastwithdraw
[**fastwithdraw_info**](BridgeApi.md#fastwithdraw_info) | **GET** /api/v1/fastwithdraw/info | fastwithdraw_info


# **create_intent_address**
> CreateIntentAddressResp create_intent_address(chain_id, from_addr, amount, is_external_deposit=is_external_deposit)

createIntentAddress

Create a bridge intent address for CCTP bridge

### Example


```python
import lighter
from lighter.models.create_intent_address_resp import CreateIntentAddressResp
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
    api_instance = lighter.BridgeApi(api_client)
    chain_id = 'chain_id_example' # str | 
    from_addr = 'from_addr_example' # str | 
    amount = 'amount_example' # str | 
    is_external_deposit = True # bool |  (optional)

    try:
        # createIntentAddress
        api_response = await api_instance.create_intent_address(chain_id, from_addr, amount, is_external_deposit=is_external_deposit)
        print("The response of BridgeApi->create_intent_address:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BridgeApi->create_intent_address: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chain_id** | **str**|  | 
 **from_addr** | **str**|  | 
 **amount** | **str**|  | 
 **is_external_deposit** | **bool**|  | [optional] 

### Return type

[**CreateIntentAddressResp**](CreateIntentAddressResp.md)

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

# **deposit_latest**
> Deposit deposit_latest(l1_address)

deposit_latest

Get most recent deposit for given l1 address

### Example


```python
import lighter
from lighter.models.deposit import Deposit
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
    api_instance = lighter.BridgeApi(api_client)
    l1_address = 'l1_address_example' # str | 

    try:
        # deposit_latest
        api_response = await api_instance.deposit_latest(l1_address)
        print("The response of BridgeApi->deposit_latest:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BridgeApi->deposit_latest: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **l1_address** | **str**|  | 

### Return type

[**Deposit**](Deposit.md)

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

# **deposit_networks**
> BridgeSupportedNetworks deposit_networks()

deposit_networks

Get networks that support deposits via intent address

### Example


```python
import lighter
from lighter.models.bridge_supported_networks import BridgeSupportedNetworks
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
    api_instance = lighter.BridgeApi(api_client)

    try:
        # deposit_networks
        api_response = await api_instance.deposit_networks()
        print("The response of BridgeApi->deposit_networks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BridgeApi->deposit_networks: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BridgeSupportedNetworks**](BridgeSupportedNetworks.md)

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

# **fastbridge_info**
> RespGetFastBridgeInfo fastbridge_info()

fastbridge_info

Get fast bridge info

### Example


```python
import lighter
from lighter.models.resp_get_fast_bridge_info import RespGetFastBridgeInfo
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
    api_instance = lighter.BridgeApi(api_client)

    try:
        # fastbridge_info
        api_response = await api_instance.fastbridge_info()
        print("The response of BridgeApi->fastbridge_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BridgeApi->fastbridge_info: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RespGetFastBridgeInfo**](RespGetFastBridgeInfo.md)

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

# **fastwithdraw**
> ResultCode fastwithdraw(tx_info, to_address, authorization=authorization, auth=auth)

fastwithdraw

Fast withdraw

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
    api_instance = lighter.BridgeApi(api_client)
    tx_info = 'tx_info_example' # str | 
    to_address = 'to_address_example' # str | 
    authorization = 'authorization_example' # str |  make required after integ is done (optional)
    auth = 'auth_example' # str |  made optional to support header auth clients (optional)

    try:
        # fastwithdraw
        api_response = await api_instance.fastwithdraw(tx_info, to_address, authorization=authorization, auth=auth)
        print("The response of BridgeApi->fastwithdraw:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BridgeApi->fastwithdraw: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tx_info** | **str**|  | 
 **to_address** | **str**|  | 
 **authorization** | **str**|  make required after integ is done | [optional] 
 **auth** | **str**|  made optional to support header auth clients | [optional] 

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

# **fastwithdraw_info**
> RespGetFastwithdrawalInfo fastwithdraw_info(authorization, account_index)

fastwithdraw_info

Get fast withdraw info

### Example


```python
import lighter
from lighter.models.resp_get_fastwithdrawal_info import RespGetFastwithdrawalInfo
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
    api_instance = lighter.BridgeApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 

    try:
        # fastwithdraw_info
        api_response = await api_instance.fastwithdraw_info(authorization, account_index)
        print("The response of BridgeApi->fastwithdraw_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BridgeApi->fastwithdraw_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 

### Return type

[**RespGetFastwithdrawalInfo**](RespGetFastwithdrawalInfo.md)

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

