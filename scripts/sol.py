import csv
import json
from collections import defaultdict
from datetime import datetime

def parse_time(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def parse_ctfd_data():
    light_time = datetime.strptime("07:11:30", "%H:%M:%S").time()
    
    # 读取CSV文件
    users = read_csv('data/TestCTF-users.csv')
    submissions = read_csv('data/TestCTF-submissions.csv')
    challenges = read_csv('data/TestCTF-challenges.csv')

    # 计算总题目数
    total_challenges = len(challenges)

    # 创建题目分值映射
    challenge_values = {c['id']: int(c['value']) for c in challenges}

    # 统计每个用户的解题情况
    user_stats = defaultdict(lambda: {
        'solved': set(), 
        'score': 0,
        'light_submissions': [],  # 存储黑灯后的正确提交
        'max_submit': 0,         # 黑灯后的总提交次数
    })
    
    # 处理提交记录
    for sub in submissions:
        user_id = sub['user_id']
        sub_time = parse_time(sub['date']).time()
        
        # 黑灯前的提交
        if sub_time < light_time:
            if sub['type'] == 'correct':
                challenge_id = sub['challenge_id']
                user_stats[user_id]['solved'].add(challenge_id)
                user_stats[user_id]['score'] += challenge_values[challenge_id]
        # 黑灯后的提交
        else:
            user_stats[user_id]['max_submit'] += 1
            if sub['type'] == 'correct':
                challenge_id = sub['challenge_id']
                user_stats[user_id]['light_submissions'].append(
                    (user_stats[user_id]['max_submit'], 
                     challenge_values[challenge_id])
                )

    # 格式化输出结果
    result = []
    for user in users:
        if user['type'] == 'user':
            stats = user_stats[user['id']]
            result.append({
                'name': user['name'],
                'solved': len(stats['solved']),
                'total': total_challenges,
                'ctfScore': stats['score'],
                'kohScore': 0,
                'totalScore': stats['score'],
                'lightSubmit': stats['light_submissions'],
                'maxSubmit': stats['max_submit']
            })

    # 输出JSON格式
    print(json.dumps(result))
    # print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    parse_ctfd_data()

'''
'''