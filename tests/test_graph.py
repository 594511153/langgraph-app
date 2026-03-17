from protocol_review.graph import review_protocol


def test_review_protocol_pass_case():
    result = review_protocol(
        protocol_name="OrderCreateProtocol",
        identifiers=["order_id", "user_id", "total_amount"],
        description="该协议用于创建订单，字段包括订单ID、用户ID、金额。协议约束包含金额必须大于0，错误处理覆盖字段缺失和类型错误。",
    )

    assert result["summary"]["passed"] is True
    assert result["reviews"]["name_naming"]["compliant"] is True


def test_review_protocol_fail_case():
    result = review_protocol(
        protocol_name="bad-name",
        identifiers=["A", "A"],
        description="太短",
    )

    assert result["summary"]["passed"] is False
    assert len(result["summary"]["failed_items"]) >= 1
