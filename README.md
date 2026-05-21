# lighter

Python SDK for [Lighter](https://lighter.xyz) (zkLighter perpetuals exchange).

## Requirements

Python 3.8+

## Installation

```sh
pip install git+https://github.com/elliottech/zklighter-perps-python.git
```

Then:

```python
import lighter
```

## Getting started

```python
import asyncio
import lighter


async def main():
    client = lighter.ApiClient()
    account_api = lighter.AccountApi(client)
    account = await account_api.account(by="index", value="1")
    print(account)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Examples

The [`examples/`](examples) directory contains end-to-end scripts for the
common flows. A few starting points:

- [Read public REST endpoints](examples/get_info.py)
- [Stream order books and account state over websocket](examples/ws.py)
- [Create / modify / cancel an order over HTTP](examples/create_modify_cancel_order_http.py)
- [Create / modify / cancel an order over websocket](examples/create_modify_cancel_order_ws.py)
- [System setup (API key, signer)](examples/system_setup.py)

See [`examples/README.md`](examples/README.md) for the full annotated list.

<!-- AUTOGEN:API_ENDPOINTS -->
All URIs are relative to *https://mainnet.zklighter.elliot.ai*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AccountApi* | [**account**](docs/AccountApi.md#account) | **GET** /api/v1/account | account
*AccountApi* | [**account_limits**](docs/AccountApi.md#account_limits) | **GET** /api/v1/accountLimits | accountLimits
*AccountApi* | [**account_metadata**](docs/AccountApi.md#account_metadata) | **GET** /api/v1/accountMetadata | accountMetadata
*AccountApi* | [**accounts_by_l1_address**](docs/AccountApi.md#accounts_by_l1_address) | **GET** /api/v1/accountsByL1Address | accountsByL1Address
*AccountApi* | [**apikeys**](docs/AccountApi.md#apikeys) | **GET** /api/v1/apikeys | apikeys
*AccountApi* | [**change_account_tier**](docs/AccountApi.md#change_account_tier) | **POST** /api/v1/changeAccountTier | changeAccountTier
*AccountApi* | [**get_maker_only_api_keys**](docs/AccountApi.md#get_maker_only_api_keys) | **GET** /api/v1/getMakerOnlyApiKeys | getMakerOnlyApiKeys
*AccountApi* | [**l1_metadata**](docs/AccountApi.md#l1_metadata) | **GET** /api/v1/l1Metadata | l1Metadata
*AccountApi* | [**lease_options**](docs/AccountApi.md#lease_options) | **GET** /api/v1/leaseOptions | leaseOptions
*AccountApi* | [**leases**](docs/AccountApi.md#leases) | **GET** /api/v1/leases | leases
*AccountApi* | [**liquidations**](docs/AccountApi.md#liquidations) | **GET** /api/v1/liquidations | liquidations
*AccountApi* | [**lit_lease**](docs/AccountApi.md#lit_lease) | **POST** /api/v1/litLease | litLease
*AccountApi* | [**partner_stats**](docs/AccountApi.md#partner_stats) | **GET** /api/v1/partnerStats | partnerStats
*AccountApi* | [**pnl**](docs/AccountApi.md#pnl) | **GET** /api/v1/pnl | pnl
*AccountApi* | [**position_funding**](docs/AccountApi.md#position_funding) | **GET** /api/v1/positionFunding | positionFunding
*AccountApi* | [**public_pools_metadata**](docs/AccountApi.md#public_pools_metadata) | **GET** /api/v1/publicPoolsMetadata | publicPoolsMetadata
*AccountApi* | [**referral_user_referrals**](docs/AccountApi.md#referral_user_referrals) | **GET** /api/v1/referral/userReferrals | userReferrals
*AccountApi* | [**rfq_create**](docs/AccountApi.md#rfq_create) | **POST** /api/v1/rfq/create | rfq_create
*AccountApi* | [**rfq_get**](docs/AccountApi.md#rfq_get) | **GET** /api/v1/rfq/get | rfq_get
*AccountApi* | [**rfq_list**](docs/AccountApi.md#rfq_list) | **GET** /api/v1/rfq/list | rfq_list
*AccountApi* | [**rfq_respond**](docs/AccountApi.md#rfq_respond) | **POST** /api/v1/rfq/respond | rfq_respond
*AccountApi* | [**rfq_update**](docs/AccountApi.md#rfq_update) | **POST** /api/v1/rfq/update | rfq_update
*AccountApi* | [**set_maker_only_api_keys**](docs/AccountApi.md#set_maker_only_api_keys) | **POST** /api/v1/setMakerOnlyApiKeys | setMakerOnlyApiKeys
*AccountApi* | [**tokens**](docs/AccountApi.md#tokens) | **GET** /api/v1/tokens | tokens
*AccountApi* | [**tokens_create**](docs/AccountApi.md#tokens_create) | **POST** /api/v1/tokens/create | tokens_create
*AccountApi* | [**tokens_revoke**](docs/AccountApi.md#tokens_revoke) | **POST** /api/v1/tokens/revoke | tokens_revoke
*AnnouncementApi* | [**announcement**](docs/AnnouncementApi.md#announcement) | **GET** /api/v1/announcement | announcement
*BlockApi* | [**block**](docs/BlockApi.md#block) | **GET** /api/v1/block | block
*BlockApi* | [**blocks**](docs/BlockApi.md#blocks) | **GET** /api/v1/blocks | blocks
*BlockApi* | [**current_height**](docs/BlockApi.md#current_height) | **GET** /api/v1/currentHeight | currentHeight
*BridgeApi* | [**create_intent_address**](docs/BridgeApi.md#create_intent_address) | **POST** /api/v1/createIntentAddress | createIntentAddress
*BridgeApi* | [**deposit_latest**](docs/BridgeApi.md#deposit_latest) | **GET** /api/v1/deposit/latest | deposit_latest
*BridgeApi* | [**deposit_networks**](docs/BridgeApi.md#deposit_networks) | **GET** /api/v1/deposit/networks | deposit_networks
*BridgeApi* | [**fastbridge_info**](docs/BridgeApi.md#fastbridge_info) | **GET** /api/v1/fastbridge/info | fastbridge_info
*BridgeApi* | [**fastwithdraw**](docs/BridgeApi.md#fastwithdraw) | **POST** /api/v1/fastwithdraw | fastwithdraw
*BridgeApi* | [**fastwithdraw_info**](docs/BridgeApi.md#fastwithdraw_info) | **GET** /api/v1/fastwithdraw/info | fastwithdraw_info
*CandlestickApi* | [**candles**](docs/CandlestickApi.md#candles) | **GET** /api/v1/candles | candles
*CandlestickApi* | [**fundings**](docs/CandlestickApi.md#fundings) | **GET** /api/v1/fundings | fundings
*FundingApi* | [**funding_rates**](docs/FundingApi.md#funding_rates) | **GET** /api/v1/funding-rates | funding-rates
*InfoApi* | [**layer1_basic_info**](docs/InfoApi.md#layer1_basic_info) | **GET** /api/v1/layer1BasicInfo | layer1BasicInfo
*InfoApi* | [**synthetic_spot_info**](docs/InfoApi.md#synthetic_spot_info) | **GET** /api/v1/syntheticSpotInfo | syntheticSpotInfo
*InfoApi* | [**system_config**](docs/InfoApi.md#system_config) | **GET** /api/v1/systemConfig | systemConfig
*InfoApi* | [**transfer_fee_info**](docs/InfoApi.md#transfer_fee_info) | **GET** /api/v1/transferFeeInfo | transferFeeInfo
*InfoApi* | [**withdrawal_delay**](docs/InfoApi.md#withdrawal_delay) | **GET** /api/v1/withdrawalDelay | withdrawalDelay
*NotificationApi* | [**notification_ack**](docs/NotificationApi.md#notification_ack) | **POST** /api/v1/notification/ack | notification_ack
*OrderApi* | [**account_active_orders**](docs/OrderApi.md#account_active_orders) | **GET** /api/v1/accountActiveOrders | accountActiveOrders
*OrderApi* | [**account_inactive_orders**](docs/OrderApi.md#account_inactive_orders) | **GET** /api/v1/accountInactiveOrders | accountInactiveOrders
*OrderApi* | [**asset_details**](docs/OrderApi.md#asset_details) | **GET** /api/v1/assetDetails | assetDetails
*OrderApi* | [**exchange_metrics**](docs/OrderApi.md#exchange_metrics) | **GET** /api/v1/exchangeMetrics | exchangeMetrics
*OrderApi* | [**exchange_stats**](docs/OrderApi.md#exchange_stats) | **GET** /api/v1/exchangeStats | exchangeStats
*OrderApi* | [**execute_stats**](docs/OrderApi.md#execute_stats) | **GET** /api/v1/executeStats | executeStats
*OrderApi* | [**export**](docs/OrderApi.md#export) | **GET** /api/v1/export | export
*OrderApi* | [**order_book_details**](docs/OrderApi.md#order_book_details) | **GET** /api/v1/orderBookDetails | orderBookDetails
*OrderApi* | [**order_book_orders**](docs/OrderApi.md#order_book_orders) | **GET** /api/v1/orderBookOrders | orderBookOrders
*OrderApi* | [**order_books**](docs/OrderApi.md#order_books) | **GET** /api/v1/orderBooks | orderBooks
*OrderApi* | [**recent_trades**](docs/OrderApi.md#recent_trades) | **GET** /api/v1/recentTrades | recentTrades
*OrderApi* | [**trades**](docs/OrderApi.md#trades) | **GET** /api/v1/trades | trades
*ReferralApi* | [**referral_create**](docs/ReferralApi.md#referral_create) | **POST** /api/v1/referral/create | referral_create
*ReferralApi* | [**referral_get**](docs/ReferralApi.md#referral_get) | **GET** /api/v1/referral/get | referral_get
*ReferralApi* | [**referral_kickback_update**](docs/ReferralApi.md#referral_kickback_update) | **POST** /api/v1/referral/kickback/update | referral_kickback_update
*ReferralApi* | [**referral_points**](docs/ReferralApi.md#referral_points) | **GET** /api/v1/referral/points | referral_points
*ReferralApi* | [**referral_update**](docs/ReferralApi.md#referral_update) | **POST** /api/v1/referral/update | referral_update
*ReferralApi* | [**referral_use**](docs/ReferralApi.md#referral_use) | **POST** /api/v1/referral/use | referral_use
*RootApi* | [**info**](docs/RootApi.md#info) | **GET** /info | info
*RootApi* | [**status**](docs/RootApi.md#status) | **GET** / | status
*TokenlistApi* | [**tokenlist**](docs/TokenlistApi.md#tokenlist) | **GET** /api/v1/tokenlist | tokenlist
*TransactionApi* | [**account_txs**](docs/TransactionApi.md#account_txs) | **GET** /api/v1/accountTxs | accountTxs
*TransactionApi* | [**block_txs**](docs/TransactionApi.md#block_txs) | **GET** /api/v1/blockTxs | blockTxs
*TransactionApi* | [**deposit_history**](docs/TransactionApi.md#deposit_history) | **GET** /api/v1/deposit/history | deposit_history
*TransactionApi* | [**next_nonce**](docs/TransactionApi.md#next_nonce) | **GET** /api/v1/nextNonce | nextNonce
*TransactionApi* | [**send_tx**](docs/TransactionApi.md#send_tx) | **POST** /api/v1/sendTx | sendTx
*TransactionApi* | [**send_tx_batch**](docs/TransactionApi.md#send_tx_batch) | **POST** /api/v1/sendTxBatch | sendTxBatch
*TransactionApi* | [**set_account_metadata**](docs/TransactionApi.md#set_account_metadata) | **POST** /api/v1/setAccountMetadata | setAccountMetadata
*TransactionApi* | [**transfer_history**](docs/TransactionApi.md#transfer_history) | **GET** /api/v1/transfer/history | transfer_history
*TransactionApi* | [**tx**](docs/TransactionApi.md#tx) | **GET** /api/v1/tx | tx
*TransactionApi* | [**tx_from_l1_tx_hash**](docs/TransactionApi.md#tx_from_l1_tx_hash) | **GET** /api/v1/txFromL1TxHash | txFromL1TxHash
*TransactionApi* | [**txs**](docs/TransactionApi.md#txs) | **GET** /api/v1/txs | txs
*TransactionApi* | [**withdraw_history**](docs/TransactionApi.md#withdraw_history) | **GET** /api/v1/withdraw/history | withdraw_history
<!-- /AUTOGEN:API_ENDPOINTS -->

<!-- AUTOGEN:MODELS -->
 - [Account](docs/Account.md)
 - [AccountApiKeys](docs/AccountApiKeys.md)
 - [AccountAsset](docs/AccountAsset.md)
 - [AccountLimits](docs/AccountLimits.md)
 - [AccountMetadata](docs/AccountMetadata.md)
 - [AccountMetadatas](docs/AccountMetadatas.md)
 - [AccountPnL](docs/AccountPnL.md)
 - [AccountPosition](docs/AccountPosition.md)
 - [Announcement](docs/Announcement.md)
 - [Announcements](docs/Announcements.md)
 - [ApiKey](docs/ApiKey.md)
 - [ApiToken](docs/ApiToken.md)
 - [ApprovedIntegrator](docs/ApprovedIntegrator.md)
 - [Asset](docs/Asset.md)
 - [AssetDetails](docs/AssetDetails.md)
 - [Block](docs/Block.md)
 - [Blocks](docs/Blocks.md)
 - [BridgeSupportedNetwork](docs/BridgeSupportedNetwork.md)
 - [BridgeSupportedNetworks](docs/BridgeSupportedNetworks.md)
 - [Candle](docs/Candle.md)
 - [Candles](docs/Candles.md)
 - [ContractAddress](docs/ContractAddress.md)
 - [CreateIntentAddressResp](docs/CreateIntentAddressResp.md)
 - [CurrentHeight](docs/CurrentHeight.md)
 - [DailyReturn](docs/DailyReturn.md)
 - [Deposit](docs/Deposit.md)
 - [DepositHistory](docs/DepositHistory.md)
 - [DepositHistoryItem](docs/DepositHistoryItem.md)
 - [DetailedAccount](docs/DetailedAccount.md)
 - [DetailedAccounts](docs/DetailedAccounts.md)
 - [EnrichedTx](docs/EnrichedTx.md)
 - [ExchangeMetric](docs/ExchangeMetric.md)
 - [ExchangeStats](docs/ExchangeStats.md)
 - [ExecuteStat](docs/ExecuteStat.md)
 - [ExportData](docs/ExportData.md)
 - [Funding](docs/Funding.md)
 - [FundingRate](docs/FundingRate.md)
 - [FundingRates](docs/FundingRates.md)
 - [Fundings](docs/Fundings.md)
 - [L1Metadata](docs/L1Metadata.md)
 - [L1ProviderInfo](docs/L1ProviderInfo.md)
 - [Layer1BasicInfo](docs/Layer1BasicInfo.md)
 - [LeaseEntry](docs/LeaseEntry.md)
 - [LeaseOptionEntry](docs/LeaseOptionEntry.md)
 - [LiqTrade](docs/LiqTrade.md)
 - [Liquidation](docs/Liquidation.md)
 - [LiquidationInfo](docs/LiquidationInfo.md)
 - [LiquidationInfos](docs/LiquidationInfos.md)
 - [MarketConfig](docs/MarketConfig.md)
 - [NextNonce](docs/NextNonce.md)
 - [Order](docs/Order.md)
 - [OrderBook](docs/OrderBook.md)
 - [OrderBookDetails](docs/OrderBookDetails.md)
 - [OrderBookOrders](docs/OrderBookOrders.md)
 - [OrderBookStats](docs/OrderBookStats.md)
 - [OrderBooks](docs/OrderBooks.md)
 - [Orders](docs/Orders.md)
 - [PartnerStats](docs/PartnerStats.md)
 - [PendingUnlock](docs/PendingUnlock.md)
 - [PerpsOrderBookDetail](docs/PerpsOrderBookDetail.md)
 - [PnLEntry](docs/PnLEntry.md)
 - [PositionFunding](docs/PositionFunding.md)
 - [PositionFundings](docs/PositionFundings.md)
 - [PublicPoolInfo](docs/PublicPoolInfo.md)
 - [PublicPoolMetadata](docs/PublicPoolMetadata.md)
 - [PublicPoolShare](docs/PublicPoolShare.md)
 - [RFQEntry](docs/RFQEntry.md)
 - [RFQMetadata](docs/RFQMetadata.md)
 - [RFQResponseEntry](docs/RFQResponseEntry.md)
 - [Referral](docs/Referral.md)
 - [ReferralCode](docs/ReferralCode.md)
 - [ReferralPointEntry](docs/ReferralPointEntry.md)
 - [ReferralPoints](docs/ReferralPoints.md)
 - [ReqSetAccountMetadata](docs/ReqSetAccountMetadata.md)
 - [RespChangeAccountTier](docs/RespChangeAccountTier.md)
 - [RespCreateRFQ](docs/RespCreateRFQ.md)
 - [RespGetApiTokens](docs/RespGetApiTokens.md)
 - [RespGetExchangeMetrics](docs/RespGetExchangeMetrics.md)
 - [RespGetExecuteStats](docs/RespGetExecuteStats.md)
 - [RespGetFastBridgeInfo](docs/RespGetFastBridgeInfo.md)
 - [RespGetFastwithdrawalInfo](docs/RespGetFastwithdrawalInfo.md)
 - [RespGetLeaseOptions](docs/RespGetLeaseOptions.md)
 - [RespGetLeases](docs/RespGetLeases.md)
 - [RespGetMakerOnlyApiKeys](docs/RespGetMakerOnlyApiKeys.md)
 - [RespGetRFQ](docs/RespGetRFQ.md)
 - [RespListRFQs](docs/RespListRFQs.md)
 - [RespPostApiToken](docs/RespPostApiToken.md)
 - [RespPublicPoolsMetadata](docs/RespPublicPoolsMetadata.md)
 - [RespRespondToRFQ](docs/RespRespondToRFQ.md)
 - [RespRevokeApiToken](docs/RespRevokeApiToken.md)
 - [RespSendTx](docs/RespSendTx.md)
 - [RespSendTxBatch](docs/RespSendTxBatch.md)
 - [RespSetMakerOnlyApiKeys](docs/RespSetMakerOnlyApiKeys.md)
 - [RespSyntheticSpotInfo](docs/RespSyntheticSpotInfo.md)
 - [RespUpdateKickback](docs/RespUpdateKickback.md)
 - [RespUpdateRFQ](docs/RespUpdateRFQ.md)
 - [RespUpdateReferralCode](docs/RespUpdateReferralCode.md)
 - [RespWithdrawalDelay](docs/RespWithdrawalDelay.md)
 - [ResultCode](docs/ResultCode.md)
 - [RiskInfo](docs/RiskInfo.md)
 - [RiskParameters](docs/RiskParameters.md)
 - [SharePrice](docs/SharePrice.md)
 - [SimpleOrder](docs/SimpleOrder.md)
 - [SlippageResult](docs/SlippageResult.md)
 - [SpotOrderBookDetail](docs/SpotOrderBookDetail.md)
 - [Status](docs/Status.md)
 - [Strategy](docs/Strategy.md)
 - [SubAccounts](docs/SubAccounts.md)
 - [SystemConfig](docs/SystemConfig.md)
 - [Token](docs/Token.md)
 - [TokenList](docs/TokenList.md)
 - [Trade](docs/Trade.md)
 - [TradeStats](docs/TradeStats.md)
 - [Trades](docs/Trades.md)
 - [TransferFeeInfo](docs/TransferFeeInfo.md)
 - [TransferHistory](docs/TransferHistory.md)
 - [TransferHistoryItem](docs/TransferHistoryItem.md)
 - [Tx](docs/Tx.md)
 - [TxHash](docs/TxHash.md)
 - [Txs](docs/Txs.md)
 - [UserReferrals](docs/UserReferrals.md)
 - [ValidatorInfo](docs/ValidatorInfo.md)
 - [WithdrawHistory](docs/WithdrawHistory.md)
 - [WithdrawHistoryItem](docs/WithdrawHistoryItem.md)
 - [ZkLighterInfo](docs/ZkLighterInfo.md)


<a id="documentation-for-authorization"></a>
<!-- /AUTOGEN:MODELS -->
