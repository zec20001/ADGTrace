import random


def select_and_renumber_trajectories(input_file, output_file, num_trajectories=300):
    """
    从输入文件中随机选取指定数量的轨迹，重新编号，并将它们写入输出文件。

    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :param num_trajectories: 需要选取的轨迹数量，默认为300
    """
    # 读取所有轨迹
    with open(input_file, 'r') as f:
        trajectories = f.readlines()

    # 确保选取的数量不超过总轨迹数
    num_trajectories = min(num_trajectories, len(trajectories))

    # 随机选取指定数量的轨迹
    selected_trajectories = random.sample(trajectories, num_trajectories)

    # 将选取的轨迹重新编号并写入输出文件
    with open(output_file, 'w') as f:
        for i, traj in enumerate(selected_trajectories, 1):
            # 去掉原始编号，重新编号
            traj_data = traj.split(':', 1)[1].strip()
            f.write(f"T{i}:{traj_data}\n")


if __name__ == "__main__":
    input_file = "output_taxi/2_1.txt"  # 输入文件路径
    output_file = "output_taxi/3_1.txt"  # 输出文件路径

    select_and_renumber_trajectories(input_file, output_file)
    print(f"已从 {input_file} 中随机选取 300 条轨迹，并重新编号后保存到 {output_file}")