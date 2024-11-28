import csv
import numpy as np

def read_data_from_csv(filename):
    department_data = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            department = row["Department"]
            score = int(row["Score"])
            if department not in department_data:
                department_data[department] = []
            department_data[department].append(score)
    return department_data

def calculate_department_score(threat_scores):
    return np.mean(threat_scores)

def calculate_aggregated_score(department_scores, importance_weights):
    weighted_sum = sum(score * weight for score, weight in zip(department_scores, importance_weights))
    total_weight = sum(importance_weights)
    return weighted_sum / total_weight if total_weight else 0

if __name__ == '__main__':
    # Parameters
    input_file = "generated_data.csv"
    importance_weights = [1, 2, 3, 4, 5]  # Example weights for each department

    # Read data
    department_data = read_data_from_csv(input_file)

    # Calculate department scores
    department_scores = [calculate_department_score(scores) for scores in department_data.values()]

    # Calculate aggregated score
    aggregated_score = calculate_aggregated_score(department_scores, importance_weights)

    # Output results
    print("Department Scores:", department_scores)
    print("Aggregated Score:", aggregated_score)
