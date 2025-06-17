#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简洁版抽奖脚本（适合公布算法验证用）
功能：
- 从 uids.txt 读取 UID（每行一个整数）
- 固定随机种子进行抽奖
- 分配一二三等奖
- 所有参数均硬编码，结果可复现
"""

import random
import os
import sys

# ========== 配置参数 ==========
FILE_PATH = "uids.txt"  # UID 文件，每行一个 UID（整数）
SEED = 20080405528491   # 随机种子（可提前公布）
A = 5                   # 一等奖人数
B = 10                  # 二等奖结束索引（[A, B)）
C = 25                 # 三等奖结束索引（[B, C)）
# =============================

def read_uids(file_path):
    """读取 UID 列表（每行一个整数）"""
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)
    uids = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                uid = int(s)
                uids.append(uid)
            except ValueError:
                print(f"警告：第 {line_no} 行无效 UID，已跳过: {s}", file=sys.stderr)
    return uids

def main():
    # 参数校验
    if not (0 <= A <= B <= C):
        print(f"错误：参数关系必须满足 0 ≤ A ≤ B ≤ C，当前 A={A}, B={B}, C={C}", file=sys.stderr)
        sys.exit(1)

    uids = read_uids(FILE_PATH)
    total = len(uids)
    if total == 0:
        print("错误：UID 列表为空", file=sys.stderr)
        sys.exit(1)
    if C > total:
        print(f"错误：抽奖总人数 C={C} 大于 UID 总数 {total}", file=sys.stderr)
        sys.exit(1)

    # 排序 + 洗牌
    sorted_uids = sorted(uids)
    rnd = random.Random(SEED)
    rnd.shuffle(sorted_uids)
    winners = sorted_uids[:C]

    # 分组
    first = winners[:A]
    second = winners[A:B]
    third = winners[B:C]

    # 输出
    print("=== 抽奖结果 ===")
    print(f"随机种子: {SEED}")
    print(f"参与者总数: {total}，抽取前 {C} 人中奖\n")

    print(f"一等奖（{len(first)} 名）:")
    for uid in first:
        print(f"  UID: {uid}")
    print()

    print(f"二等奖（{len(second)} 名）:")
    for uid in second:
        print(f"  UID: {uid}")
    print()

    print(f"三等奖（{len(third)} 名）:")
    for uid in third:
        print(f"  UID: {uid}")
    print()

if __name__ == "__main__":
    main()
