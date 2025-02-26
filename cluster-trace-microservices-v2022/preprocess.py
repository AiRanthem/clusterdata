import argparse
import pandas as pd
import os
from tqdm import tqdm
import glob

def process_and_save_data(input_csv_path, output_dir):
    print(f"Processing and saving data from {input_csv_path} to {output_dir}")
    df = pd.read_csv(input_csv_path, usecols=['timestamp', 'msinstanceid', 'cpu_utilization'])
    grouped = df.groupby('msinstanceid')

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for msinstanceid, data in tqdm(grouped):
        data = data[['timestamp', 'cpu_utilization']]
        data = data.sort_values(by=['timestamp'])
        data['cpu_utilization'] = data['cpu_utilization'].apply(lambda x: min(x * 15, 0.8))
        output_file_path = os.path.join(output_dir, f'{msinstanceid}.csv')
        # 如果文件存在，追加到文件后面而不是覆盖
        if os.path.exists(output_file_path):
            data.to_csv(output_file_path, mode='a', header=False, index=False)
        else:
            data.to_csv(output_file_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, help='输入的CSV文件目录')
    parser.add_argument('--output_dir', type=str, required=True, help='输出目录路径')
    args = parser.parse_args()

    # 获取目录下所有csv文件
    csv_files = glob.glob(os.path.join(args.input_dir, '*.csv'))
    for input_csv_path in csv_files:
        process_and_save_data(input_csv_path, args.output_dir)