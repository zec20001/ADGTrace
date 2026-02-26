import re
from collections import defaultdict
import os


class MarkovTrajectoryProcessor:
    def __init__(self, folder_range, trajectory_file_template, transition_counts_file_template, transition_probabilities_file_template):
        self.folder_range = folder_range
        self.trajectory_file_template = trajectory_file_template
        self.transition_counts_file_template = transition_counts_file_template
        self.transition_probabilities_file_template = transition_probabilities_file_template

    def process_folder(self, folder_idx):
        trajectory_file_path = self.trajectory_file_template.format(folder_idx=folder_idx)
        transition_counts_file_path = self.transition_counts_file_template.format(folder_idx=folder_idx)
        transition_probabilities_file_path = self.transition_probabilities_file_template.format(folder_idx=folder_idx)

        if not os.path.exists(trajectory_file_path):
            print(f"文件 {trajectory_file_path} 不存在，跳过文件夹 {folder_idx:03d}。")
            return
        with open(trajectory_file_path, 'r') as file:
            trajectories = file.readlines()

        transition_counts = defaultdict(lambda: defaultdict(int))

        for trajectory in trajectories:
            states = re.findall(r'\((\d+),(\d+)\)', trajectory)

            for i in range(len(states) - 1):
                state_A = (int(states[i][0]), int(states[i][1]))
                state_B = (int(states[i + 1][0]), int(states[i + 1][1]))
                transition_counts[state_A][state_B] += 1

        transition_probabilities = defaultdict(lambda: defaultdict(float))

        for state_A, transitions in transition_counts.items():
            total_transitions_from_A = sum(transitions.values())

            for state_B, count in transitions.items():
                transition_probabilities[state_A][state_B] = count / total_transitions_from_A

        with open(transition_counts_file_path, 'w') as counts_file:
            for state_A, transitions in transition_counts.items():
                for state_B, count in transitions.items():
                    counts_file.write(f"(({state_A[0]},{state_A[1]})({state_B[0]},{state_B[1]})) {count}\n")

        with open(transition_probabilities_file_path, 'w') as probabilities_file:
            for state_A, transitions in transition_probabilities.items():
                for state_B, probability in transitions.items():
                    probabilities_file.write(f"(({state_A[0]},{state_A[1]})({state_B[0]},{state_B[1]})) {probability:.4f}\n")

        print(f"文件夹 {folder_idx:03d} 的马尔科夫转移数已保存到 {transition_counts_file_path}")
        print(f"文件夹 {folder_idx:03d} 的马尔科夫转移概率已保存到 {transition_probabilities_file_path}")

    def process_all_folders(self):
        for folder_idx in self.folder_range:
            print(f"Processing folder {folder_idx:03d}...")
            self.process_folder(folder_idx)

