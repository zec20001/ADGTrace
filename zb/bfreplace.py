import random
import os

# from zc.cbgridmap import grid_size


class GridTrajectoryReplacer:
    def __init__(self, grid_file_template, trajectory_file_template, output_file_template, folder_range):
        """
        初始化 GridTrajectoryReplacer 类
        :param grid_file_template: 网格文件路径模板
        :param trajectory_file_template: 轨迹文件路径模板
        :param output_file_template: 输出文件路径模板
        :param folder_range: 要处理的文件夹范围
        """
        self.grid_file_template = grid_file_template
        self.trajectory_file_template = trajectory_file_template
        self.output_file_template = output_file_template
        self.folder_range = folder_range

    def load_grid_to_coordinates(self, grid_file):
        """
        从网格文件中加载网格和经纬度数据
        :param grid_file: 网格文件路径
        :return: 一个字典，键为网格坐标，值为对应的经纬度列表
        """
        grid_to_coords = {}
        with open(grid_file, 'r') as f:
            for line in f:
                try:
                    grid_key, coords = line.split(":")
                    coords_list = coords.strip().split(")(")
                    
                    processed_coords = []
                    for coord in coords_list:
                        # 清理坐标字符串
                        cleaned_coord = coord.strip("()").strip()
                        if cleaned_coord:
                            try:
                                # 分割并过滤空字符串
                                lat_lon = [c.strip() for c in cleaned_coord.split(",") if c.strip()]
                                if len(lat_lon) == 2:
                                    processed_coords.append((float(lat_lon[0]), float(lat_lon[1])))
                                else:
                                    print(f"Warning: Invalid coordinate format {coord} for grid {grid_key.strip()}")
                            except ValueError as e:
                                print(f"Warning: Failed to convert coordinates {coord} for grid {grid_key.strip()}: {e}")
                    
                    grid_key_clean = grid_key.strip()
                    if processed_coords:  # 只添加有效的坐标列表
                        grid_to_coords[grid_key_clean] = processed_coords
                except ValueError:
                    print(f"Warning: Failed to parse line: {line.strip()}")
        return grid_to_coords

    def load_trajectories(self, trajectory_file):
        """
        从轨迹文件中加载轨迹数据
        :param trajectory_file: 轨迹文件路径
        :return: 一个字典，键为轨迹ID，值为网格坐标列表
        """
        trajectories = {}
        with open(trajectory_file, 'r') as f:
            for line in f:
                tra_id, grid_locs = line.split(":")
                grid_locs = grid_locs.strip().split(")(")
                
                # 添加错误处理，避免空字符串转换为整数
                processed_locs = []
                for loc in grid_locs:
                    # 清理坐标字符串
                    cleaned_loc = loc.strip("()").strip()
                    if cleaned_loc:
                        try:
                            # 分割并过滤空字符串
                            coords = [c.strip() for c in cleaned_loc.split(",") if c.strip()]
                            if len(coords) == 2:
                                processed_locs.append((int(coords[0]), int(coords[1])))
                            else:
                                print(f"Warning: Invalid coordinate format {loc} in trajectory {tra_id.strip()}")
                        except ValueError as e:
                            print(f"Warning: Failed to convert coordinates {loc} in trajectory {tra_id.strip()}: {e}")
                
                trajectories[tra_id.strip()] = processed_locs
        return trajectories

    def replace_grid_with_coordinates(self, trajectories, grid_to_coords):
        """
        将轨迹中的网格坐标替换为对应的经纬度
        :param trajectories: 包含网格坐标的轨迹字典
        :param grid_to_coords: 网格与经纬度对应关系的字典
        :return: 替换后的轨迹字典
        """
        replaced_trajectories = {}
        for tra_id, grid_locs in trajectories.items():
            replaced_trajectories[tra_id] = []
            for grid_loc in grid_locs:
                grid_key = f"({grid_loc[0]},{grid_loc[1]})"
                if grid_key in grid_to_coords:
                    # 随机从对应网格的经纬度列表中选取一个经纬度
                    replaced_trajectories[tra_id].append(random.choice(grid_to_coords[grid_key]))
                else:
                    print(f"Warning: No coordinates found for grid {grid_key}")
        return replaced_trajectories

    def save_replaced_trajectories(self, output_file, replaced_trajectories):
        """
        将替换后的轨迹保存到文件
        :param output_file: 输出文件路径
        :param replaced_trajectories: 替换后的轨迹数据字典
        """
        with open(output_file, 'w') as f:
            for tra_id, coords in replaced_trajectories.items():
                coord_str = "".join([f"({lat},{lon})" for lat, lon in coords])
                f.write(f"{tra_id}:{coord_str}\n")

    def process(self):
        """
        处理轨迹文件中的网格坐标替换为经纬度
        """
        # 直接使用传入的文件路径（不再是模板）
        grid_file = self.grid_file_template  # 现在是直接的文件路径
        trajectory_file = self.trajectory_file_template  # 现在是直接的文件路径
        output_file = self.output_file_template  # 现在是直接的文件路径
        
        # 检查文件是否存在
        if not os.path.exists(grid_file):
            print(f"错误: 网格文件 {grid_file} 不存在。")
            return
        if not os.path.exists(trajectory_file):
            print(f"错误: 轨迹文件 {trajectory_file} 不存在。")
            return

        print(f"正在处理网格文件: {grid_file}")
        print(f"正在处理轨迹文件: {trajectory_file}")
        
        # Step 1: 读取网格与经纬度数据
        try:
            grid_to_coords = self.load_grid_to_coordinates(grid_file)
            print(f"成功加载网格数据，共 {len(grid_to_coords)} 个网格")
        except Exception as e:
            print(f"加载网格数据失败: {e}")
            return

        # Step 2: 读取轨迹数据
        try:
            trajectories = self.load_trajectories(trajectory_file)
            print(f"成功加载轨迹数据，共 {len(trajectories)} 条轨迹")
        except Exception as e:
            print(f"加载轨迹数据失败: {e}")
            return

        # Step 3: 替换网格坐标为经纬度
        try:
            replaced_trajectories = self.replace_grid_with_coordinates(trajectories, grid_to_coords)
            print(f"成功替换网格坐标为经纬度")
        except Exception as e:
            print(f"替换网格坐标失败: {e}")
            return

        # Step 4: 保存替换后的轨迹
        try:
            self.save_replaced_trajectories(output_file, replaced_trajectories)
            print(f"成功保存替换后的轨迹到: {output_file}")
        except Exception as e:
            print(f"保存替换后的轨迹失败: {e}")
            return

        print("轨迹文件替换已完成。")


