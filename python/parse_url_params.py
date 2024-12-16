# -*- coding:utf-8 -*-
import pandas as pd
import re
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

# 读取Nginx Access Log文件
def read_nginx_log(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

# 解析日志并提取请求参数，限制每个参数最多保存50个值
def extract_query_params(logs, max_unique_values=50):
    params_dict = defaultdict(set)  # 使用列表来存储值，但会限制长度
    
    for log in logs:
        # Nginx日志格式可能不同，这里假设日志的URL部分在第七个字段（索引6）
        # 根据实际情况调整索引
        parts = log.split()
        if len(parts) > 2:
            url = parts[2]
            url = "http://kuwo.cn?" + url
            parsed_url = urlparse(url)
            print(parsed_url)
            query_params = parse_qs(parsed_url.query)
            # print(query_params)
            for param, values in query_params.items():
                # 由于parse_qs返回的值是一个列表的列表（对于每个参数可能有多个值），
                # 我们将其展平为一个列表，但在这里我们直接添加集合以避免重复。
                for value in values:
                    # 添加值到集合中（自动去重）
                    if len(params_dict[param]) < max_unique_values:
                        params_dict[param].add(value)
    
    # 由于我们直接限制了列表长度，所以不需要额外的过滤步骤
    # 但为了表示有超过50个值的情况，我们可以在最后添加一个特殊标记（可选）
    # 注意：这个特殊标记在实际写入Excel时可能不会被使用，因为它会破坏数据的结构
    # for param in params_dict:
    #     if len(params_dict[param]) == 50:
    #         params_dict[param].append('...')  # 这只是一个示例，实际上不会这样做
    
    # 由于我们不需要这个特殊标记，所以直接返回处理后的字典即可
    # 注意：这里的字典值是一个列表，列表中的元素是参数的值（可能是字符串），且最多50个
    final_params_dict = {param: list(values) for param, values in params_dict.items()}
 
    return final_params_dict

# 将结果写入Excel文件
def write_to_excel(params, output_file):
    # 创建DataFrame
    data = []
    for param, values in params.items():
        for value in values:
            data.append([param, value])
    
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    
    # 写入Excel
    df.to_excel(output_file, index=False)

# 主函数
def main():
    nginx_log_file = 'nginx_access.log'  # 替换为你的Nginx Access Log文件路径
    output_excel_file = 'nginx_params.xlsx'  # 输出Excel文件路径
    
    logs = read_nginx_log(nginx_log_file)
    params = extract_query_params(logs)
    write_to_excel(params, output_excel_file)
    
    print(f"Results have been written to {output_excel_file}")

if __name__ == "__main__":
    main()