# ApprovedIntegrator


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_index** | **int** |  | 
**name** | **str** |  | 
**max_perps_taker_fee** | **int** |  | 
**max_perps_maker_fee** | **int** |  | 
**max_spot_taker_fee** | **int** |  | 
**max_spot_maker_fee** | **int** |  | 
**approval_expiry** | **int** |  Timestamp in milliseconds, after which the integrator is no longer approved | 

## Example

```python
from lighter.models.approved_integrator import ApprovedIntegrator

# TODO update the JSON string below
json = "{}"
# create an instance of ApprovedIntegrator from a JSON string
approved_integrator_instance = ApprovedIntegrator.from_json(json)
# print the JSON string representation of the object
print(ApprovedIntegrator.to_json())

# convert the object into a dict
approved_integrator_dict = approved_integrator_instance.to_dict()
# create an instance of ApprovedIntegrator from a dict
approved_integrator_from_dict = ApprovedIntegrator.from_dict(approved_integrator_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


