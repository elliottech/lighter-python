# PnlLeaderboardEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rank** | **int** |  | 
**l1_address** | **str** |  | 
**account_value** | **float** |  | 
**pnl** | **float** |  | 
**roi** | **float** |  | 
**volume** | **float** |  | 

## Example

```python
from lighter.models.pnl_leaderboard_entry import PnlLeaderboardEntry

# TODO update the JSON string below
json = "{}"
# create an instance of PnlLeaderboardEntry from a JSON string
pnl_leaderboard_entry_instance = PnlLeaderboardEntry.from_json(json)
# print the JSON string representation of the object
print(PnlLeaderboardEntry.to_json())

# convert the object into a dict
pnl_leaderboard_entry_dict = pnl_leaderboard_entry_instance.to_dict()
# create an instance of PnlLeaderboardEntry from a dict
pnl_leaderboard_entry_from_dict = PnlLeaderboardEntry.from_dict(pnl_leaderboard_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


