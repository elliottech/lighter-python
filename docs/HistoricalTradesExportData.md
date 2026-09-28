# HistoricalTradesExportData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | [optional] 
**data_url** | **str** |  | 
**expires_at** | **str** |  | 

## Example

```python
from lighter.models.historical_trades_export_data import HistoricalTradesExportData

# TODO update the JSON string below
json = "{}"
# create an instance of HistoricalTradesExportData from a JSON string
historical_trades_export_data_instance = HistoricalTradesExportData.from_json(json)
# print the JSON string representation of the object
print(HistoricalTradesExportData.to_json())

# convert the object into a dict
historical_trades_export_data_dict = historical_trades_export_data_instance.to_dict()
# create an instance of HistoricalTradesExportData from a dict
historical_trades_export_data_from_dict = HistoricalTradesExportData.from_dict(historical_trades_export_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


