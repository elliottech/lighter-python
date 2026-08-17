# LivePointsTotal


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**total_live_points** | **float** |  | 

## Example

```python
from lighter.models.live_points_total import LivePointsTotal

# TODO update the JSON string below
json = "{}"
# create an instance of LivePointsTotal from a JSON string
live_points_total_instance = LivePointsTotal.from_json(json)
# print the JSON string representation of the object
print(LivePointsTotal.to_json())

# convert the object into a dict
live_points_total_dict = live_points_total_instance.to_dict()
# create an instance of LivePointsTotal from a dict
live_points_total_from_dict = LivePointsTotal.from_dict(live_points_total_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


