from LLMInfo import LLMInfo, load_llms_from_excel
import pandas as pd

if __name__ == "__main__":
    habit_df = pd.read_excel("HabitDB.xlsx")
    true_labels = habit_df.iloc[:, -1].dropna().tolist()
    llm_dict = load_llms_from_excel("LLMs_info.xlsx")
    LLMInfo.set_input_prompt(
        """You are a habit recognition expert.

habit is a process by which a stimulus generates an impulse to act as a result of a learned stimulus-response association. Habit-generated impulses may compete or combine with impulses and inhibitions arising from other sources, including conscious decisionmaking, to influence responses, and need not generate behaviour.

Your task is to determine whether each sentence in a given list describes a habit.

The input is a list of 66 sentences, each enclosed in single quotation marks ('').  
Please evaluate the sentences in the exact order they appear in the list.

For each sentence, assign one of the following labels:  
- "habit" if the sentence describes a recurring or routine behavior,  
- "not a habit" if it does not.

The output should be a numbered list. Each item should include the sentence and your classification result in the following format:

[Number]. [Sentence] — [Label]

Here is a structured one‑shot example to show how to answer:

Example:
'He checks his phone before going to bed every night.' — habit  

Now, please process the list:


['In the morning after getting up, I immediately drink coffee.', 'Whenever I am tired, I do breathing exercises.', 'When I feel a negative emotion strongly, I try to feel it out.', 'In the evening after dinner, I drink a glass of wine.', 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.', 'After getting up, I do weight training.', 'As soon as I see a task, I enter it in Notion.', 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.', 'If no one is expecting me at home after work, I walk home.', 'Once a month, I spend a day alone in Dresden.', 'In the morning after getting up, I wash my face.', 'In the morning/evening after washing my face, I brush my teeth.', 'In the morning/evening after brushing my teeth, I moisturize my face.', 'In the morning after applying face cream, I feed the cat.', 'In the morning after feeding the cat, the dog gets a chew stick.', 'In the morning after feeding the animals, I drink a coffee.', 'After jogging, I drink a protein shake.', 'If I feel like having a beer or wine, I drink a malt beer.', 'Before I go to sleep, I put in my earplugs.', 'Before I go to sleep, I take my supplements.', "If I'm stressed, I go to the fridge and get something to eat.", 'After getting up, I make myself some lemon water.', 'When I go to bed in the evening, I scroll mindlessly through social media.', 'When I go to DM, I buy myself something sweet.', 'After getting up, after drinking and taking my medication, I do a short HIIT workout.', 'After dinner, I wash the dishes.', 'After getting up, I do some language exercises.', 'I check whether I have my key with me when I leave the apartment.', 'I take vitamin D tablets.', 'On Saturdays, I clean the bathroom.', "If it doesn't rain, I water the apple tree every day in the summer.", 'After dinner on a stressful day, I like to eat a piece of chocolate.', 'After exercising in the evening, I often go to bed late.', 'I watched a new series on Netflix today.', 'I went to the cinema yesterday.', 'I plan to try a new flavor of drink.', 'I plan to go to the swimming pool tomorrow.', 'I visited my friends in another city over the weekend.', 'I listened to a podcast for the first time today.', 'I took a selfie with my new camera for the first time today.', 'Today I took a long walk through an unfamiliar area.', 'I redecorated my apartment last week.', "Last week I went to my best friend's wedding.", "Last week I went to a good friend's funeral.", 'I plan to go to the doctor next Wednesday.', 'I feel very bad right now because my stomach hurts.', "I'm used to the scenery in the mountains.", "Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.", 'This morning I suddenly felt very tired.', 'Oatmeal tastes better when you add blueberries to it.', "It's raining today, so I don't want to go to the gym.", 'I listened to the rap once and it sounded pretty good.', 'Today I tried to learn how to bake a cake.', 'I met a lot of new friends today.', 'I ordered a lot of new furniture today to decorate my new house.', 'When I try to pay, the website keeps freezing for some unknown reason.', 'Maybe I plan to join the military in the future.', 'I watched a movie in English without subtitles yesterday.', 'I bought a new plant today.', "I go jogging.", 'Last week I went jogging.', 'I played table tennis once and never touched it again.', 'I love French fries.', 'I ate French fries yesterday.', "I like ice cream, but not every time.", 'Yesterday I did yoga for the first time.']"""
    )
    llm_dict[
        "gpt4.1"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit  
9. 'If no one is expecting me at home after work, I walk home.' — habit  
10. 'Once a month, I spend a day alone in Dresden.' — habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit  
33. 'After exercising in the evening, I often go to bed late.' — habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — not a habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""

    llm_dict[
        "gpt4.1 mini"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — not a habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — not a habit  
9. 'If no one is expecting me at home after work, I walk home.' — not a habit  
10. 'Once a month, I spend a day alone in Dresden.' — not a habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — not a habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — not a habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — not a habit  
33. 'After exercising in the evening, I often go to bed late.' — not a habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""
    llm_dict[
        "o3"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit  
9. 'If no one is expecting me at home after work, I walk home.' — habit  
10. 'Once a month, I spend a day alone in Dresden.' — habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit  
33. 'After exercising in the evening, I often go to bed late.' — habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — not a habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""

    llm_dict[
        "o4 mini (High Effort)"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit  
9. 'If no one is expecting me at home after work, I walk home.' — habit  
10. 'Once a month, I spend a day alone in Dresden.' — habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit  
33. 'After exercising in the evening, I often go to bed late.' — habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — not a habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""


    llm_dict[
        "o3 mini (High Effort)"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit  
9. 'If no one is expecting me at home after work, I walk home.' — habit  
10. 'Once a month, I spend a day alone in Dresden.' — habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit  
33. 'After exercising in the evening, I often go to bed late.' — habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — not a habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""

    llm_dict[
        "GPT-4o mini"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — not a habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — not a habit  
9. 'If no one is expecting me at home after work, I walk home.' — not a habit  
10. 'Once a month, I spend a day alone in Dresden.' — not a habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — not a habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — not a habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — not a habit  
33. 'After exercising in the evening, I often go to bed late.' — not a habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""


    llm_dict[
        "GPT-4o"
    ].output = """1. 'In the morning after getting up, I immediately drink coffee.' — habit
2. 'Whenever I am tired, I do breathing exercises.' — habit
3. 'When I feel a negative emotion strongly, I try to feel it out.' — not a habit
4. 'In the evening after dinner, I drink a glass of wine.' — habit
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit
6. 'After getting up, I do weight training.' — habit
7. 'As soon as I see a task, I enter it in Notion.' — habit
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — not a habit
9. 'If no one is expecting me at home after work, I walk home.' — not a habit
10. 'Once a month, I spend a day alone in Dresden.' — habit
11. 'In the morning after getting up, I wash my face.' — habit
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit
14. 'In the morning after applying face cream, I feed the cat.' — habit
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit
16. 'In the morning after feeding the animals, I drink a coffee.' — habit
17. 'After jogging, I drink a protein shake.' — habit
18. 'If I feel like having a beer or wine, I drink a malt beer.' — not a habit
19. 'Before I go to sleep, I put in my earplugs.' — habit
20. 'Before I go to sleep, I take my supplements.' — habit
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit
22. 'After getting up, I make myself some lemon water.' — habit
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit
24. 'When I go to DM, I buy myself something sweet.' — habit
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit
26. 'After dinner, I wash the dishes.' — habit
27. 'After getting up, I do some language exercises.' — habit
28. 'I check whether I have my key with me when I leave the apartment.' — habit
29. 'I take vitamin D tablets.' — habit
30. 'On Saturdays, I clean the bathroom.' — habit
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit
33. 'After exercising in the evening, I often go to bed late.' — habit
34. 'I watched a new series on Netflix today.' — not a habit
35. 'I went to the cinema yesterday.' — not a habit
36. 'I plan to try a new flavor of drink.' — not a habit
37. 'I plan to go to the swimming pool tomorrow.' — not a habit
38. 'I visited my friends in another city over the weekend.' — not a habit
39. 'I listened to a podcast for the first time today.' — not a habit
40. 'I took a selfie with my new camera for the first time today.' — not a habit
41. 'Today I took a long walk through an unfamiliar area.' — not a habit
42. 'I redecorated my apartment last week.' — not a habit
43. 'Last week I went to my best friend's wedding.' — not a habit
44. 'Last week I went to a good friend's funeral.' — not a habit
45. 'I plan to go to the doctor next Wednesday.' — not a habit
46. 'I feel very bad right now because my stomach hurts.' — not a habit
47. 'I'm used to the scenery in the mountains.' — not a habit
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit
49. 'This morning I suddenly felt very tired.' — not a habit
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit
51. 'It's raining today, so I don't want to go to the gym.' — not a habit
52. 'I listened to the rap once and it sounded pretty good.' — not a habit
53. 'Today I tried to learn how to bake a cake.' — not a habit
54. 'I met a lot of new friends today.' — not a habit
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit
57. 'Maybe I plan to join the military in the future.' — not a habit
58. 'I watched a movie in English without subtitles yesterday.' — not a habit
59. 'I bought a new plant today.' — not a habit
60. 'I go jogging.' — habit
61. 'Last week I went jogging.' — not a habit
62. 'I played table tennis once and never touched it again.' — not a habit
63. 'I love French fries.' — not a habit
64. 'I ate French fries yesterday.' — not a habit
65. 'I like ice cream, but not every time.' — not a habit
66. 'Yesterday I did yoga for the first time.' — not a habit"""


    llm_dict[
        "DeepSeek-Coder-V2-Lite-Instruct"
    ].output = """ Here is the evaluation of each sentence based on the definition of a habit:

1. 'In the morning after getting up, I immediately drink coffee.' — habit
2. 'Whenever I am tired, I do breathing exercises.' — habit
3. 'When I feel a negative emotion strongly, I try to feel it out.' — habit
4. 'In the evening after dinner, I drink a glass of wine.' — habit
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit
6. 'After getting up, I do weight training.' — habit
7. 'As soon as I see a task, I enter it in Notion.' — habit
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit
9. 'If no one is expecting me at home after work, I walk home.' — habit
10. 'Once a month, I spend a day alone in Dresden.' — habit
11. 'In the morning after getting up, I wash my face.' — habit
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit
14. 'In the morning after applying face cream, I feed the cat.' — habit
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit
16. 'In the morning after feeding the animals, I drink a coffee.' — habit
17. 'After jogging, I drink a protein shake.' — habit
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit
19. 'Before I go to sleep, I put in my earplugs.' — habit
20. 'Before I go to sleep, I take my supplements.' — habit
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit
22. 'After getting up, I make myself some lemon water.' — habit
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit
24. 'When I go to DM, I buy myself something sweet.' — habit
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit
26. 'After dinner, I wash the dishes.' — habit
27. 'After getting up, I do some language exercises.' — habit
28. 'I check whether I have my key with me when I leave the apartment.' — habit
29. 'I take vitamin D tablets.' — habit
30. 'On Saturdays, I clean the bathroom.' — habit
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit
33. 'After exercising in the evening, I often go to bed late.' — habit
34. 'I watched a new series on Netflix today.' — not a habit
35. 'I went to the cinema yesterday.' — not a habit
36. 'I plan to try a new flavor of drink.' — not a habit
37. 'I plan to go to the swimming pool tomorrow.' — not a habit
38. 'I visited my friends in another city over the weekend.' — not a habit
39. 'I listened to a podcast for the first time today.' — not a habit
40. 'I took a selfie with my new camera for the first time today.' — not a habit
41. 'Today I took a long walk through an unfamiliar area.' — not a habit
42. 'I redecorated my apartment last week.' — not a habit
43. 'Last week I went to my best friend's wedding.' — not a habit
44. 'Last week I went to a good friend's funeral.' — not a habit
45. 'I plan to go to the doctor next Wednesday.' — not a habit
46. 'I feel very bad right now because my stomach hurts.' — not a habit
47. 'I'm used to the scenery in the mountains.' — not a habit
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit
49. 'This morning I suddenly felt very tired.' — not a habit
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit
51. 'It's raining today, so I don't want to go to the gym.' — not a habit
52. 'I listened to the rap once and it sounded pretty good.' — not a habit
53. 'Today I tried to learn how to bake a cake.' — not a habit
54. 'I met a lot of new friends today.' — not a habit
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit
57. 'Maybe I plan to join the military in the future.' — not a habit
58. 'I watched a movie in English without subtitles yesterday.' — not a habit
59. 'I bought a new plant today.' — not a habit
60. 'I go jogging.' — not a habit
61. 'Last week I went jogging.' — not a habit
62. 'I played table tennis once and never touched it again.' — not a habit
63. 'I love French fries.' — not a habit
64. 'I ate French fries yesterday.' — not a habit
65. 'I like ice cream, but not every time.' — not a habit
66. 'Yesterday I did yoga for the first time.' — not a habit"""

    llm_dict[
        "DeepSeek-R1"
    ].output = """

1. 'In the morning after getting up, I immediately drink coffee.' — habit  
2. 'Whenever I am tired, I do breathing exercises.' — habit  
3. 'When I feel a negative emotion strongly, I try to feel it out.' — not a habit  
4. 'In the evening after dinner, I drink a glass of wine.' — habit  
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit  
6. 'After getting up, I do weight training.' — habit  
7. 'As soon as I see a task, I enter it in Notion.' — habit  
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit  
9. 'If no one is expecting me at home after work, I walk home.' — not a habit  
10. 'Once a month, I spend a day alone in Dresden.' — not a habit  
11. 'In the morning after getting up, I wash my face.' — habit  
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit  
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit  
14. 'In the morning after applying face cream, I feed the cat.' — habit  
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit  
16. 'In the morning after feeding the animals, I drink a coffee.' — habit  
17. 'After jogging, I drink a protein shake.' — habit  
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit  
19. 'Before I go to sleep, I put in my earplugs.' — habit  
20. 'Before I go to sleep, I take my supplements.' — habit  
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit  
22. 'After getting up, I make myself some lemon water.' — habit  
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit  
24. 'When I go to DM, I buy myself something sweet.' — habit  
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit  
26. 'After dinner, I wash the dishes.' — habit  
27. 'After getting up, I do some language exercises.' — habit  
28. 'I check whether I have my key with me when I leave the apartment.' — habit  
29. 'I take vitamin D tablets.' — habit  
30. 'On Saturdays, I clean the bathroom.' — habit  
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit  
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — not a habit  
33. 'After exercising in the evening, I often go to bed late.' — not a habit  
34. 'I watched a new series on Netflix today.' — not a habit  
35. 'I went to the cinema yesterday.' — not a habit  
36. 'I plan to try a new flavor of drink.' — not a habit  
37. 'I plan to go to the swimming pool tomorrow.' — not a habit  
38. 'I visited my friends in another city over the weekend.' — not a habit  
39. 'I listened to a podcast for the first time today.' — not a habit  
40. 'I took a selfie with my new camera for the first time today.' — not a habit  
41. 'Today I took a long walk through an unfamiliar area.' — not a habit  
42. 'I redecorated my apartment last week.' — not a habit  
43. 'Last week I went to my best friend's wedding.' — not a habit  
44. 'Last week I went to a good friend's funeral.' — not a habit  
45. 'I plan to go to the doctor next Wednesday.' — not a habit  
46. 'I feel very bad right now because my stomach hurts.' — not a habit  
47. 'I'm used to the scenery in the mountains.' — not a habit  
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit  
49. 'This morning I suddenly felt very tired.' — not a habit  
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit  
51. 'It's raining today, so I don't want to go to the gym.' — not a habit  
52. 'I listened to the rap once and it sounded pretty good.' — not a habit  
53. 'Today I tried to learn how to bake a cake.' — not a habit  
54. 'I met a lot of new friends today.' — not a habit  
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit  
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit  
57. 'Maybe I plan to join the military in the future.' — not a habit  
58. 'I watched a movie in English without subtitles yesterday.' — not a habit  
59. 'I bought a new plant today.' — not a habit  
60. 'I go jogging.' — habit  
61. 'Last week I went jogging.' — not a habit  
62. 'I played table tennis once and never touched it again.' — not a habit  
63. 'I love French fries.' — not a habit  
64. 'I ate French fries yesterday.' — not a habit  
65. 'I like ice cream, but not every time.' — not a habit  
66. 'Yesterday I did yoga for the first time.' — not a habit"""

    llm_dict[
        "Llama-3.3-70B-Instruct"
    ].output = """Here is the list with each sentence classified as either "habit" or "not a habit":

1. 'In the morning after getting up, I immediately drink coffee.' — habit
2. 'Whenever I am tired, I do breathing exercises.' — habit
3. 'When I feel a negative emotion strongly, I try to feel it out.' — habit
4. 'In the evening after dinner, I drink a glass of wine.' — habit
5. 'If I go to the bakery on the weekend, I stop by my favorite cafe and drink a cappuccino.' — habit
6. 'After getting up, I do weight training.' — habit
7. 'As soon as I see a task, I enter it in Notion.' — habit
8. 'If Teams shows me that a colleague is in an EvalGiGe meeting, I join the meeting.' — habit
9. 'If no one is expecting me at home after work, I walk home.' — habit
10. 'Once a month, I spend a day alone in Dresden.' — habit
11. 'In the morning after getting up, I wash my face.' — habit
12. 'In the morning/evening after washing my face, I brush my teeth.' — habit
13. 'In the morning/evening after brushing my teeth, I moisturize my face.' — habit
14. 'In the morning after applying face cream, I feed the cat.' — habit
15. 'In the morning after feeding the cat, the dog gets a chew stick.' — habit
16. 'In the morning after feeding the animals, I drink a coffee.' — habit
17. 'After jogging, I drink a protein shake.' — habit
18. 'If I feel like having a beer or wine, I drink a malt beer.' — habit
19. 'Before I go to sleep, I put in my earplugs.' — habit
20. 'Before I go to sleep, I take my supplements.' — habit
21. 'If I'm stressed, I go to the fridge and get something to eat.' — habit
22. 'After getting up, I make myself some lemon water.' — habit
23. 'When I go to bed in the evening, I scroll mindlessly through social media.' — habit
24. 'When I go to DM, I buy myself something sweet.' — habit
25. 'After getting up, after drinking and taking my medication, I do a short HIIT workout.' — habit
26. 'After dinner, I wash the dishes.' — habit
27. 'After getting up, I do some language exercises.' — habit
28. 'I check whether I have my key with me when I leave the apartment.' — habit
29. 'I take vitamin D tablets.' — habit
30. 'On Saturdays, I clean the bathroom.' — habit
31. 'If it doesn't rain, I water the apple tree every day in the summer.' — habit
32. 'After dinner on a stressful day, I like to eat a piece of chocolate.' — habit
33. 'After exercising in the evening, I often go to bed late.' — habit
34. 'I watched a new series on Netflix today.' — not a habit
35. 'I went to the cinema yesterday.' — not a habit
36. 'I plan to try a new flavor of drink.' — not a habit
37. 'I plan to go to the swimming pool tomorrow.' — not a habit
38. 'I visited my friends in another city over the weekend.' — not a habit
39. 'I listened to a podcast for the first time today.' — not a habit
40. 'I took a selfie with my new camera for the first time today.' — not a habit
41. 'Today I took a long walk through an unfamiliar area.' — not a habit
42. 'I redecorated my apartment last week.' — not a habit
43. 'Last week I went to my best friend's wedding.' — not a habit
44. 'Last week I went to a good friend's funeral.' — not a habit
45. 'I plan to go to the doctor next Wednesday.' — not a habit
46. 'I feel very bad right now because my stomach hurts.' — not a habit
47. 'I'm used to the scenery in the mountains.' — not a habit
48. 'Last Wednesday it suddenly rained, so I went to a cafe I hadn't been to before to seek shelter from the rain, and I found that I really liked it.' — not a habit
49. 'This morning I suddenly felt very tired.' — not a habit
50. 'Oatmeal tastes better when you add blueberries to it.' — not a habit
51. 'It's raining today, so I don't want to go to the gym.' — not a habit
52. 'I listened to the rap once and it sounded pretty good.' — not a habit
53. 'Today I tried to learn how to bake a cake.' — not a habit
54. 'I met a lot of new friends today.' — not a habit
55. 'I ordered a lot of new furniture today to decorate my new house.' — not a habit
56. 'When I try to pay, the website keeps freezing for some unknown reason.' — not a habit
57. 'Maybe I plan to join the military in the future.' — not a habit
58. 'I watched a movie in English without subtitles yesterday.' — not a habit
59. 'I bought a new plant today.' — not a habit
60. 'I go jogging.' — habit
61. 'Last week I went jogging.' — not a habit
62. 'I played table tennis once and never touched it again.' — not a habit
63. 'I love French fries.' — not a habit
64. 'I ate French fries yesterday.' — not a habit
65. 'I like ice cream, but not every time.' — not a habit
66. 'Yesterday I did yoga for the first time.' — not a habit

Note: Some sentences may describe actions that could potentially become habits, but based on the information provided, they do not currently meet the criteria for a habit."""

def evaluate_and_report(llm_dict: dict, true_labels: list, metric_names: list = None):
    if metric_names is None:
        metric_names = ["accuracy", "precision", "recall", "f1", "mcc", "kappa"]

    for name, model in llm_dict.items():
        try:
            model.evaluate(true_labels)
        except Exception as e:
            continue
        try:
            model.get_cost_performance()
        except Exception as e:
            continue


import pandas as pd


def summarize_llm_full_info(
    llm_dict: dict, preview_output_len: int = 50
) -> pd.DataFrame:
    """
    Displays complete information about the LLM, including cost, output preview, evaluation metrics, and all price/performance indicators.
    """
    records = []
    for llm in llm_dict.values():
        if llm.metrics is None or llm.cost is None or not llm.cost_performance:
            continue

        try:
            prompt_tokens = llm.tokenizer_fn(LLMInfo.input_prompt)
            output_tokens = llm.tokenizer_fn(llm.output)
        except Exception as e:
            prompt_tokens = -1
            output_tokens = -1
            print(f"[Token Count Error] {llm.name}: {e}")

        record = {
            "Model": llm.name,
            "Input Cost / 1M": llm.input_cost,
            "Output Cost / 1M": llm.output_cost,
            "Prompt Token Count": prompt_tokens,
            "Output Token Count": output_tokens,
            "Total Cost (USD)": round(llm.cost, 6),
            "Output Preview": llm.output[:preview_output_len].replace("\n", " "),
            # Classification indicators
            "Accuracy": round(llm.metrics.get("accuracy", 0), 4),
            "Precision": round(llm.metrics.get("precision", 0), 4),
            "Recall": round(llm.metrics.get("recall", 0), 4),
            "F1-Score": round(llm.metrics.get("f1", 0), 4),
            "MCC": round(llm.metrics.get("mcc", 0), 4),
            "Kappa": round(llm.metrics.get("kappa", 0), 4),
            # Cost-effectiveness index (each item divided by cost)
            "Accuracy / Cost": round(llm.cost_performance.get("accuracy", 0), 4),
            "Precision / Cost": round(llm.cost_performance.get("precision", 0), 4),
            "Recall / Cost": round(llm.cost_performance.get("recall", 0), 4),
            "F1 / Cost": round(llm.cost_performance.get("f1", 0), 4),
            "MCC / Cost": round(llm.cost_performance.get("mcc", 0), 4),
            "Kappa / Cost": round(llm.cost_performance.get("kappa", 0), 4),
        }
        records.append(record)

    df = pd.DataFrame(records)
    return df

evaluate_and_report(
    llm_dict,
    true_labels,
    metric_names=["accuracy", "precision", "recall", "f1", "mcc", "kappa"],
)
df = summarize_llm_full_info(llm_dict, 20)
df.to_excel(
    "EN_llm_all_info_with_cost_performance_oneshot_with_definition.xlsx", index=False
)
