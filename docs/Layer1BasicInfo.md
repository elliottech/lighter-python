# Layer1BasicInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**l1_providers** | [**List[L1ProviderInfo]**](L1ProviderInfo.md) |  | 
**l1_providers_health** | **bool** |  | 
**validator_info** | [**List[ValidatorInfo]**](ValidatorInfo.md) |  | 
**contract_addresses** | [**List[ContractAddress]**](ContractAddress.md) |  | 
**latest_l1_generic_block** | **int** |  | 
**latest_l1_governance_block** | **int** |  | 
**latest_l1_desert_block** | **int** |  | 

## Example

```python
from lighter.models.layer1_basic_info import Layer1BasicInfo

# TODO update the JSON string below
json = "{}"
# create an instance of Layer1BasicInfo from a JSON string
layer1_basic_info_instance = Layer1BasicInfo.from_json(json)
# print the JSON string representation of the object
print(Layer1BasicInfo.to_json())

# convert the object into a dict
layer1_basic_info_dict = layer1_basic_info_instance.to_dict()
# create an instance of Layer1BasicInfo from a dict
layer1_basic_info_from_dict = Layer1BasicInfo.from_dict(layer1_basic_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


