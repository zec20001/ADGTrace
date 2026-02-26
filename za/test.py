import os
from adindexTra import process_trajectory
from aemarkov import MarkovChainProcessor
from afdis import TrajectoryProcessor
from agsim import TrajectorySimulator

# 定义文件夹范围和网格大小列表
folder_range = range(2,3)  # 处理文件夹 1 到 2
grid_sizes = [10, 20, 30, 40, 50]  # 网格大小列表

input_dir = 'output_taxi/'  # 输入文件夹路径
for file_index in folder_range:
    input_file_name = f'{file_index}_1.txt'

    # 检查输入文件是否存在
    input_file = os.path.join(input_dir, input_file_name)
    if not os.path.exists(input_file):
        print(f"输入文件 {input_file} 不存在，跳过该文件。")
        continue

    # 为每个文件创建单独的文件夹
    for n in grid_sizes:
        # 动态生成输出文件夹路径，带上当前网格数
        output_dir = f'grid_output_taxi/{file_index}/grid{n}/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"输出文件夹 {output_dir} 不存在，已自动创建。")

            # 输出文件名
        output_file_name = f'{file_index}_1_grid.txt'
        output_file = os.path.join(output_dir, output_file_name)

        # 保存每个网格的坐标到 11gridloca.txt 文件
        gridloca_file = os.path.join(output_dir, '11gridloca.txt')

        # 处理轨迹数据
        try:
            process_trajectory(input_file, output_file)# n, gridloca_file
            print(f"网格化处理完成，结果已保存至 {output_file}，网格坐标已保存至 {gridloca_file}")
        except Exception as e:
            print(f"处理文件 {input_file} 时出错: {e}")