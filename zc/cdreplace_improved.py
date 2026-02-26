import os
import random
import math
from collections import defaultdict, deque


def read_trajectory_file(file_path):
    """读取轨迹文件，返回轨迹字典"""
    trajectories = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                trajectory_id = parts[0]
                grid_coordinates = parts[1].strip()
                trajectories[trajectory_id] = grid_coordinates
    return trajectories


def extract_grid_coordinates(coordinates):
    """提取网格坐标列表"""
    return [tuple(map(int, coord.strip('()').split(','))) for coord in coordinates.split(')(')]


def read_grid_map(file_path):
    """读取网格映射文件"""
    grid_map = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                grid_coord = tuple(map(int, parts[0].strip('() ').split(',')))
                grid_50_coords = parts[1].strip().split(')(')
                grid_map[grid_coord] = [tuple(map(int, coord.strip('()').split(','))) for coord in grid_50_coords]
    return grid_map


def read_probability_counts(file_path):
    """读取概率计数文件"""
    counts = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                coord = tuple(map(int, parts[0].strip('()').split(',')))
                count = int(parts[1].strip())
                counts[coord] = count
    return counts


def manhattan_distance(coord1, coord2):
    """计算曼哈顿距离"""
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def euclidean_distance(coord1, coord2):
    """计算欧几里得距离"""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])** 2)


def calculate_direction(prev_coord, curr_coord):
    """计算移动方向"""
    dx = curr_coord[0] - prev_coord[0]
    dy = curr_coord[1] - prev_coord[1]
    return (dx, dy)


def direction_similarity(dir1, dir2):
    """计算方向相似度（余弦相似度）"""
    dot_product = dir1[0] * dir2[0] + dir1[1] * dir2[1]
    mag1 = math.sqrt(dir1[0]**2 + dir1[1]** 2) or 1e-9
    mag2 = math.sqrt(dir2[0]**2 + dir2[1]** 2) or 1e-9
    return dot_product / (mag1 * mag2)


def softmax(weights, temperature=1.0):
    """应用softmax函数对权重进行归一化，防止数值溢出"""
    if not weights:
        return []
    
    try:
        # 温度参数调整，temperature越小，概率分布越集中
        temp_weights = [w / temperature for w in weights]
        
        # 减去最大值防止数值溢出
        if temp_weights:
            max_weight = max(temp_weights)
            exp_values = [math.exp(w - max_weight) for w in temp_weights]
            total = sum(exp_values)
            
            # 防止除零
            if total > 0:
                return [e / total for e in exp_values]
            else:
                # 如果总和为0，返回均匀分布
                return [1.0 / len(weights) for _ in weights]
        else:
            return []
    except Exception as e:
        # 异常处理，返回均匀分布作为fallback
        print(f"softmax计算异常: {e}")
        return [1.0 / len(weights) for _ in weights]


def calculate_turn_angle(dir1, dir2):
    """计算方向变化角度（弧度制）"""
    # 将方向向量转换为角度（atan2返回弧度）
    angle1 = math.atan2(dir1[1], dir1[0])
    angle2 = math.atan2(dir2[1], dir2[0])
    
    # 计算角度差
    angle_diff = angle2 - angle1
    
    # 标准化角度差到 [-π, π]
    while angle_diff > math.pi:
        angle_diff -= 2 * math.pi
    while angle_diff < -math.pi:
        angle_diff += 2 * math.pi
    
    return abs(angle_diff)


