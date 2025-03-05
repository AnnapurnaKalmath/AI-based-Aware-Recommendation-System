In the phase 2: the main purpose is to understand the behaviour of the person and help them to be present in whichever state they are. This phase can be divided into tasks:
1.	Identifying the current state of the user
2.	Mechanism applied to help the user to be in the state they are present currently

1.Identifying the current state of the user
States focused on are: Focused/Leisure
Can identify the current state by 3 kinds:
1.	Prompt provided by the user
2.	Tracking the behavior of the user. Here we can consider these metrics:
  1.	Focused -  Long watch time for the same productive content (watch time, productive content)
  2.	Leisure -  Short watch time/can be long also but entertainment tagged with higher number of switches/can be low also
3. Searches in the prompt/that is search area   (nlp)

## 1.User State Tracker 
### Overview: This script determines whether a user’s current state is focused or leisure based on their behavior, like search activity, content engagement, and watch time patterns. It prioritizes early exit for efficiency and asks for user input only when needed.
### Libraries Used:
•	time: Simulates time-based behavior (not heavily used here).
•	random: Generates synthetic data for testing.
•	spacy: Processes and analyzes natural language input from user searches.
### NLP Model:
•	en_core_web_sm: A small English model used for lemmatization and keyword matching. Ensure it’s installed using: python -m spacy download en_core_web_sm.
Synthetic Data Structure:
synthetic_data = [
    {"content_type": "news", "watch_time": random.randint(1, 10), "content_id": 1},
    ...
]
•	content_type: Type of content watched (education, entertainment, news, etc.).
•	watch_time: Minutes spent watching the content.
•	content_id: Unique identifier for the content.
### Tracking Variables:
•	entertainment_time: Total time spent on entertainment content.
•	productive_time: Total time spent on productive content.
•	total_watch_time: Sum of all watch times.
### Thresholds:
•	ENGAGEMENT_TIME_THRESHOLD = 15: Minimum watch time to determine consistent state.
•	MINIMUM_PERCENTAGE_THRESHOLD = 0.75: Percentage of time spent on one content type to infer the user’s state.
### Content Categorization:
•	Productive: education, documentary, news.
•	Entertainment: drama, entertainment.
•	Other: Content not classified as either.
### State Determination Methods:
1.	User Input: Asks the user their intent (focus/leisure) at the start. Early exit if clear.
2.	Search Behavior (NLP): Analyzes the user’s search query to detect focused or leisure intent.
3.	Content Engagement: Tracks total watch time and determines state based on time spent on productive vs. entertainment content.
4.	Fallback User Prompt: If no method determines the state, asks the user directly.
### Functions:
•	categorize_content(content_type): Maps content type to productive, entertainment, or other.
•	determine_state_from_search(search_query): Uses NLP to identify user state from search behavior.
•	track_user_state(data): Tracks watch time and identifies user state once the engagement threshold is met.
### Flow:
1.	Check user’s initial input. Exit early if provided.
2.	Analyze search behavior with NLP. Exit early if determined.
3.	Track engagement metrics over time to determine state.
4.	Prompt user only if no state is identified.
### Assumptions:
•	Users spend a minimum of 15 minutes engaging with content to determine behavior.
•	Users generally focus on one type of content (productive or leisure) during a session.

## 2. Slipping into Distraction Mode
This phase begins when a user diverts from productive content and starts moving toward potentially distracting content. We track their behavior to detect slipping into distraction based on the following steps:
#### •	Detecting First Diversion:
1.	When the user switches from productive content (like educational or work-related videos) to non-productive content (like entertainment), we start monitoring.
2.	We track the first instance of content from the user’s identified “drug of choice” (recurring indulgent content) or any high-reward, non-productive genres.(here we are using drug of choice and metrics to identify if the person is engaging in another content which isn’t drug of choice but still a distraction .. but care is taken that the first preference is drug of choice)
3.	That is, if in 10 min window at any point of time the person indulges/interacts with his drug of choice then that will be flagged but if he uses other content that pattern will be detected.  
#### •	10-Minute Observation Window:
1.  After detecting the first diversion, we allow a 10-minute window without any intervention.
2.	During this time, we monitor behavior but do not take action, giving the user a chance to self-correct.
##### •	Tracking Behavior Metrics:
1.	Content Switching Speed: Frequency and speed of switching between different content types.
2.	Time Between Switches: Time spent on each content type before switching.
3.	Scrolling Time: Duration spent scrolling without engaging with content.
4.  Content Repetition: Watching similar videos without exploring new topics.
5.	Drug of Choice Identification: Identifying whether the user is repeatedly engaging with their known distraction-prone content.
### •	Identifying Slipping into Distraction:
1.	If the user continues with distracting content beyond the 10-minute window and patterns of high switching speed, short time between switches, and engagement with their drug of choice emerge, we flag them as slipping into distraction.
2.  If the user returns to productive content within the 10-minute window, tracking is reset.

## 3. Nudging Mechanism (When Slipping from Focused State)
When a user has been identified as slipping into distraction from a focused state, we deploy a three-step nudging mechanism to help them return to productive behavior(but all of these occur simultaneously:
•	1. Pop-Up Notification:
1.	A gentle reminder that they’ve been away from productive content for over 10 minutes.
2.	Encouragement to return to their focused task.
•	2. Highlight Previous Productive Content:
1.  The system brings their previously watched productive content to the forefront.
2.	Novelty recommendations related to their focused content are highlighted to capture interest and ease the transition back to productivity.
•	3. Option to Resume First Diversion Content:
1.	The system offers the option to resume the first entertainment or non-productive content they switched to.
2.	This option is pushed lower in priority to subtly steer them toward more constructive content.

## 4. Tracking Full Distraction in Leisure State
When the user is in a leisure state, we monitor whether their engagement turns into full distraction:
•	Background Monitoring:
1. 	While the user engages with entertainment content, the system tracks behavior without immediate intervention.
•	Flagging Full Distraction:
1.	If the user indulges in their “drug of choice” or non-productive content for more than 45 minutes continuously, they are flagged as fully distracted.
2.	This information contributes to their distraction profile and helps tailor future nudging and recommendations.
•	Tracking Metrics:
1.  Content switching speed, time between switches, scrolling time, content repetition, and engagement with the drug of choice continue to be monitored to assess the depth of distraction.
