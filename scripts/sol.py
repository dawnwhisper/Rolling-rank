import csv
import json
from collections import defaultdict
from datetime import datetime

def parse_time(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def parse_ctfd_data():
    light_time = datetime.strptime("07:11:30", "%H:%M:%S").time()
    
    # 读取CSV文件
    users = read_csv('data/NUAACTF-users.csv')
    submissions = read_csv('data/NUAACTF-submissions.csv')
    challenges = read_csv('data/NUAACTF-challenges.csv')
    teams = read_csv('data/NUAACTF-teams.csv')

    # 计算总题目数
    total_challenges = len(challenges)

    # 创建题目分值映射
    challenge_values = {c['id']: int(c['value']) for c in challenges}

    # 创建用户到团队的映射
    user_team_map = {u['id']: u['team_id'] for u in users}

    # 初始化所有队伍的统计数据
    team_stats = {}
    for team in teams:
        # 跳过隐藏的队伍
        if team['hidden'] == 'True':
            continue
        team_stats[team['id']] = {
            'name': team['name'],
            'solved': set(),
            'score': 0,
            'light_submissions': [],
            'max_submit': 0,
            'nonCompeting': False
        }
        if team_stats[team['id']]['name'] in ['mini5U5', 'miniSUS', 'Dozer', 'N0T', '国际中央大学壹队', '国际中央大学二队']:
            team_stats[team['id']]['nonCompeting'] = True
    
    # 处理提交记录
    for sub in submissions:
        user_id = sub['user_id']
        team_id = user_team_map[user_id]
        if team_id not in team_stats:  # 跳过隐藏队伍的提交
            continue
            
        sub_time = parse_time(sub['date']).time()
        
        # 黑灯前的提交
        if sub_time < light_time:
            if sub['type'] == 'correct':
                challenge_id = sub['challenge_id']
                team_stats[team_id]['solved'].add(challenge_id)
                team_stats[team_id]['score'] += challenge_values[challenge_id]
        # 黑灯后的提交
        else:
            team_stats[team_id]['max_submit'] += 1
            if sub['type'] == 'correct':
                challenge_id = sub['challenge_id']
                team_stats[team_id]['light_submissions'].append(
                    (team_stats[team_id]['max_submit'], 
                     challenge_values[challenge_id])
                )

    # 格式化输出结果
    result = []
    for team_id, stats in team_stats.items():
        result.append({
            'name': stats['name'],
            'solved': len(stats['solved']),
            'total': total_challenges,
            'ctfScore': stats['score'],
            'kohScore': 0,
            'totalScore': stats['score'],
            'lightSubmit': stats['light_submissions'],
            'maxSubmit': stats['max_submit'],
            'nonCompeting': stats['nonCompeting']
        })

    # 输出JSON格式
    # print(json.dumps(result))
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    parse_ctfd_data()