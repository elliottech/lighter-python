# lighter.AccountApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**account**](AccountApi.md#account) | **GET** /api/v1/account | account
[**account_limits**](AccountApi.md#account_limits) | **GET** /api/v1/accountLimits | accountLimits
[**account_metadata**](AccountApi.md#account_metadata) | **GET** /api/v1/accountMetadata | accountMetadata
[**accounts_by_l1_address**](AccountApi.md#accounts_by_l1_address) | **GET** /api/v1/accountsByL1Address | accountsByL1Address
[**apikeys**](AccountApi.md#apikeys) | **GET** /api/v1/apikeys | apikeys
[**change_account_tier**](AccountApi.md#change_account_tier) | **POST** /api/v1/changeAccountTier | changeAccountTier
[**get_maker_only_api_keys**](AccountApi.md#get_maker_only_api_keys) | **GET** /api/v1/getMakerOnlyApiKeys | getMakerOnlyApiKeys
[**l1_metadata**](AccountApi.md#l1_metadata) | **GET** /api/v1/l1Metadata | l1Metadata
[**lease_options**](AccountApi.md#lease_options) | **GET** /api/v1/leaseOptions | leaseOptions
[**leases**](AccountApi.md#leases) | **GET** /api/v1/leases | leases
[**liquidations**](AccountApi.md#liquidations) | **GET** /api/v1/liquidations | liquidations
[**lit_lease**](AccountApi.md#lit_lease) | **POST** /api/v1/litLease | litLease
[**partner_stats**](AccountApi.md#partner_stats) | **GET** /api/v1/partnerStats | partnerStats
[**pnl**](AccountApi.md#pnl) | **GET** /api/v1/pnl | pnl
[**position_funding**](AccountApi.md#position_funding) | **GET** /api/v1/positionFunding | positionFunding
[**public_pools_metadata**](AccountApi.md#public_pools_metadata) | **GET** /api/v1/publicPoolsMetadata | publicPoolsMetadata
[**referral_user_referrals**](AccountApi.md#referral_user_referrals) | **GET** /api/v1/referral/userReferrals | userReferrals
[**rfq_create**](AccountApi.md#rfq_create) | **POST** /api/v1/rfq/create | rfq_create
[**rfq_get**](AccountApi.md#rfq_get) | **GET** /api/v1/rfq/get | rfq_get
[**rfq_list**](AccountApi.md#rfq_list) | **GET** /api/v1/rfq/list | rfq_list
[**rfq_respond**](AccountApi.md#rfq_respond) | **POST** /api/v1/rfq/respond | rfq_respond
[**rfq_update**](AccountApi.md#rfq_update) | **POST** /api/v1/rfq/update | rfq_update
[**set_maker_only_api_keys**](AccountApi.md#set_maker_only_api_keys) | **POST** /api/v1/setMakerOnlyApiKeys | setMakerOnlyApiKeys
[**tokens**](AccountApi.md#tokens) | **GET** /api/v1/tokens | tokens
[**tokens_create**](AccountApi.md#tokens_create) | **POST** /api/v1/tokens/create | tokens_create
[**tokens_revoke**](AccountApi.md#tokens_revoke) | **POST** /api/v1/tokens/revoke | tokens_revoke


# **account**
> DetailedAccounts account(by, value, active_only=active_only, cursor=cursor)

account

Get account by an account's index, or L1 address

### Example


```python
import lighter
from lighter.models.detailed_accounts import DetailedAccounts
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
    api_instance = lighter.AccountApi(api_client)
    by = 'by_example' # str | 
    value = 'value_example' # str | 
    active_only = False # bool | Hide markets for which leverage and margin settings are present (meaning the account traded it at least once), but with no active position. (optional) (default to False)
    cursor = 'cursor_example' # str |  (optional)

    try:
        # account
        api_response = await api_instance.account(by, value, active_only=active_only, cursor=cursor)
        print("The response of AccountApi->account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **by** | **str**|  | 
 **value** | **str**|  | 
 **active_only** | **bool**| Hide markets for which leverage and margin settings are present (meaning the account traded it at least once), but with no active position. | [optional] [default to False]
 **cursor** | **str**|  | [optional] 

### Return type

[**DetailedAccounts**](DetailedAccounts.md)

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

# **account_limits**
> AccountLimits account_limits(account_index, authorization)

accountLimits

Get account limits. For more details on account types, see this page: https://apidocs.lighter.xyz/docs/account-types

### Example


```python
import lighter
from lighter.models.account_limits import AccountLimits
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | 
    authorization = 'authorization_example' # str | 

    try:
        # accountLimits
        api_response = await api_instance.account_limits(account_index, authorization)
        print("The response of AccountApi->account_limits:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->account_limits: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **authorization** | **str**|  | 

### Return type

[**AccountLimits**](AccountLimits.md)

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

# **account_metadata**
> AccountMetadatas account_metadata(by, value, authorization=authorization, cursor=cursor)

accountMetadata

Get account metadatas

### Example


```python
import lighter
from lighter.models.account_metadatas import AccountMetadatas
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
    api_instance = lighter.AccountApi(api_client)
    by = 'by_example' # str | 
    value = 'value_example' # str | 
    authorization = 'authorization_example' # str |  (optional)
    cursor = 'cursor_example' # str |  (optional)

    try:
        # accountMetadata
        api_response = await api_instance.account_metadata(by, value, authorization=authorization, cursor=cursor)
        print("The response of AccountApi->account_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->account_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **by** | **str**|  | 
 **value** | **str**|  | 
 **authorization** | **str**|  | [optional] 
 **cursor** | **str**|  | [optional] 

### Return type

[**AccountMetadatas**](AccountMetadatas.md)

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

# **accounts_by_l1_address**
> SubAccounts accounts_by_l1_address(l1_address, cursor=cursor)

accountsByL1Address

Returns all accounts associated with the given L1 address

### Example


```python
import lighter
from lighter.models.sub_accounts import SubAccounts
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
    api_instance = lighter.AccountApi(api_client)
    l1_address = 'l1_address_example' # str | 
    cursor = 'cursor_example' # str |  (optional)

    try:
        # accountsByL1Address
        api_response = await api_instance.accounts_by_l1_address(l1_address, cursor=cursor)
        print("The response of AccountApi->accounts_by_l1_address:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->accounts_by_l1_address: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **l1_address** | **str**|  | 
 **cursor** | **str**|  | [optional] 

### Return type

[**SubAccounts**](SubAccounts.md)

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

# **apikeys**
> AccountApiKeys apikeys(account_index, api_key_index=api_key_index)

apikeys

Get account api key. Set `api_key_index` to 255 to retrieve all api keys associated with the account.

### Example


```python
import lighter
from lighter.models.account_api_keys import AccountApiKeys
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | 
    api_key_index = 56 # int |  (optional)

    try:
        # apikeys
        api_response = await api_instance.apikeys(account_index, api_key_index=api_key_index)
        print("The response of AccountApi->apikeys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->apikeys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **api_key_index** | **int**|  | [optional] 

### Return type

[**AccountApiKeys**](AccountApiKeys.md)

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

# **change_account_tier**
> RespChangeAccountTier change_account_tier(account_index, new_tier, authorization=authorization, auth=auth)

changeAccountTier

Change account tier. You can only perform this action once every 24 hours, and with no orders or positions open.

### Example


```python
import lighter
from lighter.models.resp_change_account_tier import RespChangeAccountTier
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | 
    new_tier = 'new_tier_example' # str | 
    authorization = 'authorization_example' # str |  make required after integ is done (optional)
    auth = 'auth_example' # str |  made optional to support header auth clients (optional)

    try:
        # changeAccountTier
        api_response = await api_instance.change_account_tier(account_index, new_tier, authorization=authorization, auth=auth)
        print("The response of AccountApi->change_account_tier:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->change_account_tier: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **new_tier** | **str**|  | 
 **authorization** | **str**|  make required after integ is done | [optional] 
 **auth** | **str**|  made optional to support header auth clients | [optional] 

### Return type

[**RespChangeAccountTier**](RespChangeAccountTier.md)

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

# **get_maker_only_api_keys**
> RespGetMakerOnlyApiKeys get_maker_only_api_keys(authorization, account_index)

getMakerOnlyApiKeys

Get maker-only API key indexes

### Example


```python
import lighter
from lighter.models.resp_get_maker_only_api_keys import RespGetMakerOnlyApiKeys
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 

    try:
        # getMakerOnlyApiKeys
        api_response = await api_instance.get_maker_only_api_keys(authorization, account_index)
        print("The response of AccountApi->get_maker_only_api_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->get_maker_only_api_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 

### Return type

[**RespGetMakerOnlyApiKeys**](RespGetMakerOnlyApiKeys.md)

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

# **l1_metadata**
> L1Metadata l1_metadata(authorization, l1_address)

l1Metadata

Get L1 metadata

### Example


```python
import lighter
from lighter.models.l1_metadata import L1Metadata
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    l1_address = 'l1_address_example' # str | 

    try:
        # l1Metadata
        api_response = await api_instance.l1_metadata(authorization, l1_address)
        print("The response of AccountApi->l1_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->l1_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **l1_address** | **str**|  | 

### Return type

[**L1Metadata**](L1Metadata.md)

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

# **lease_options**
> RespGetLeaseOptions lease_options()

leaseOptions

Returns available lease duration/rate tiers, sorted by duration descending.

### Example


```python
import lighter
from lighter.models.resp_get_lease_options import RespGetLeaseOptions
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
    api_instance = lighter.AccountApi(api_client)

    try:
        # leaseOptions
        api_response = await api_instance.lease_options()
        print("The response of AccountApi->lease_options:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->lease_options: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RespGetLeaseOptions**](RespGetLeaseOptions.md)

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

# **leases**
> RespGetLeases leases(account_index, authorization=authorization, cursor=cursor, limit=limit, auth=auth)

leases

Returns paginated lease entries for an account, most recent first. Supports read-only auth via signature/account_index/timestamp query params.

### Example


```python
import lighter
from lighter.models.resp_get_leases import RespGetLeases
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | Account index to fetch leases for
    authorization = 'authorization_example' # str | API token authorization (optional)
    cursor = 'cursor_example' # str | Pagination cursor from a previous response (optional)
    limit = 20 # int | Number of results to return (1–100, default 20) (optional) (default to 20)
    auth = 'auth_example' # str | Read-only auth (alternative to header authorization) (optional)

    try:
        # leases
        api_response = await api_instance.leases(account_index, authorization=authorization, cursor=cursor, limit=limit, auth=auth)
        print("The response of AccountApi->leases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->leases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**| Account index to fetch leases for | 
 **authorization** | **str**| API token authorization | [optional] 
 **cursor** | **str**| Pagination cursor from a previous response | [optional] 
 **limit** | **int**| Number of results to return (1–100, default 20) | [optional] [default to 20]
 **auth** | **str**| Read-only auth (alternative to header authorization) | [optional] 

### Return type

[**RespGetLeases**](RespGetLeases.md)

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

# **liquidations**
> LiquidationInfos liquidations(authorization, account_index, limit, market_id=market_id, cursor=cursor)

liquidations

Get liquidation infos

### Example


```python
import lighter
from lighter.models.liquidation_infos import LiquidationInfos
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    limit = 56 # int | 
    market_id = 56 # int |  (optional)
    cursor = 'cursor_example' # str |  (optional)

    try:
        # liquidations
        api_response = await api_instance.liquidations(authorization, account_index, limit, market_id=market_id, cursor=cursor)
        print("The response of AccountApi->liquidations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->liquidations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **limit** | **int**|  | 
 **market_id** | **int**|  | [optional] 
 **cursor** | **str**|  | [optional] 

### Return type

[**LiquidationInfos**](LiquidationInfos.md)

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

# **lit_lease**
> TxHash lit_lease(tx_info, lease_amount, duration_days, authorization=authorization)

litLease

Submit a LIT lease transfer. The server calculates the required fee based on lease_amount and duration_days, then executes the transfer. Fee formula (integer arithmetic): fee = lease_amount × (annual_rate × 100) × duration_days / (360 × 10000).

### Example


```python
import lighter
from lighter.models.tx_hash import TxHash
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
    api_instance = lighter.AccountApi(api_client)
    tx_info = 'tx_info_example' # str | Signed transaction info (JSON with L2 signature, L1 signature, etc.)
    lease_amount = 'lease_amount_example' # str | Amount of LIT to lease in raw units (1 LIT = 100000000)
    duration_days = 56 # int | Lease duration in days. Must match one of the available lease options.
    authorization = 'authorization_example' # str | API token authorization (optional)

    try:
        # litLease
        api_response = await api_instance.lit_lease(tx_info, lease_amount, duration_days, authorization=authorization)
        print("The response of AccountApi->lit_lease:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->lit_lease: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tx_info** | **str**| Signed transaction info (JSON with L2 signature, L1 signature, etc.) | 
 **lease_amount** | **str**| Amount of LIT to lease in raw units (1 LIT &#x3D; 100000000) | 
 **duration_days** | **int**| Lease duration in days. Must match one of the available lease options. | 
 **authorization** | **str**| API token authorization | [optional] 

### Return type

[**TxHash**](TxHash.md)

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

# **partner_stats**
> PartnerStats partner_stats(account_index, start_timestamp=start_timestamp, end_timestamp=end_timestamp)

partnerStats

Get partner stats. If timestamps are not provided, all-time stats will be returned.

### Example


```python
import lighter
from lighter.models.partner_stats import PartnerStats
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | 
    start_timestamp = 56 # int |  (optional)
    end_timestamp = 56 # int |  (optional)

    try:
        # partnerStats
        api_response = await api_instance.partner_stats(account_index, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        print("The response of AccountApi->partner_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->partner_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **start_timestamp** | **int**|  | [optional] 
 **end_timestamp** | **int**|  | [optional] 

### Return type

[**PartnerStats**](PartnerStats.md)

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

# **pnl**
> AccountPnL pnl(by, value, resolution, start_timestamp, end_timestamp, count_back, authorization=authorization, ignore_transfers=ignore_transfers)

pnl

Get account PnL chart

### Example


```python
import lighter
from lighter.models.account_pn_l import AccountPnL
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
    api_instance = lighter.AccountApi(api_client)
    by = 'by_example' # str | 
    value = 'value_example' # str | 
    resolution = 'resolution_example' # str | 
    start_timestamp = 56 # int | 
    end_timestamp = 56 # int | 
    count_back = 56 # int | 
    authorization = 'authorization_example' # str |  (optional)
    ignore_transfers = False # bool |  (optional) (default to False)

    try:
        # pnl
        api_response = await api_instance.pnl(by, value, resolution, start_timestamp, end_timestamp, count_back, authorization=authorization, ignore_transfers=ignore_transfers)
        print("The response of AccountApi->pnl:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->pnl: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **by** | **str**|  | 
 **value** | **str**|  | 
 **resolution** | **str**|  | 
 **start_timestamp** | **int**|  | 
 **end_timestamp** | **int**|  | 
 **count_back** | **int**|  | 
 **authorization** | **str**|  | [optional] 
 **ignore_transfers** | **bool**|  | [optional] [default to False]

### Return type

[**AccountPnL**](AccountPnL.md)

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

# **position_funding**
> PositionFundings position_funding(account_index, limit, authorization=authorization, market_id=market_id, cursor=cursor, side=side, start_timestamp=start_timestamp, end_timestamp=end_timestamp)

positionFunding

Get accounts position fundings

### Example


```python
import lighter
from lighter.models.position_fundings import PositionFundings
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | 
    limit = 56 # int | 
    authorization = 'authorization_example' # str |  (optional)
    market_id = 56 # int |  (optional)
    cursor = 'cursor_example' # str |  (optional)
    side = all # str |  (optional) (default to all)
    start_timestamp = 56 # int |  (optional)
    end_timestamp = 56 # int |  (optional)

    try:
        # positionFunding
        api_response = await api_instance.position_funding(account_index, limit, authorization=authorization, market_id=market_id, cursor=cursor, side=side, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        print("The response of AccountApi->position_funding:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->position_funding: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **limit** | **int**|  | 
 **authorization** | **str**|  | [optional] 
 **market_id** | **int**|  | [optional] 
 **cursor** | **str**|  | [optional] 
 **side** | **str**|  | [optional] [default to all]
 **start_timestamp** | **int**|  | [optional] 
 **end_timestamp** | **int**|  | [optional] 

### Return type

[**PositionFundings**](PositionFundings.md)

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

# **public_pools_metadata**
> RespPublicPoolsMetadata public_pools_metadata(index, limit, authorization=authorization, filter=filter, account_index=account_index)

publicPoolsMetadata

Get public pools metadata. `auth` is required in case you specify an account_index. You will see public pools with an index that starts an n-1 of the one you specify. To see staking pools, use `filter=stake`

### Example


```python
import lighter
from lighter.models.resp_public_pools_metadata import RespPublicPoolsMetadata
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
    api_instance = lighter.AccountApi(api_client)
    index = 56 # int | 
    limit = 56 # int | 
    authorization = 'authorization_example' # str |  (optional)
    filter = 'filter_example' # str |  (optional)
    account_index = 56 # int |  (optional)

    try:
        # publicPoolsMetadata
        api_response = await api_instance.public_pools_metadata(index, limit, authorization=authorization, filter=filter, account_index=account_index)
        print("The response of AccountApi->public_pools_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->public_pools_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **index** | **int**|  | 
 **limit** | **int**|  | 
 **authorization** | **str**|  | [optional] 
 **filter** | **str**|  | [optional] 
 **account_index** | **int**|  | [optional] 

### Return type

[**RespPublicPoolsMetadata**](RespPublicPoolsMetadata.md)

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

# **referral_user_referrals**
> UserReferrals referral_user_referrals(l1_address, authorization=authorization, cursor=cursor, auth=auth, stats_start_timestamp=stats_start_timestamp, stats_end_timestamp=stats_end_timestamp, limit=limit)

userReferrals

Get user referrals

### Example


```python
import lighter
from lighter.models.user_referrals import UserReferrals
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
    api_instance = lighter.AccountApi(api_client)
    l1_address = 'l1_address_example' # str | 
    authorization = 'authorization_example' # str |  (optional)
    cursor = 'cursor_example' # str |  (optional)
    auth = 'auth_example' # str |  (optional)
    stats_start_timestamp = 56 # int |  (optional)
    stats_end_timestamp = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # userReferrals
        api_response = await api_instance.referral_user_referrals(l1_address, authorization=authorization, cursor=cursor, auth=auth, stats_start_timestamp=stats_start_timestamp, stats_end_timestamp=stats_end_timestamp, limit=limit)
        print("The response of AccountApi->referral_user_referrals:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->referral_user_referrals: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **l1_address** | **str**|  | 
 **authorization** | **str**|  | [optional] 
 **cursor** | **str**|  | [optional] 
 **auth** | **str**|  | [optional] 
 **stats_start_timestamp** | **int**|  | [optional] 
 **stats_end_timestamp** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**UserReferrals**](UserReferrals.md)

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

# **rfq_create**
> RespCreateRFQ rfq_create(authorization, market_index, direction, base_amount=base_amount, quote_amount=quote_amount, metadata=metadata)

rfq_create

Create RFQ

### Example


```python
import lighter
from lighter.models.resp_create_rfq import RespCreateRFQ
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    market_index = 56 # int | 
    direction = 56 # int | 
    base_amount = 'base_amount_example' # str |  (optional)
    quote_amount = 'quote_amount_example' # str |  (optional)
    metadata = 'metadata_example' # str |  (optional)

    try:
        # rfq_create
        api_response = await api_instance.rfq_create(authorization, market_index, direction, base_amount=base_amount, quote_amount=quote_amount, metadata=metadata)
        print("The response of AccountApi->rfq_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->rfq_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **market_index** | **int**|  | 
 **direction** | **int**|  | 
 **base_amount** | **str**|  | [optional] 
 **quote_amount** | **str**|  | [optional] 
 **metadata** | **str**|  | [optional] 

### Return type

[**RespCreateRFQ**](RespCreateRFQ.md)

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

# **rfq_get**
> RespGetRFQ rfq_get(authorization, rfq_id)

rfq_get

Get RFQ by ID

### Example


```python
import lighter
from lighter.models.resp_get_rfq import RespGetRFQ
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    rfq_id = 56 # int | 

    try:
        # rfq_get
        api_response = await api_instance.rfq_get(authorization, rfq_id)
        print("The response of AccountApi->rfq_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->rfq_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **rfq_id** | **int**|  | 

### Return type

[**RespGetRFQ**](RespGetRFQ.md)

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

# **rfq_list**
> RespListRFQs rfq_list(authorization, account_index=account_index, status=status, cursor=cursor, limit=limit)

rfq_list

List RFQs

### Example


```python
import lighter
from lighter.models.resp_list_rfqs import RespListRFQs
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int |  (optional)
    status = 'status_example' # str |  (optional)
    cursor = 'cursor_example' # str |  (optional)
    limit = 56 # int |  (optional)

    try:
        # rfq_list
        api_response = await api_instance.rfq_list(authorization, account_index=account_index, status=status, cursor=cursor, limit=limit)
        print("The response of AccountApi->rfq_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->rfq_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | [optional] 
 **status** | **str**|  | [optional] 
 **cursor** | **str**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**RespListRFQs**](RespListRFQs.md)

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

# **rfq_respond**
> RespRespondToRFQ rfq_respond(authorization, rfq_id, status)

rfq_respond

Respond to RFQ

### Example


```python
import lighter
from lighter.models.resp_respond_to_rfq import RespRespondToRFQ
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    rfq_id = 56 # int | 
    status = 'status_example' # str | 

    try:
        # rfq_respond
        api_response = await api_instance.rfq_respond(authorization, rfq_id, status)
        print("The response of AccountApi->rfq_respond:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->rfq_respond: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **rfq_id** | **int**|  | 
 **status** | **str**|  | 

### Return type

[**RespRespondToRFQ**](RespRespondToRFQ.md)

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

# **rfq_update**
> RespUpdateRFQ rfq_update(authorization, rfq_id, status)

rfq_update

Update RFQ status

### Example


```python
import lighter
from lighter.models.resp_update_rfq import RespUpdateRFQ
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    rfq_id = 56 # int | 
    status = 'status_example' # str | 

    try:
        # rfq_update
        api_response = await api_instance.rfq_update(authorization, rfq_id, status)
        print("The response of AccountApi->rfq_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->rfq_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **rfq_id** | **int**|  | 
 **status** | **str**|  | 

### Return type

[**RespUpdateRFQ**](RespUpdateRFQ.md)

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

# **set_maker_only_api_keys**
> RespSetMakerOnlyApiKeys set_maker_only_api_keys(authorization, account_index, api_key_indexes, auth=auth)

setMakerOnlyApiKeys

Set maker-only API key indexes. This replaces the current list; pass all indexes you want marked as maker-only. Pass [] to clear all maker-only restrictions.

### Example


```python
import lighter
from lighter.models.resp_set_maker_only_api_keys import RespSetMakerOnlyApiKeys
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
    api_instance = lighter.AccountApi(api_client)
    authorization = 'authorization_example' # str | 
    account_index = 56 # int | 
    api_key_indexes = 'api_key_indexes_example' # str | JSON array string of API key indexes, e.g. \\\"[4,5]\\\". Use [] to clear all maker-only restrictions.
    auth = 'auth_example' # str |  (optional)

    try:
        # setMakerOnlyApiKeys
        api_response = await api_instance.set_maker_only_api_keys(authorization, account_index, api_key_indexes, auth=auth)
        print("The response of AccountApi->set_maker_only_api_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->set_maker_only_api_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
 **account_index** | **int**|  | 
 **api_key_indexes** | **str**| JSON array string of API key indexes, e.g. \\\&quot;[4,5]\\\&quot;. Use [] to clear all maker-only restrictions. | 
 **auth** | **str**|  | [optional] 

### Return type

[**RespSetMakerOnlyApiKeys**](RespSetMakerOnlyApiKeys.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens**
> RespGetApiTokens tokens(account_index, authorization=authorization)

tokens

Get read only auth tokens for an account

### Example


```python
import lighter
from lighter.models.resp_get_api_tokens import RespGetApiTokens
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
    api_instance = lighter.AccountApi(api_client)
    account_index = 56 # int | 
    authorization = 'authorization_example' # str |  make required after integ is done (optional)

    try:
        # tokens
        api_response = await api_instance.tokens(account_index, authorization=authorization)
        print("The response of AccountApi->tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **authorization** | **str**|  make required after integ is done | [optional] 

### Return type

[**RespGetApiTokens**](RespGetApiTokens.md)

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

# **tokens_create**
> RespPostApiToken tokens_create(name, account_index, expiry, sub_account_access, authorization=authorization, scopes=scopes)

tokens_create

Create an API token for read-only access

### Example


```python
import lighter
from lighter.models.resp_post_api_token import RespPostApiToken
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
    api_instance = lighter.AccountApi(api_client)
    name = 'name_example' # str | 
    account_index = 56 # int | 
    expiry = 56 # int | 
    sub_account_access = True # bool | 
    authorization = 'authorization_example' # str |  (optional)
    scopes = 'read.*' # str |  (optional) (default to 'read.*')

    try:
        # tokens_create
        api_response = await api_instance.tokens_create(name, account_index, expiry, sub_account_access, authorization=authorization, scopes=scopes)
        print("The response of AccountApi->tokens_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->tokens_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **account_index** | **int**|  | 
 **expiry** | **int**|  | 
 **sub_account_access** | **bool**|  | 
 **authorization** | **str**|  | [optional] 
 **scopes** | **str**|  | [optional] [default to &#39;read.*&#39;]

### Return type

[**RespPostApiToken**](RespPostApiToken.md)

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

# **tokens_revoke**
> RespRevokeApiToken tokens_revoke(token_id, account_index, authorization=authorization)

tokens_revoke

Revoke read only auth token for an account

### Example


```python
import lighter
from lighter.models.resp_revoke_api_token import RespRevokeApiToken
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
    api_instance = lighter.AccountApi(api_client)
    token_id = 56 # int | 
    account_index = 56 # int | 
    authorization = 'authorization_example' # str |  (optional)

    try:
        # tokens_revoke
        api_response = await api_instance.tokens_revoke(token_id, account_index, authorization=authorization)
        print("The response of AccountApi->tokens_revoke:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->tokens_revoke: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_id** | **int**|  | 
 **account_index** | **int**|  | 
 **authorization** | **str**|  | [optional] 

### Return type

[**RespRevokeApiToken**](RespRevokeApiToken.md)

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

