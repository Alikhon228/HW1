import numpy as np
import csv

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def write_data_to_csv(filename, num_departments, mean, variance, num_samples):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Department", "Score"])
        for i in range(num_departments):
            department_scores = generate_random_data(mean, variance, num_samples)
            for score in department_scores:
                writer.writerow([f"Department_{i+1}", score])

if __name__ == '__main__':
    # Parameters for data generation
    output_file = "generated_data.csv"
    num_departments = 5
    mean = 30
    variance = 10
    num_samples = 50

    # Generate and save data
    write_data_to_csv(output_file, num_departments, mean, variance, num_samples)
    print(f"Data generated and saved to {output_file}")
