import numpy as np
import pandas as pd
from collections import Counter

# Simulated synthetic data for user sessions
np.random.seed(42)
data = {
    'user_id': np.repeat(np.arange(1, 6), 5),
    'session_id': np.tile(np.arange(1, 6), 5),
    'content_type': np.random.choice(['drama', 'educational', 'entertainment', 'news', 'documentary'], 25),
    'watch_time': np.random.randint(1, 100, 25),
    'interaction_rate': np.random.rand(25),
    'search_repetition': np.random.randint(0, 5, 25),
    'return_rate': np.random.randint(0, 3, 25),
    'switching_time': np.random.randint(1, 10, 25),
    'scrolling_time': np.random.randint(1, 10, 25),
    'time_of_day': np.random.choice(['morning', 'afternoon', 'evening', 'night'], 25)
}

# Additional data to ensure multiple content types per session for a single user
extra_data = {
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5],
    'session_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5],
    'content_type': ['drama', 'news', 'educational', 'entertainment', 'documentary', 'news', 'news', 'drama', 'educational', 'drama', 'entertainment', 'documentary', 'news'],
    'watch_time': [45, 30, 60, 20, 50, 40, 70, 40, 55, 25, 35, 60, 45],
    'interaction_rate': [0.8, 0.5, 0.9, 0.3, 0.7, 0.6, 0.6, 0.75, 0.85, 0.4, 0.5, 0.9, 0.7],
    'search_repetition': [4, 2, 5, 1, 3, 2, 2, 4, 3, 1, 2, 5, 4],
    'return_rate': [2, 1, 2, 0, 1, 1, 1, 2, 2, 0, 1, 2, 1],
    'switching_time': [3, 5, 2, 8, 6, 5, 7, 4, 6, 3, 4, 2, 5],
    'scrolling_time': [4, 6, 3, 7, 5, 6, 5, 3, 4, 2, 3, 6, 4],
    'time_of_day': ['evening', 'night', 'morning', 'afternoon', 'night', 'morning', 'morning', 'night', 'afternoon', 'evening', 'night', 'morning', 'evening']
}

# Combine datasets
data.update({k: np.append(v, extra_data[k]) for k, v in data.items()})

# DataFrame creation
df = pd.DataFrame(data)

# Engagement metric weights
weights = {
    'watch_time': 0.1,
    'interaction_rate': 0.05,
    'search_repetition': 0.2,
    'return_rate': 0.2,
    'switching_time': 0.25,
    'scrolling_time': 0.2,
    'time_of_day_weight': {
        'educational': {'night': 0.8, 'morning': 1.2, 'afternoon': 1.0, 'evening': 1.0},
        'entertainment': {'night': 1.3, 'morning': 0.7, 'afternoon': 1.0, 'evening': 1.1},
        'drama': {'night': 1.7, 'morning': 0.6, 'afternoon': 1.0, 'evening': 1.1},
        'default': {'night': 1.0, 'morning': 1.0, 'afternoon': 1.0, 'evening': 1.0}
    }
}

# Calculate engagement score
def calculate_engagement_score(row):
    content_type = row['content_type']
    time_weight = weights['time_of_day_weight'].get(content_type, weights['time_of_day_weight']['default'])[row['time_of_day']]
    base_score = (
        (row['watch_time'] * weights['watch_time']) +
        (row['interaction_rate'] * weights['interaction_rate']) +
        (row['search_repetition'] * weights['search_repetition']) +
        (row['return_rate'] * weights['return_rate']) +
        (row['switching_time'] * weights['switching_time']) +
        (row['scrolling_time'] * weights['scrolling_time'])
    )
    return base_score * time_weight

df['engagement_score'] = df.apply(calculate_engagement_score, axis=1)

# Calculate drug of choice labels
def get_labels(user_sessions):
    engagement_scores = {}
    content_frequency = Counter()

    for _, session in user_sessions.groupby('session_id'):
        content_counts = Counter(session['content_type'])
        content_frequency.update(content_counts)
        for _, row in session.iterrows():
            content = row['content_type']
            if content not in engagement_scores:
                engagement_scores[content] = []
            engagement_scores[content].append(row['engagement_score'])

    avg_scores = {content: np.mean(scores) for content, scores in engagement_scores.items()}
    std_dev = np.std(list(avg_scores.values()))

    if std_dev < 0.5:
        balance = True
    else:
        balance = False

    freq_weighted_scores = {content: avg_scores[content] * (1 + (content_frequency[content] / sum(content_frequency.values()))) for content in avg_scores}
    max_score = max(freq_weighted_scores.values())
    drug_of_choice = [content for content, score in freq_weighted_scores.items() if abs(score - max_score) <= 0.3 or std_dev < 0.3]

    return drug_of_choice, balance

# Output for each user
user_labels = df.groupby('user_id').apply(get_labels)

for user_id, (drug_of_choice, balance) in user_labels.items():
    balance_status = 'Balanced' if balance else 'Not Balanced'
    print(f"User {user_id} -> Drug of Choice: {drug_of_choice}, Balance Status: {balance_status}")
