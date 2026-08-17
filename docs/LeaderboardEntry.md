# LeaderboardEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**l1_address** | **str** |  | 
**points** | **float** |  | 
**entry** | **int** |  | 
**entry_id** | **int** |  | 
**metadata** | **str** |  | 

## Example

```python
from lighter.models.leaderboard_entry import LeaderboardEntry

# TODO update the JSON string below
json = "{}"
# create an instance of LeaderboardEntry from a JSON string
leaderboard_entry_instance = LeaderboardEntry.from_json(json)
# print the JSON string representation of the object
print(LeaderboardEntry.to_json())

# convert the object into a dict
leaderboard_entry_dict = leaderboard_entry_instance.to_dict()
# create an instance of LeaderboardEntry from a dict
leaderboard_entry_from_dict = LeaderboardEntry.from_dict(leaderboard_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


