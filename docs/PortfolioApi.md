# lighter.PortfolioApi

All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**portfolio_bo_pnl**](PortfolioApi.md#portfolio_bo_pnl) | **GET** /api/v1/portfolio/boPnl | portfolio_boPnl


# **portfolio_bo_pnl**
> RespGetBoPnL portfolio_bo_pnl(account_index, authorization=authorization, auth=auth, event_id=event_id, cursor=cursor, limit=limit)

portfolio_boPnl

Get binary-options realized PnL for an authenticated account, grouped by event and ordered newest event first. cursor is an exclusive event id; event_id returns a single event. Every outcome the account has traded is reported, including markets still open or unsettled, so an entry never disappears as the account trades. Per outcome, total_pnl is all realized PnL so far including settlement, and settlement_pnl is null until the market settles with a position to settle, then the string 0.000000 for an actual zero-PnL settlement. An event's total_pnl is the sum of its listed outcomes. Missing display metadata uses zero/empty values.

### Example


```python
import lighter
from lighter.models.resp_get_bo_pn_l import RespGetBoPnL
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
    api_instance = lighter.PortfolioApi(api_client)
    account_index = 56 # int | 
    authorization = 'authorization_example' # str |  make required after integ is done (optional)
    auth = 'auth_example' # str |  made optional to support header auth clients (optional)
    event_id = 56 # int |  (optional)
    cursor = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # portfolio_boPnl
        api_response = await api_instance.portfolio_bo_pnl(account_index, authorization=authorization, auth=auth, event_id=event_id, cursor=cursor, limit=limit)
        print("The response of PortfolioApi->portfolio_bo_pnl:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->portfolio_bo_pnl: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_index** | **int**|  | 
 **authorization** | **str**|  make required after integ is done | [optional] 
 **auth** | **str**|  made optional to support header auth clients | [optional] 
 **event_id** | **int**|  | [optional] 
 **cursor** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**RespGetBoPnL**](RespGetBoPnL.md)

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