#使用类
if __name__ == "__main__":
    # 处理的文件夹范围和网格大小
    folder_range = range(30,38)  # 处理的文件夹范围
    grid_sizes = [50]  # 处理的网格大小

    # 循环处理每个文件夹和每个网格大小
    for folder_idx in folder_range:
        for grid_size in grid_sizes:
            # 为每个文件夹和网格大小创建独立的处理器
            print(f"Creating processor for folder {folder_idx}, grid size {grid_size}")
            
            # 设置文件路径模板（注意：这里不需要模板参数，直接使用具体路径）
            grid_file = f"grid_output_taxi/{folder_idx}/grid{grid_size}/11gridloca.txt"
            trajectory_file = f"grid_output_taxi/{folder_idx}/grid{grid_size}/selected_trajectories.txt"
            output_file = f"grid_output_taxi/{folder_idx}/grid{grid_size}/result/replaced_trajectories.txt"
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Created output directory: {output_dir}")
            
            # 创建处理器实例，只传入单个文件夹的范围
            replacer = GridTrajectoryReplacer(
                grid_file,  # 直接使用文件路径，不是模板
                trajectory_file,  # 直接使用文件路径，不是模板
                output_file,  # 直接使用文件路径，不是模板
                [folder_idx]  # 只处理当前文件夹
            )
            
            # 处理单个文件夹
            replacer.process()
