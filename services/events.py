"""
Human-readable name for Ping++ Webhook events.
"""

# 上一天 0 点到 23 点 59 分 59 秒的交易金额和交易量统计，在每日 04:00 点左右触发。
DAILY_SUMMARY = 'summary.daily.available'

# 上周一 0 点至上周日 23 点 59 分 59 秒的交易金额和交易量统计，在每周一 04:00 点左右触发。
WEEKLY_SUMMARY = 'summary.weekly.available'

# 上月一日 0 点至上月末 23 点 59 分 59 秒的交易金额和交易量统计，在每月一日 04:00 点左右触发。
MONTHLY_SUMMARY = 'summary.monthly.available'

# 支付对象，支付成功时触发。
CHARGE_SUCCEEDED = 'charge.succeeded'

# 退款对象，退款成功时触发。
REFUND_SUCCEEDED = 'refund.succeeded'
