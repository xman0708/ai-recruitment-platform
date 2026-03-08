import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.extractor import extract_resume_info

dummy_resume = """
姓名：李明
电话：13812345678
邮箱：liming@example.com
学历：清华大学 计算机科学与技术 本科 2018-2022
工作经历：
2022-至今 字节跳动 后端工程师，负责Go微服务开发和维护。
专业技能：熟悉Python, Go, Vue, MySQL, Redis。
"""

if __name__ == "__main__":
    print("Testing Zhipu AI Extraction...")
    result = extract_resume_info(dummy_resume)
    print("Extraction Result:")
    print(result)
