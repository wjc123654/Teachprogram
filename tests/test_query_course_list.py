# -*- coding: utf-8 -*-
"""
查询课程列表接口测试
====================
接口地址：GET /api/clues/course/list
需求来源：客达天下API文档

测试用例：
  1. 不带条件查询全部课程 → 期望 code=200, total>0, rows 非空
  2. 按课程名称精确查询 → 期望 code=200, 返回匹配的课程
  3. 查询不存在的课程名称 → 期望 code=200, total=0, rows=[]
  4. 未登录查询课程列表 → 期望 code=401
  5. 按学科查询课程 → 期望 code=200, 返回对应学科的课程
  6. 按适用人群查询课程 → 期望 code=200, 返回对应的课程
"""
import time
import pytest


class TestQueryCourseList:
    """查询课程列表接口测试类。"""

    # ==================== 正向用例 ====================
    def test_query_all_courses(self, logged_in_client):
        """用例1：不带条件查询全部课程。

        前置条件：已登录，系统中存在课程数据
        预期结果：HTTP 200，code=200，total>0，rows 非空列表
        """
        response = logged_in_client.get_course_list()

        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        data = response.json()
        assert data["code"] == 200, f"业务码异常: {data}"
        assert data["msg"] == "查询成功", f"返回消息异常: {data['msg']}"
        assert data["total"] > 0, f"系统中应有课程数据, total={data['total']}"
        assert isinstance(data["rows"], list), "rows 应为列表"
        assert len(data["rows"]) > 0, "rows 不应为空"

    def test_query_by_name(self, logged_in_client):
        """用例2：按课程名称精确查询。

        前置条件：已登录，先创建一门课程再查
        预期结果：code=200，返回包含该名称的课程
        """
        # 先创建一门课程，确保能查到
        course_name = f"查询测试课程_{int(time.time())}"
        add_resp = logged_in_client.add_course(
            name=course_name,
            subject="6",
            price=899,
            applicable_person="2",
            info="按名称查询测试",
        )
        assert add_resp.json()["code"] == 200, "前置: 创建课程失败"

        # 按名称查询
        response = logged_in_client.get_course_list(name=course_name)

        data = response.json()
        assert data["code"] == 200
        assert data["total"] >= 1, f"应查到刚创建的课程, total={data['total']}"
        assert data["rows"][0]["name"] == course_name, "课程名称不匹配"

    def test_query_nonexistent_course(self, logged_in_client):
        """用例3：查询不存在的课程名称。

        前置条件：已登录
        预期结果：code=200，total=0，rows=[]
        """
        response = logged_in_client.get_course_list(name="这是一个不存在的课程名称ABC123XYZ")

        data = response.json()
        assert data["code"] == 200
        assert data["total"] == 0, f"不存在的课程应返回total=0, 实际={data['total']}"
        assert data["rows"] == [], f"rows应为空列表, 实际={data['rows']}"

    # ==================== 反向用例 ====================
    def test_query_not_logged_in(self, client):
        """用例4：未登录查询课程列表。

        前置条件：未登录
        预期结果：业务 code=401
        """
        response = client.get_course_list()

        data = response.json()
        assert data["code"] == 401, f"未登录时应返回401, 实际: {data}"

    # ==================== 条件组合用例 ====================
    def test_query_by_subject(self, logged_in_client):
        """用例5：按课程学科查询。

        前置条件：已登录
        预期结果：code=200，返回对应学科的课程
        """
        response = logged_in_client.get_course_list(subject="6")

        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "查询成功"
        if data["total"] > 0:
            for course in data["rows"]:
                assert course["subject"] == "6", f"学科不匹配: {course['subject']}"

    def test_query_by_applicable_person(self, logged_in_client):
        """用例6：按适用人群查询。

        前置条件：已登录
        预期结果：code=200，返回对应的课程
        """
        response = logged_in_client.get_course_list(applicable_person="2")

        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "查询成功"
        if data["total"] > 0:
            for course in data["rows"]:
                assert course["applicablePerson"] == "2", \
                    f"适用人群不匹配: {course.get('applicablePerson')}"
