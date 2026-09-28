# -*- coding: utf-8 -*-
"""
学生：王健丞
GitHub：wjc123654
分支：dev_wjc123654
日期：2026-09-28
"""


def main():
    print("Hello, Teacher!")
    print("我是王健丞，这是我的作业提交")
    name = input("请输入你的名字：")
    print(f"你好，{name}！欢迎来到编程课堂。")

    print("\n--- 简单计算器 ---")
    a = float(input("请输入第一个数字："))
    b = float(input("请输入第二个数字："))
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} * {b} = {a * b}")
    if b != 0:
        print(f"{a} / {b} = {a / b}")
    else:
        print("除数不能为0")


if __name__ == "__main__":
    main()