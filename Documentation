## User Drug of Choice Labels Code Documentation
## Overview
This code analyzes user engagement with different content types across sessions and determines their "drug of choice" (preferred content) and balance status (whether their preferences are evenly distributed). It uses engagement metrics like watch time, interaction rate, search repetition, and more to derive these insights.

## Data Preparation
•	Synthetic Data: Randomly generated user session data, including content_type, watch_time, interaction_rate, and more.
•	Extra Data: Additional entries to ensure diversity in content types per session.
•	DataFrame Creation: Combines synthetic and extra data into a single DataFrame df.
## Engagement Score Calculation
•	Weights: Different engagement metrics are weighted according to their importance.
•	Time of Day Weighting: Adjusts weights based on content type and time of day.
•	Engagement Score Formula:
•	base_score = (watch_time * weight) + (interaction_rate * weight) + ...
engagement_score = base_score * time_of_day_weight
## Drug of Choice and Balance Calculation
•	Content Frequency: Tracks how often each content type is watched.
•	Engagement Scores: Averages engagement scores for each content type.
•	Standard Deviation (std_dev): Measures the spread of average engagement scores.
•	Balance Status:
o	Balanced if std_dev < 0.5 (engagement scores are similar across content types)
o	Not Balanced otherwise
•	Frequency-Weighted Scores: Adjusts engagement scores based on how often content appears.
•	Drug of Choice:
o	Content types with highest frequency-weighted scores.
o	If multiple content types have similar scores (abs(score - max_score) <= 0.3), they’re all considered.
o	If std_dev < 0.3, all content types are considered preferred.

## Output
For each user:
User <id> -> Drug of Choice: [<content_types>], Balance Status: <Balanced/Not Balanced>
