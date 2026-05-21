# RespSyntheticSpotInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**bps_per_day** | **float** |  | 
**expiry_time_ms** | **int** |  | 
**spot_close_ms** | **int** |  | 
**source** | **str** |  | 
**symbol** | **str** |  | 

## Example

```python
from lighter.models.resp_synthetic_spot_info import RespSyntheticSpotInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RespSyntheticSpotInfo from a JSON string
resp_synthetic_spot_info_instance = RespSyntheticSpotInfo.from_json(json)
# print the JSON string representation of the object
print(RespSyntheticSpotInfo.to_json())

# convert the object into a dict
resp_synthetic_spot_info_dict = resp_synthetic_spot_info_instance.to_dict()
# create an instance of RespSyntheticSpotInfo from a dict
resp_synthetic_spot_info_from_dict = RespSyntheticSpotInfo.from_dict(resp_synthetic_spot_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


