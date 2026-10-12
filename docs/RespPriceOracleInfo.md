# RespPriceOracleInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**computed_at_ms** | **int** |  | 
**markets** | [**List[PriceOracleMarket]**](PriceOracleMarket.md) |  | 

## Example

```python
from lighter.models.resp_price_oracle_info import RespPriceOracleInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RespPriceOracleInfo from a JSON string
resp_price_oracle_info_instance = RespPriceOracleInfo.from_json(json)
# print the JSON string representation of the object
print(RespPriceOracleInfo.to_json())

# convert the object into a dict
resp_price_oracle_info_dict = resp_price_oracle_info_instance.to_dict()
# create an instance of RespPriceOracleInfo from a dict
resp_price_oracle_info_from_dict = RespPriceOracleInfo.from_dict(resp_price_oracle_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


