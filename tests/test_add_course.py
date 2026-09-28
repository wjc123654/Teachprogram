# -*- coding: utf-8 -*-
"""
新增课程接口测试
================
接口地址：POST /api/clues/course
需求来源：客达天下API文档

测试用例：
  1. 正常新增课程（所有必填字段都填写）→ 期望 code=200, msg="操作成功"
  2. 未登录新增课程（不带 Authorization 头）→ 期望 code=401
  3. 缺少必填字段-不传课程名称 → 期望 code=500, msg="操作失败"
  4. 缺少必填字段-不传课程学科 → 期望 code=500, msg="操作失败"
  5. 缺少必填字段-不传课程价格 → 期望 code=500, msg="操作失败"
  6. 缺少必填字段-不传适用人群 → 期望 code=500, msg="操作失败"
"""
import time
import pytest


class TestAddCourse:
    """新增课程接口测试类。"""

    # ==================== 正向用例 ====================
    def test_add_course_success(self, logged_in_client):
        """用例1：正常新增课程，所有必填字段都填写。

        前置条件：已登录
        预期结果：HTTP 200，业务 code=200，msg="操作成功"
        """
        course_name = f"测试课程_{int(time.time())}"

        response = logged_in_client.add_course(
            name=course_name,
            subject="6",
            price=899,
            applicable_person="2",
            info="新增课程接口测试-正常用例",
        )

        # 断言1：HTTP 状态码
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 断言2：业务状态码
        data = response.json()
        assert data["code"] == 200, f"业务码异常: {data}"

        # 断言3：返回消息
        assert data["msg"] == "操作成功", f"返回消息异常: {data['msg']}"

    # ==================== 反向用例 ====================
    def test_add_course_not_logged_in(self, client):
        """用例2：未登录新增课程，不带 Authorization 请求头。

        前置条件：未登录（使用 client 夹具而非 logged_in_client）
        预期结果：HTTP 200，业务 code=401
        """
        response = client.add_course(
            name="未登录测试课程",
            subject="6",
            price=100,
            applicable_person="2",
            info="不应创建成功",
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 401, f"未登录时应返回401, 实际: {data}"

    def test_add_course_missing_name(self, logged_in_client):
        """用例3：缺少必填字段-不传课程名称。

        前置条件：已登录
        预期结果：业务 code=500, msg="操作失败"
        """
        response = logged_in_client.add_course(
            name="",
            subject="6",
            price=899,
            applicable_person="2",
            info="缺少课程名称",
        )

        data = response.json()
        assert data["code"] == 500, f"缺少名称应返回500, 实际: {data}"
        assert data["msg"] == "操作失败", f"消息异常: {data['msg']}"

    def test_add_course_missing_subject(self, logged_in_client):
        """用例4：缺少必填字段-不传课程学科。

        前置条件：已登录
        预期结果：业务 code=500, msg="操作失败"
        """
        response = logged_in_client.add_course(
            name="缺少学科测试",
            subject="",
            price=899,
            applicable_person="2",
            info="缺少课程学科",
        )

        data = response.json()
        assert data["code"] == 500, f"缺少学科应返回500, 实际: {data}"

    def test_add_course_missing_price(self, logged_in_client):
        """用例5：缺少必填字段-不传课程价格。

        前置条件：已登录
        预期结果：业务 code=500, msg="操作失败"
        """
        response = logged_in_client.add_course(
            name="缺少价格测试",
            subject="6",
            price="",
            applicable_person="2",
            info="缺少课程价格",
        )

        data = response.json()
        assert data["code"] == 500, f"缺少价格应返回500, 实际: {data}"

    def test_add_course_missing_applicable_person(self, logged_in_client):
        """用例6：缺少必填字段-不传适用人群。

        前置条件：已登录
        预期结果：业务 code=500, msg="操作失败"
        """
        response = logged_in_client.add_course(
            name="缺少适用人群测试",
            subject="6",
            price=899,
            applicable_person="",
            info="缺少适用人群",
        )

        data = response.json()
        assert data["code"] == 500, f"缺少适用人群应返回500, 实际: {data}"
