# PnlLeaderboard


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**entries** | [**List[PnlLeaderboardEntry]**](PnlLeaderboardEntry.md) |  | 
**total** | **int** |  | 
**updated_at** | **int** |  | 

## Example

```python
from lighter.models.pnl_leaderboard import PnlLeaderboard

# TODO update the JSON string below
json = "{}"
# create an instance of PnlLeaderboard from a JSON string
pnl_leaderboard_instance = PnlLeaderboard.from_json(json)
# print the JSON string representation of the object
print(PnlLeaderboard.to_json())

# convert the object into a dict
pnl_leaderboard_dict = pnl_leaderboard_instance.to_dict()
# create an instance of PnlLeaderboard from a dict
pnl_leaderboard_from_dict = PnlLeaderboard.from_dict(pnl_leaderboard_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


