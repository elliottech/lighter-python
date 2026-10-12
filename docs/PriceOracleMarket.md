# PriceOracleMarket


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** |  | 
**index** | [**PriceOraclePrice**](PriceOraclePrice.md) |  | 
**mark** | [**PriceOraclePrice**](PriceOraclePrice.md) |  | 

## Example

```python
from lighter.models.price_oracle_market import PriceOracleMarket

# TODO update the JSON string below
json = "{}"
# create an instance of PriceOracleMarket from a JSON string
price_oracle_market_instance = PriceOracleMarket.from_json(json)
# print the JSON string representation of the object
print(PriceOracleMarket.to_json())

# convert the object into a dict
price_oracle_market_dict = price_oracle_market_instance.to_dict()
# create an instance of PriceOracleMarket from a dict
price_oracle_market_from_dict = PriceOracleMarket.from_dict(price_oracle_market_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


