import csv
import random
from faker import Faker

# 初始化Faker库用于生成模拟数据
fake = Faker()

# CSV文件名
csv_file_name = 'random_test_data.csv'

# 定义要生成的数据数量
num_of_rows = 10

# 定义CSV列头
headers = ["Name", "Age", "City"]

# 打开CSV文件并写入列头
with open(csv_file_name, 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    # 生成并写入随机数据
    for _ in range(num_of_rows):
        name = fake.name()
        age = random.randint(18, 99)
        city = fake.city()
        writer.writerow([name, age, city])

print(f"随机CSV文件 '{csv_file_name}' 已成功生成，包含了{num_of_rows}行数据。")
