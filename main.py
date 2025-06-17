#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制台抽奖脚本 - 不含入围未中奖版本
从 txt 文件读取 UID，排序后用设定随机种子抽取 N 名作为中奖者，
分为一等奖、二等奖、三等奖。控制台带加载滚动动画和彩色输出。
"""

import random
import sys
import os
import time

# ========== 配置参数 ==========
FILE_PATH = "uids.txt"       # 每行一个 UID 的文件
N = 25                      # 总抽奖人数（一等奖 + 二等奖 + 三等奖）
SEED = 20080405528491        # 随机种子（可提前公布）
A = 5                        # 一等奖数量
B = 10                       # 二等奖结束索引（[A, B) 为二等奖）
C = 25                     # 三等奖结束索引（[B, C) 为三等奖）；要求 C == N
NO_COLOR = False             # 是否禁用颜色输出
OUTPUT_PATH = "winners.csv"  # 结果输出文件，设为 None 可不导出
LOAD_DELAY = 0               # 每个 UID 加载延迟（秒）
DRAW_CYCLES = 30             # 抽奖滚动动画循环次数
DRAW_DELAY_START = 0.01      # 抽奖动画初始延时
DRAW_DELAY_INCREMENT = 0     # 每轮延迟增量
# ==============================

# ANSI 颜色
ANSI_RESET = "\033[0m"
ANSI_RED = "\033[31m"
ANSI_YELLOW = "\033[33m"
ANSI_GREEN = "\033[32m"
ANSI_CYAN = "\033[36m"
ANSI_BG_RED = "\033[41m"
ANSI_BG_YELLOW = "\033[43m"
ANSI_BG_GREEN = "\033[42m"

def enable_color_on_windows():
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

def read_uids(file_path):
    uids = []
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                uid = int(s)
                uids.append(uid)
            except ValueError:
                print(f"警告：第 {line_no} 行不是有效整数，已跳过: {s}", file=sys.stderr)
    return uids

def print_colored(text, color_code, no_color=False, end="\n"):
    if no_color:
        sys.stdout.write(text + end)
    else:
        sys.stdout.write(f"{color_code}{text}{ANSI_RESET}" + end)
    sys.stdout.flush()

def ascii_bar(counts, labels, total, width=50, no_color=False):
    if total <= 0:
        print("无项目可绘制条形图。")
        return
    ratios = [c / total for c in counts]
    seg_lengths = [int(r * width) for r in ratios]
    used = sum(seg_lengths)
    if used < width:
        for i in range(len(seg_lengths)-1):
            if seg_lengths[i] > 0 and used < width:
                seg_lengths[i] += 1
                used += 1
            if used >= width:
                break
        if used < width:
            seg_lengths[-1] += (width - used)
    elif used > width:
        seg_lengths[-1] = max(0, seg_lengths[-1] - (used - width))
    bar = ""
    for (label, color_bg), length in zip(labels, seg_lengths):
        if length <= 0:
            continue
        if no_color:
            bar += "█" * length
        else:
            bar += f"{color_bg}{' ' * length}{ANSI_RESET}"
    print(f"比例条形图（总 {total}）：")
    print(bar)
    summary_parts = []
    for (label, _), cnt in zip(labels, counts):
        summary_parts.append(f"{label}: {cnt}")
    print("  " + "  ".join(summary_parts))

def animate_loading(uids_sorted):
    print("开始加载 UID 列表...")
    for uid in uids_sorted:
        sys.stdout.write(f"加载 UID: {uid}\n")
        sys.stdout.flush()
        if LOAD_DELAY > 0:
            time.sleep(LOAD_DELAY)
    print("UID 列表加载完成。\n")

def animate_selection(label, final_uid, source_list, color_code=None):
    prefix = f"{label}: "
    delay = DRAW_DELAY_START
    for _ in range(DRAW_CYCLES):
        rnd_uid = random.choice(source_list)
        text = f"{prefix}{rnd_uid}"
        out = f"{color_code}{text}{ANSI_RESET}" if color_code and not NO_COLOR else text
        sys.stdout.write("\r" + " " * (len(prefix) + 20) + "\r")
        sys.stdout.write(out)
        sys.stdout.flush()
        time.sleep(delay)
        delay += DRAW_DELAY_INCREMENT
    final_text = f"{prefix}{final_uid}"
    out = f"{color_code}{final_text}{ANSI_RESET}" if color_code and not NO_COLOR else final_text
    sys.stdout.write("\r" + " " * (len(prefix) + 20) + "\r")
    sys.stdout.write(out + "\n")
    sys.stdout.flush()

def main():
    if not NO_COLOR:
        enable_color_on_windows()

    if not (0 <= A <= B <= C == N):
        print(f"参数错误：必须满足 0 ≤ A ≤ B ≤ C == N。当前 A={A}, B={B}, C={C}, N={N}", file=sys.stderr)
        sys.exit(1)

    uids = read_uids(FILE_PATH)
    total_count = len(uids)
    if total_count == 0:
        print("错误：UID 列表为空。", file=sys.stderr)
        sys.exit(1)
    if N > total_count:
        print(f"错误：抽取数量 N={N} 超过 UID 总数 {total_count}", file=sys.stderr)
        sys.exit(1)

    uids_sorted = sorted(uids)
    print(f"读取到 {total_count} 个 UID，已排序。")
    animate_loading(uids_sorted)

    rnd = random.Random(SEED)
    uids_copy = uids_sorted[:]
    rnd.shuffle(uids_copy)
    winners = uids_copy[:N]

    first_winners = winners[:A]
    second_winners = winners[A:B]
    third_winners = winners[B:C]

    print("开始抽奖动画...\n")
    for idx, uid in enumerate(first_winners, 1):
        animate_selection(f"一等奖 {idx}", uid, uids_sorted, ANSI_RED)
    for idx, uid in enumerate(second_winners, 1):
        animate_selection(f"二等奖 {idx}", uid, uids_sorted, ANSI_YELLOW)
    for idx, uid in enumerate(third_winners, 1):
        animate_selection(f"三等奖 {idx}", uid, uids_sorted, ANSI_GREEN)

    print_colored("\n=== 抽奖结果 ===", ANSI_CYAN, NO_COLOR)
    print(f"随机种子: {SEED}，UID 总数: {total_count}，抽取 N={N} (A={A}, B={B}, C={C})\n")

    if first_winners:
        print_colored(f"一等奖 ({len(first_winners)} 名):", ANSI_RED, NO_COLOR)
        for uid in first_winners:
            print_colored(f"  UID: {uid}", ANSI_RED, NO_COLOR)
        print()

    if second_winners:
        print_colored(f"二等奖 ({len(second_winners)} 名):", ANSI_YELLOW, NO_COLOR)
        for uid in second_winners:
            print_colored(f"  UID: {uid}", ANSI_YELLOW, NO_COLOR)
        print()

    if third_winners:
        print_colored(f"三等奖 ({len(third_winners)} 名):", ANSI_GREEN, NO_COLOR)
        for uid in third_winners:
            print_colored(f"  UID: {uid}", ANSI_GREEN, NO_COLOR)
        print()

    counts = [len(first_winners), len(second_winners), len(third_winners)]
    labels = [
        ("一等奖", ANSI_BG_RED),
        ("二等奖", ANSI_BG_YELLOW),
        ("三等奖", ANSI_BG_GREEN)
    ]
    ascii_bar(counts, labels, total=N, width=50, no_color=NO_COLOR)
    print()

    if OUTPUT_PATH:
        try:
            _, ext = os.path.splitext(OUTPUT_PATH)
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as outf:
                if ext.lower() == '.csv':
                    outf.write("UID,奖项\n")
                for uid in first_winners:
                    outf.write(f"{uid},一等奖\n")
                for uid in second_winners:
                    outf.write(f"{uid},二等奖\n")
                for uid in third_winners:
                    outf.write(f"{uid},三等奖\n")
            print(f"已将结果写入: {OUTPUT_PATH}")
        except Exception as e:
            print(f"写入文件时发生错误: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
