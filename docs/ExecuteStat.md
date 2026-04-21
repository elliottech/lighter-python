# ExecuteStat


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **int** |  | [optional] 
**slippage** | [**List[SlippageResult]**](SlippageResult.md) |  | [optional] 

## Example

```python
from lighter.models.execute_stat import ExecuteStat

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteStat from a JSON string
execute_stat_instance = ExecuteStat.from_json(json)
# print the JSON string representation of the object
print(ExecuteStat.to_json())

# convert the object into a dict
execute_stat_dict = execute_stat_instance.to_dict()
# create an instance of ExecuteStat from a dict
execute_stat_from_dict = ExecuteStat.from_dict(execute_stat_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


