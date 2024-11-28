import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def calculate_department_score(threat_scores):
    return np.mean(threat_scores)

def calculate_aggregated_score(department_scores, importance_weights):
    weighted_sum = sum(score * weight for score, weight in zip(department_scores, importance_weights))
    total_weight = sum(importance_weights)
    return weighted_sum / total_weight if total_weight else 0

class TestAggregatedUserThreatScore(unittest.TestCase):

    def test_calculate_department_score(self):
        scores = [10, 20, 30, 40, 50]
        self.assertEqual(calculate_department_score(scores), 30, "Should calculate average score correctly")

    def test_calculate_aggregated_score_equal_importance(self):
        department_scores = [20, 30, 40, 50, 60]
        importance_weights = [1, 1, 1, 1, 1]
        self.assertEqual(calculate_aggregated_score(department_scores, importance_weights), 40,
                         "Should average scores equally")

    def test_calculate_aggregated_score_varying_importance(self):
        department_scores = [10, 30, 50, 70, 90]
        importance_weights = [1, 2, 3, 4, 5]
        weighted_avg = calculate_aggregated_score(department_scores, importance_weights)
        self.assertAlmostEqual(weighted_avg, 63.3, places=1, msg="Should calculate weighted average correctly")

    def test_generate_random_data(self):
        # Adjusted test for generate_random_data while keeping its behavior
        data = generate_random_data(30, 10, 50)
        self.assertTrue((data >= 20).all() and (data <= 40).all(),
                        "Generated data should be within the specified mean and variance")

    def test_functional_case_1(self):
        scores_eng = generate_random_data(30, 5, 100)
        scores_mkt = generate_random_data(30, 5, 100)
        scores_fin = generate_random_data(30, 5, 100)
        scores_hr = generate_random_data(30, 5, 100)
        scores_sci = generate_random_data(30, 5, 100)

        dept_scores = [calculate_department_score(scores) for scores in
                       [scores_eng, scores_mkt, scores_fin, scores_hr, scores_sci]]
        importance = [1, 1, 1, 1, 1]
        aggregated_score = calculate_aggregated_score(dept_scores, importance)

        self.assertTrue(all(0 <= score <= 90 for score in dept_scores), "Each department score should be valid")
        self.assertTrue(0 <= aggregated_score <= 90, "Aggregated score should be within 0-90")

    def test_functional_case_2(self):
        scores_eng = generate_random_data(60, 10, 150)
        scores_mkt = generate_random_data(20, 5, 50)
        scores_fin = generate_random_data(40, 8, 75)
        scores_hr = generate_random_data(25, 10, 20)
        scores_sci = generate_random_data(35, 15, 200)

        dept_scores = [calculate_department_score(scores) for scores in
                       [scores_eng, scores_mkt, scores_fin, scores_hr, scores_sci]]
        importance = [5, 1, 3, 2, 4]
        aggregated_score = calculate_aggregated_score(dept_scores, importance)

        self.assertTrue(all(0 <= score <= 90 for score in dept_scores), "Each department score should be valid")
        self.assertTrue(0 <= aggregated_score <= 90, "Aggregated score should be within 0-90")

    def test_functional_case_3(self):
        scores_eng = generate_random_data(5, 2, 80)
        scores_mkt = generate_random_data(10, 2, 60)
        scores_fin = generate_random_data(8, 3, 100)
        scores_hr = generate_random_data(5, 2, 50)
        scores_sci = generate_random_data(7, 2, 120)

        dept_scores = [calculate_department_score(scores) for scores in
                       [scores_eng, scores_mkt, scores_fin, scores_hr, scores_sci]]
        importance = [3, 2, 1, 4, 5]
        aggregated_score = calculate_aggregated_score(dept_scores, importance)

        self.assertTrue(all(0 <= score <= 90 for score in dept_scores), "Each department score should be valid")
        self.assertTrue(0 <= aggregated_score <= 90, "Aggregated score should be within 0-90")

if __name__ == '__main__':
    unittest.main()
