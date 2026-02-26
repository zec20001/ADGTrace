from geopy.distance import distance
import math

min_lat, max_lat = 35.464588, 35.902039
min_lon, max_lon = 139.537016, 140.075257

# n = 20


def calculate_grid_sizes(n):
    lat_distance_km = distance((min_lat, min_lon), (max_lat, min_lon)).km
    lat_grid_size_km = lat_distance_km / n

    lon_distance_km = distance((min_lat, min_lon), (min_lat, max_lon)).km
    m = int(lon_distance_km / lat_grid_size_km)

    return lat_grid_size_km, m


def lat_lon_to_grid(lat, lon, lat_grid_size_km, m):
    lat_distance = distance((min_lat, min_lon), (lat, min_lon)).km
    grid_i = math.floor(lat_distance / lat_grid_size_km)

    lon_distance = distance((min_lat, min_lon), (min_lat, lon)).km
    grid_j = math.floor(lon_distance / lat_grid_size_km)

    grid_j = min(grid_j, m - 1)

    return grid_i, grid_j


def process_trajectory(input_file, output_file,n,gridloca_file):
    lat_grid_size_km, m = calculate_grid_sizes(n)
    grid_dict = {}
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            trajectory_id, points = line.split(':')
            points = points.strip().split(')(')
            points[0] = points[0].replace('(', '')
            points[-1] = points[-1].replace(')', '')

            grid_points = []
            for point in points:
                lat, lon = map(float, point.split(','))
                grid_i, grid_j = lat_lon_to_grid(lat, lon, lat_grid_size_km, m)
                grid_points.append(f"({grid_i},{grid_j})")
                grid_key = f"({grid_i},{grid_j})"

                # 将原始坐标点添加到对应网格的列表中
                if grid_key not in grid_dict:
                    grid_dict[grid_key] = []
                grid_dict[grid_key].append(f"({lat},{lon})")

                grid_points.append(grid_key)
            outfile.write(f"{trajectory_id}:{''.join(grid_points)}\n")
            with open(gridloca_file, 'w') as gridfile:
                for grid_key in sorted(grid_dict.keys()):
                    points_str = ''.join(grid_dict[grid_key])
                    gridfile.write(f"{grid_key}: {points_str}\n")
