# Leaderboard


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**entries** | [**List[LeaderboardEntry]**](LeaderboardEntry.md) |  | 

## Example

```python
from lighter.models.leaderboard import Leaderboard

# TODO update the JSON string below
json = "{}"
# create an instance of Leaderboard from a JSON string
leaderboard_instance = Leaderboard.from_json(json)
# print the JSON string representation of the object
print(Leaderboard.to_json())

# convert the object into a dict
leaderboard_dict = leaderboard_instance.to_dict()
# create an instance of Leaderboard from a dict
leaderboard_from_dict = Leaderboard.from_dict(leaderboard_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


