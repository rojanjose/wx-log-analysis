import csv
import random
import pandas as pd

from datetime import datetime, timedelta

def generate_data(start_date, num_days):
    # Baseline values for daily operations
    baseline_compression = 10
    baseline_encryption = 5
    data = []

    # Generate data for each day
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        if random.random() < 0.15:  # 15% chance of a spike
            # Simulate a spike, potentially malicious
            compression = baseline_compression * random.randint(5, 10)
            encryption = baseline_encryption * random.randint(5, 10)
        else:
            # Normal daily activity with small variations
            compression = baseline_compression + random.randint(-2, 2)
            encryption = baseline_encryption + random.randint(-1, 1)

        # Append the day's data to the list
        data.append({
            "Date": date.strftime('%Y-%m-%d'),
            "Session ID": f"session_id_{random.randint(1000, 2000)}", 
            "Files Compressed": compression,
            "Files Encrypted": encryption
        })

    return data

#Save the generated data into a CSV file.
def save_to_csv(data, filename, fieldnames):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Generate synthetic data for 30 days.
def generate_suspicious_disk_activity():
    
    file_name='suspicious_disk_activity.csv'
    fieldnames = ["Date", "Session ID", "Files Compressed", "Files Encrypted"]
    start_date = datetime.now()
    num_days = 30
    data = generate_data(start_date, num_days)

    save_to_csv(data, file_name, fieldnames)
    print(f"Disk activity data saved to {file_name}")

# Generate synthetic file read/write for a date range.
def generate_malicious_reads_and_writes():

    file_name = 'data/malicious_reads_writes.csv'
    random.seed(42)

    # Generate a DataFrame for disk reads and writes
    data = {
        "timestamp": pd.date_range(start="2024-05-09 00:00:00", periods=1440, freq="min"),  # Every minute for one day
        "file_accessed": ["file_" + str(random.randint(1, 20)) for _ in range(1440)],
        "disk_reads": [random.randint(10, 30) for _ in range(1440)],  # Normal range of reads
        "disk_writes": [random.randint(5, 10) for _ in range(1440)],  # Normal range of writes
        "user": ["user_" + str(random.randint(1, 10)) for _ in range(1440)]
    }

    # Introduce a malicious read pattern: high volume reads from a rarely accessed file at an odd time
    malicious_start_index = 1200  # Late at night
    malicious_end_index = malicious_start_index + 10
    malicious_file = "file_19"  # Typically not accessed frequently
    malicious_user = "user_9"  # Suspicious or less frequent user

    #Generate abnormally high read & write count
    for i in range(malicious_start_index, malicious_end_index):
        data["disk_reads"][i] = random.randint(500, 1000)  
        data["disk_writes"][i] = random.randint(500, 1000)
        data["file_accessed"][i] = malicious_file
        data["user"][i] = malicious_user

    df = pd.DataFrame(data)
    df.to_csv(file_name)
    print(f"Read/write activity data saved to {file_name}")


def main():

    generate_suspicious_disk_activity()
    generate_malicious_reads_and_writes()


if __name__ == "__main__":
    main()
