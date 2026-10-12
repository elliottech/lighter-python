# PriceOraclePrice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | 
**using_median** | **bool** |  | 
**using_internal_price** | **bool** |  | 
**median_sources** | **List[str]** |  | 
**price_cap_bps** | **float** |  | 
**price_cap_reference_price** | **float** |  cap bounds: ref * (1 -/+ bps / 10000) | 

## Example

```python
from lighter.models.price_oracle_price import PriceOraclePrice

# TODO update the JSON string below
json = "{}"
# create an instance of PriceOraclePrice from a JSON string
price_oracle_price_instance = PriceOraclePrice.from_json(json)
# print the JSON string representation of the object
print(PriceOraclePrice.to_json())

# convert the object into a dict
price_oracle_price_dict = price_oracle_price_instance.to_dict()
# create an instance of PriceOraclePrice from a dict
price_oracle_price_from_dict = PriceOraclePrice.from_dict(price_oracle_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


