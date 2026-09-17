"""Decode asset metadata from legacy and native-domain API responses."""

import pytest

from lighter.models.asset import Asset
from lighter.models.asset_details import AssetDetails


@pytest.mark.parametrize("metadata", [
    {"l1_decimals": 6},
    {"canonical_domain": 1, "l1_decimals": 18, "evm_token": "0x" + "11" * 20},
    {"canonical_domain": 2, "evm_token": "0x" + "00" * 20},
    {"canonical_domain": 3, "evm_decimals": 18, "evm_token": "0x" + "22" * 20},
    {"canonical_domain": 3, "evm_decimals": 0, "evm_token": "0x" + "00" * 20},
])
def test_asset_metadata_response(metadata):
    payload = {
        "asset_id": 7, "symbol": "TOKEN", "decimals": 8,
        "min_transfer_amount": "0.01", "min_withdrawal_amount": "0.01",
        "margin_mode": "disabled", "index_price": "2.500000000",
        "l1_address": "0x" + "00" * 20, "price_decimals": 9,
        "global_supply_cap": "0", "user_supply_cap": "0", "total_supplied": "0",
        "liquidation_fee": "0", "liquidation_threshold": "0", "loan_to_value": "0",
        "liquidation_factor": "0", "multiplier": "1", **metadata,
    }
    response = AssetDetails.from_dict({"code": 200, "asset_details": [payload]})
    asset = response.asset_details[0]
    # Direct model validation must support the same field presence as HTTP decoding.
    validated = Asset.model_validate(payload)
    for field in ("l1_decimals", "evm_decimals", "canonical_domain", "evm_token"):
        assert getattr(asset, field) == metadata.get(field)
        assert getattr(validated, field) == metadata.get(field)
        assert (field in asset.to_dict()) == (field in metadata)
    assert asset.to_dict() == payload
    assert asset.additional_properties == {}