def improve_trajectory_mapping(grid_10_trajectories, grid_map, probability_counts, 
                               history_length=3, max_turn_angle=math.pi/2, 
                               temp=0.8, min_speed_change=0.5, max_speed_change=2.0):
    """
    改进的轨迹映射算法
    
    参数：
    - grid_10_trajectories: 轨迹字典
    - grid_map: 网格映射
    - probability_counts: 概率计数
    - history_length: 历史上下文长度
    - max_turn_angle: 最大允许转弯角度（弧度制）
    - temp: softmax温度参数
    - min_speed_change: 最小允许速度变化比例
    - max_speed_change: 最大允许速度变化比例
    
    返回：
    - 映射后的轨迹字典
    """
    mapped_trajectories = {}
    
    for trajectory_id, coords in grid_10_trajectories.items():
        new_coords = []
        coord_history = deque(maxlen=history_length)  # 保存历史坐标
        dir_history = []  # 保存历史方向
        
        grid_coords = extract_grid_coordinates(coords)
        
        for i, coord in enumerate(grid_coords):
            # 获取有效的grid_50坐标
            valid_grid_50 = grid_map.get(coord, [])
            if not valid_grid_50:
                continue
            
            # 计算基础权重
            base_weights = [probability_counts.get(g, 1) for g in valid_grid_50]
            
            if not new_coords:
                # 第一个点：使用top-k + softmax概率选择
                # 使用softmax进行权重归一化
                normalized_weights = softmax(base_weights, temp)
                
                # 基于归一化权重随机选择
                selected_coord = random.choices(valid_grid_50, weights=normalized_weights, k=1)[0]
                new_coords.append(selected_coord)
                coord_history.append(selected_coord)
            else:
                # 后续点：考虑历史上下文和连续性约束
                adjusted_weights = []
                
                for j, candidate in enumerate(valid_grid_50):
                    weight = base_weights[j]
                    
                    # 1. 距离约束（欧几里得距离比曼哈顿距离更平滑）
                    dist_weight = 1.0
                    last_coord = new_coords[-1]
                    eu_dist = euclidean_distance(last_coord, candidate)
                    
                    # 距离越小权重越高，但不强制距离为1
                    dist_weight = max(0.1, 1.0 / (eu_dist + 0.1))
                    
                    # 2. 方向约束（如果有足够的历史方向数据）
                    dir_weight = 1.0
                    if len(dir_history) > 0:
                        # 计算候选方向
                        candidate_dir = calculate_direction(last_coord, candidate)
                        
                        # 与最近历史方向的相似度
                        recent_dir = dir_history[-1]
                        dir_sim = direction_similarity(recent_dir, candidate_dir)
                        dir_weight = (dir_sim + 1) / 2  # 归一化到 [0, 1]
                        
                        # 检查转弯角度
                        if len(dir_history) > 0:
                            turn_angle = calculate_turn_angle(recent_dir, candidate_dir)
                            if turn_angle > max_turn_angle:
                                dir_weight *= 0.1  # 对大角度转弯进行惩罚
                    
                    # 3. 速度一致性约束
                    speed_weight = 1.0
                    if len(new_coords) >= 2:
                        # 计算历史速度
                        prev_dist = euclidean_distance(new_coords[-2], new_coords[-1])
                        curr_dist = euclidean_distance(last_coord, candidate)
                        
                        # 避免除以零
                        if prev_dist > 0:
                            speed_ratio = curr_dist / prev_dist
                            # 如果速度变化太大，给予惩罚
                            if speed_ratio < min_speed_change or speed_ratio > max_speed_change:
                                speed_weight = 0.3
                    
                    # 组合权重
                    total_weight = weight * dist_weight * dir_weight * speed_weight
                    adjusted_weights.append(total_weight)
                
                # 应用softmax
                normalized_weights = softmax(adjusted_weights, temp)
                
                # 基于调整后的权重选择
                selected_coord = random.choices(valid_grid_50, weights=normalized_weights, k=1)[0]
                new_coords.append(selected_coord)
                coord_history.append(selected_coord)
                
                # 更新方向历史
                if len(coord_history) >= 2:
                    new_dir = calculate_direction(coord_history[-2], coord_history[-1])
                    dir_history.append(new_dir)
                    # 保持方向历史长度不超过历史坐标长度-1
                    if len(dir_history) > history_length - 1:
                        dir_history.pop(0)
        
        # 保存映射后的轨迹
        new_coords_str = ''.join(f"({c[0]},{c[1]})" for c in new_coords)
        mapped_trajectories[trajectory_id] = new_coords_str
    
    return mapped_trajectories


# 主处理循环
if __name__ == "__main__":
    for i in range(30, 38):
        print(f"处理文件集: {i}")
        for grid_size in range(10, 41, 10):  # 从10到40的网格
            grid10_file_path = f'grid_output_taxi/{i}/grid{grid_size}/selected_trajectories.txt'
            grid_map_file_path = f'grid_output_taxi/{i}/grid{grid_size}/12gridmap.txt'
            counts_file_path = f'grid_output_taxi/{i}/grid.txt'
            output_file_path = f'grid_output_taxi/{i}/grid{grid_size}/14gridmap_output_improved.txt'

            if os.path.exists(grid10_file_path) and os.path.exists(grid_map_file_path):
                print(f"  处理网格大小: {grid_size}")
                # 读取必要的数据文件
                grid_10_trajectories = read_trajectory_file(grid10_file_path)
                grid_map = read_grid_map(grid_map_file_path)
                probability_counts = read_probability_counts(counts_file_path)
                
                # 应用改进的映射算法
                mapped_trajectories = improve_trajectory_mapping(
                    grid_10_trajectories, 
                    grid_map, 
                    probability_counts,
                    history_length=3,       # 使用最近3个点的历史
                    max_turn_angle=math.pi/2,  # 最大允许90度转弯
                    temp=0.8,              # softmax温度参数
                    min_speed_change=0.3,   # 允许速度降低到原来的30%
                    max_speed_change=1.8    # 允许速度增加到原来的180%
                )
                
                # 将结果写入文件
                with open(output_file_path, 'w') as output_file:
                    for trajectory_id, coords_str in mapped_trajectories.items():
                        output_file.write(f"{trajectory_id}: {coords_str}\n")
                
                print(f"  结果已保存到: {output_file_path}")
            else:
                print(f"  文件未找到: {grid10_file_path} 或 {grid_map_file_path}")
