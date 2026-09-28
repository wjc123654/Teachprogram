# 课程管理接口测试用例

**学生：** 王健丞  
**GitHub：** wjc123654  
**系统地址：** http://kdtx-test.itheima.net  
**日期：** 2026-09-28

---

## 一、新增课程接口（POST /api/clues/course）

| 用例编号 | 用例标题 | 前置条件 | 请求参数 | 预期结果 | 优先级 |
|---------|---------|---------|---------|---------|-------|
| TC-ADD-01 | 正常新增课程 | 已登录 | name=测试课程_xxx, subject=6, price=899, applicablePerson=2, info=测试 | code=200, msg="操作成功" | 高 |
| TC-ADD-02 | 未登录新增课程 | 未登录 | 同上 | code=401, msg包含"认证失败" | 高 |
| TC-ADD-03 | 缺少必填字段-课程名称 | 已登录 | name="", subject=6, price=899, applicablePerson=2 | code=500, msg="操作失败" | 中 |
| TC-ADD-04 | 缺少必填字段-课程学科 | 已登录 | name=测试, subject="", price=899, applicablePerson=2 | code=500, msg="操作失败" | 中 |
| TC-ADD-05 | 缺少必填字段-课程价格 | 已登录 | name=测试, subject=6, price="", applicablePerson=2 | code=500, msg="操作失败" | 中 |
| TC-ADD-06 | 缺少必填字段-适用人群 | 已登录 | name=测试, subject=6, price=899, applicablePerson="" | code=500, msg="操作失败" | 中 |

---

## 二、查询课程列表接口（GET /api/clues/course/list）

| 用例编号 | 用例标题 | 前置条件 | 请求参数 | 预期结果 | 优先级 |
|---------|---------|---------|---------|---------|-------|
| TC-QUERY-01 | 不带条件查询全部课程 | 已登录，系统有数据 | 无 | code=200, total>0, rows非空 | 高 |
| TC-QUERY-02 | 按课程名称查询 | 已登录，先创建课程 | name=查询测试课程_xxx | code=200, total>=1, rows[0].name匹配 | 高 |
| TC-QUERY-03 | 查询不存在的课程名称 | 已登录 | name=不存在的课程ABC123 | code=200, total=0, rows=[] | 中 |
| TC-QUERY-04 | 未登录查询课程列表 | 未登录 | 无 | code=401, msg包含"认证失败" | 高 |
| TC-QUERY-05 | 按学科查询课程 | 已登录 | subject=6 | code=200, 返回学科=6的课程 | 中 |
| TC-QUERY-06 | 按适用人群查询课程 | 已登录 | applicablePerson=2 | code=200, 返回适用人群=2的课程 | 中 |

---

## 三、测试代码说明

### 运行环境
- Python >= 3.12
- pytest >= 9.1.1
- requests >= 2.34.2

### 文件结构
```
Teachprogram/
├── src/
│   └── apiclient.py          # API 客户端封装类
├── tests/
│   ├── conftest.py            # pytest 共享夹具
│   ├── test_add_course.py     # 新增课程接口测试（本次提交）
│   ├── test_query_course_list.py  # 查询课程列表接口测试（本次提交）
│   └── ...
└── pyproject.toml
```

### 运行方式
```bash
# 运行全部测试
pytest tests/ -v

# 只运行新增课程测试
pytest tests/test_add_course.py -v

# 只运行查询课程列表测试
pytest tests/test_query_course_list.py -v
```

### 夹具依赖
- `client`：未登录的 API 客户端（用于反向用例）
- `logged_in_client`：已登录的 API 客户端（用于正向用例）
- 以上夹具定义在 `tests/conftest.py` 中，自动加载
