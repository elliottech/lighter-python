# BridgeSupportedNetworks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**networks** | [**List[BridgeSupportedNetwork]**](BridgeSupportedNetwork.md) |  | 

## Example

```python
from lighter.models.bridge_supported_networks import BridgeSupportedNetworks

# TODO update the JSON string below
json = "{}"
# create an instance of BridgeSupportedNetworks from a JSON string
bridge_supported_networks_instance = BridgeSupportedNetworks.from_json(json)
# print the JSON string representation of the object
print(BridgeSupportedNetworks.to_json())

# convert the object into a dict
bridge_supported_networks_dict = bridge_supported_networks_instance.to_dict()
# create an instance of BridgeSupportedNetworks from a dict
bridge_supported_networks_from_dict = BridgeSupportedNetworks.from_dict(bridge_supported_networks_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


