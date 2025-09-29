from LLMInfo import LLMInfo, load_llms_from_excel
import pandas as pd

if __name__ == "__main__":
    #  Reading real tags
    habit_df = pd.read_excel("HabitDB.xlsx")
    true_labels = habit_df.iloc[:, -1].dropna().tolist()

    #  Read LLM configuration information
    llm_dict = load_llms_from_excel("LLMs_info.xlsx")

    #  Set the general input prompt
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

Here are our examples (two habits, two non‑habits):

Example 1:
'He checks his phone before going to bed every night.' — habit  

Example 2:
'I always read a book before going to sleep.' — habit  

Example 3:
'She visited Paris last summer.' — not a habit  

Example  4:
'I jog.' — not a habit    

Now, please process the list:


['Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.', 'Immer wenn ich müde bin, mache ich Atemübungen. ', 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ', 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ', 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ', 'Nach dem Aufstehen mache ich Kraftsport', 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ', 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ', 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ', 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ', 'Morgens nach dem Aufstehen wasche ich mein Gesicht.', 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.', 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.', 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.', 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.', 'Morgens nach der Tierfütterung trinke ich einen Kaffee.', 'Nach dem Joggen trinke ich einen Proteinshake.', 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier', 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.', 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel', 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.', 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.', 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.', 'wenn ich ins DM gehe, kaufe ich mir was Süßes.', 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout', 'nach dem Abendbrot wasche ich ab', 'Nach dem Aufstehen mache ich ein paar Sprachübungen', 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe', 'Ich nehme VItamin D tabletten ein', 'Samstags putze ich das Bad.', 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.', 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade', 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ', 'Ich habe mir heute eine neue Serie auf Netflix angesehen.', 'Ich war gestern im Kino', 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren', 'Ich plane, morgen ins Schwimmbad zu gehen.', 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.', 'Ich habe heute zum ersten Mal einen Podcast gehört.', 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.', 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.', 'Ich habe letzte Woche meine Wohnung umdekoriert.', 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin', 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.', 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen', 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut', 'Ich bin an die Landschaft in den Bergen gewöhnt', 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.', 'Heute Morgen fühlte ich mich plötzlich sehr müde', 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt', 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen', 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.', 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt', 'Ich habe heute viele neue Freunde kennengelernt', 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.', 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein', 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.', 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.', 'Ich habe mir heute eine neue Pflanze gekauft.', 'Ich jogge', 'Letzte Woche war ich joggen.', 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst', 'Ich liebe Pommes Frites', 'Ich habe gestern Pommes gegessen', 'Ich mag Eis, aber nicht jedes Mal.', 'Gestern habe ich zum ersten Mal Yoga gemacht.']"""
    )

    llm_dict[
        "gpt4.1"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "gpt4.1 mini"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""
    llm_dict[
        "o3"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "o4 mini (High Effort)"
    ].output = """1. ‘Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.’ — habit  
2. ‘Immer wenn ich müde bin, mache ich Atemübungen.’ — habit  
3. ‘Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.’ — habit  
4. ‘Abends nach dem Abendbrot trinke ich ein Glas Wein.’ — habit  
5. ‘Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.’ — habit  
6. ‘Nach dem Aufstehen mache ich Kraftsport.’ — habit  
7. ‘Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.’ — habit  
8. ‘Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.’ — habit  
9. ‘Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.’ — habit  
10. ‘Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.’ — habit  
11. ‘Morgens nach dem Aufstehen wasche ich mein Gesicht.’ — habit  
12. ‘Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.’ — habit  
13. ‘Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.’ — habit  
14. ‘Morgens nach dem Gesicht‐Eincremen füttere ich die Katze.’ — habit  
15. ‘Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.’ — habit  
16. ‘Morgens nach der Tierfütterung trinke ich einen Kaffee.’ — habit  
17. ‘Nach dem Joggen trinke ich einen Proteinshake.’ — habit  
18. ‘Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier.’ — habit  
19. ‘Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.’ — habit  
20. ‘Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel.’ — habit  
21. ‘Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.’ — habit  
22. ‘Nach dem Aufstehen mache ich mir ein Zitronenwasser.’ — habit  
23. ‘Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.’ — habit  
24. ‘wenn ich ins DM gehe, kaufe ich mir was Süßes.’ — habit  
25. ‘nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout.’ — habit  
26. ‘nach dem Abendbrot wasche ich ab.’ — habit  
27. ‘Nach dem Aufstehen mache ich ein paar Sprachübungen.’ — habit  
28. ‘Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der Wohnung gehe.’ — habit  
29. ‘Ich nehme Vitamin D Tabletten ein.’ — habit  
30. ‘Samstags putze ich das Bad.’ — habit  
31. ‘Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.’ — habit  
32. ‘Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade.’ — habit  
33. ‘Nach dem Sport am Abend gehe ich oft erst spät ins Bett.’ — habit  
34. ‘Ich habe mir heute eine neue Serie auf Netflix angesehen.’ — not a habit  
35. ‘Ich war gestern im Kino.’ — not a habit  
36. ‘Ich habe vor, einen neuen Getränkegeschmack auszuprobieren.’ — not a habit  
37. ‘Ich plane, morgen ins Schwimmbad zu gehen.’ — not a habit  
38. ‘Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.’ — not a habit  
39. ‘Ich habe heute zum ersten Mal einen Podcast gehört.’ — not a habit  
40. ‘Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.’ — not a habit  
41. ‘Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.’ — not a habit  
42. ‘Ich habe letzte Woche meine Wohnung umdekoriert.’ — not a habit  
43. ‘Letzte Woche war ich auf der Hochzeit meiner besten Freundin.’ — not a habit  
44. ‘Letzte Woche war ich auf der Beerdigung eines guten Freundes.’ — not a habit  
45. ‘Ich habe vor, nächsten Mittwoch zum Arzt zu gehen.’ — not a habit  
46. ‘Mir geht es jetzt sehr schlecht, weil mein Magen weh tut.’ — not a habit  
47. ‘Ich bin an die Landschaft in den Bergen gewöhnt.’ — not a habit  
48. ‘Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.’ — not a habit  
49. ‘Heute Morgen fühlte ich mich plötzlich sehr müde.’ — not a habit  
50. ‘Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt.’ — not a habit  
51. ‘Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen.’ — not a habit  
52. ‘Ich habe mir den Rap einmal angehört und er klang ziemlich gut.’ — not a habit  
53. ‘Heute habe ich versucht zu lernen, wie man einen Kuchen backt.’ — not a habit  
54. ‘Ich habe heute viele neue Freunde kennengelernt.’ — not a habit  
55. ‘Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.’ — not a habit  
56. ‘Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein.’ — not a habit  
57. ‘Vielleicht plane ich, in Zukunft zum Militär zu gehen.’ — not a habit  
58. ‘Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.’ — not a habit  
59. ‘Ich habe mir heute eine neue Pflanze gekauft.’ — not a habit  
60. ‘Ich jogge.’ — not a habit  
61. ‘Letzte Woche war ich joggen.’ — not a habit  
62. ‘Ich habe einmal Tischtennis gespielt und es nie wieder angefasst.’ — not a habit  
63. ‘Ich liebe Pommes Frites.’ — not a habit  
64. ‘Ich habe gestern Pommes gegessen.’ — not a habit  
65. ‘Ich mag Eis, aber nicht jedes Mal.’ — not a habit  
66. ‘Gestern habe ich zum ersten Mal Yoga gemacht.’ — not a habit"""

    llm_dict[
        "o3 mini (High Effort)"
    ].output = """Below is the evaluation of each sentence according to whether it describes a recurring or routine behavior ("habit") or not ("not a habit"):

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "GPT-4o mini"
    ].output = """Here is the evaluation of each sentence based on whether it describes a habit or not:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — **habit**  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — **habit**  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — **habit**  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — **habit**  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — **habit**  
6. 'Nach dem Aufstehen mache ich Kraftsport.' — **habit**  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — **habit**  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — **habit**  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — **habit**  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — **habit**  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — **habit**  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — **habit**  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — **habit**  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — **habit**  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — **habit**  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — **habit**  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — **habit**  
18. 'Wenn ich Lust auf ein Bier/Wein habe, trinke ich ein Malzbier.' — **habit**  
19. 'Bevor ich schlafe, mache ich meine Ohrstöpsel ins Ohr.' — **habit**  
20. 'Bevor ich schlafen gehe, nehme ich meine Nahrungsergänzungsmittel.' — **habit**  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — **habit**  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — **habit**  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — **habit**  
24. 'Wenn ich ins DM gehe, kaufe ich mir was Süßes.' — **habit**  
25. 'Nach dem Aufstehen trinken und Medikamenteinnahme mache ich ein kurzes HIT Workout.' — **habit**  
26. 'Nach dem Abendbrot wasche ich ab.' — **habit**  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen.' — **habit**  
28. 'Ich prüfe, ob ich meinen Schlüssel dabeihabe, wenn ich aus der Wohnung gehe.' — **habit**  
29. 'Ich nehme Vitamin D Tabletten ein.' — **habit**  
30. 'Samstags putze ich das Bad.' — **habit**  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — **habit**  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade.' — **habit**  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett.' — **habit**  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — **not a habit**  
35. 'Ich war gestern im Kino.' — **not a habit**  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren.' — **not a habit**  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — **not a habit**  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — **not a habit**  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — **not a habit**  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — **not a habit**  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — **not a habit**  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — **not a habit**  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin.' — **not a habit**  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — **not a habit**  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen.' — **not a habit**  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut.' — **not a habit**  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt.' — **not a habit**  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — **not a habit**  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde.' — **not a habit**  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt.' — **not a habit**  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen.' — **not a habit**  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — **not a habit**  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt.' — **not a habit**  
54. 'Ich habe heute viele neue Freunde kennengelernt.' — **not a habit**  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — **not a habit**  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein.' — **not a habit**  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — **not a habit**  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — **not a habit**  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — **not a habit**  
60. 'Ich jogge.' — **habit**  
61. 'Letzte Woche war ich joggen.' — **not a habit**  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst.' — **not a habit**  
63. 'Ich liebe Pommes Frites.' — **not a habit**  
64. 'Ich habe gestern Pommes gegessen.' — **not a habit**  
65. 'Ich mag Eis, aber nicht jedes Mal.' — **not a habit**  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — **not a habit**  

Feel free to let me know if you need further clarification or adjustments!"""

    llm_dict[
        "GPT-4o"
    ].output = """Here is the evaluation of the sentences based on whether they describe a habit (recurring or routine behavior) or not:

---

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — **habit**  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — **habit**  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — **habit**  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — **habit**  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — **habit**  
6. 'Nach dem Aufstehen mache ich Kraftsport' — **habit**  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — **habit**  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — **habit**  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — **habit**  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — **habit**  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — **habit**  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — **habit**  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — **habit**  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — **habit**  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — **habit**  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — **habit**  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — **habit**  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — **habit**  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — **habit**  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — **habit**  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — **habit**  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — **habit**  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — **habit**  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — **habit**  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — **habit**  
26. 'nach dem Abendbrot wasche ich ab' — **habit**  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — **habit**  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — **habit**  
29. 'Ich nehme VItamin D tabletten ein' — **habit**  
30. 'Samstags putze ich das Bad.' — **habit**  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — **habit**  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — **habit**  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — **habit**  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — **not a habit**  
35. 'Ich war gestern im Kino' — **not a habit**  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — **not a habit**  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — **not a habit**  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — **not a habit**  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — **not a habit**  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — **not a habit**  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — **not a habit**  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — **not a habit**  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — **not a habit**  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — **not a habit**  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — **not a habit**  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — **not a habit**  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — **not a habit**  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — **not a habit**  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — **not a habit**  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — **not a habit**  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — **not a habit**  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — **not a habit**  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — **not a habit**  
54. 'Ich habe heute viele neue Freunde kennengelernt' — **not a habit**  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — **not a habit**  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — **not a habit**  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — **not a habit**  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — **not a habit**  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — **not a habit**  
60. 'Ich jogge' — **habit**  
61. 'Letzte Woche war ich joggen.' — **not a habit**  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — **not a habit**  
63. 'Ich liebe Pommes Frites' — **not a habit**  
64. 'Ich habe gestern Pommes gegessen' — **not a habit**  
65. 'Ich mag Eis, aber nicht jedes Mal.' — **not a habit**  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — **not a habit**

---

### Notes:
- **habit**: Describes a recurring or routine behavior, particularly one associated with a stimulus-response association.  
- **not a habit**: Describes a one-time action, a preference, a state, or a plan that lacks repetition or routine."""

    # （此处保留完整的66条输出）
    llm_dict[
        "Claude Sonnet 4 (Extended)"
    ].output = """Looking at each sentence to determine if it describes a recurring/routine behavior (habit) or not:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Sonnet 4"
    ].output = """I understand. Based on your examples, I can see that "I jog" is classified as "not a habit" because it's a simple statement of activity without indicating regularity or routine context. Let me evaluate each sentence:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Sonnet 3.7 (Extended)"
    ].output = """Based on your examples and definition, I'll evaluate each sentence to determine if it describes a habit - a recurring behavior with a stimulus-response association - or not:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Sonnet 3.7"
    ].output = """I'll evaluate each sentence to determine whether it describes a habit based on the definition provided and the examples. I'll pay special attention to your examples, including that "I jog" is classified as not a habit.

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Sonnet 3.5"
    ].output = """Based on the examples provided and the definition of a habit, I'll evaluate each sentence:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen...' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Opus 4 (Extended)"
    ].output = """Looking at the examples provided, I need to identify recurring/routine behaviors (habits) versus one-time events or simple statements of activities. Based on Example 4 ('I jog.' — not a habit), simply stating an activity without indicating frequency or routine is not a habit.

Here is my evaluation:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Opus 4"
    ].output = """I'll evaluate each sentence based on whether it describes a recurring or routine behavior (habit) or not.

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Claude Opus 3"
    ].output = """Here is the list of sentences classified as either describing a habit or not a habit:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Gemini 2.5 pro"
    ].output = """Based on the definition and the specific examples you provided, I have evaluated each sentence in the list. The key distinction is that a habit requires a clear recurring or routine nature, often indicated by a stimulus-response pattern, while a simple statement of an action (like "I jog") is not sufficient to be classified as a habit.

Here is the evaluation:

1.  'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2.  'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3.  'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4.  'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5.  'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6.  'Nach dem Aufstehen mache ich Kraftsport' — habit
7.  'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8.  'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9.  'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Gemini 2.0 Flash"
    ].output = """Okay, I will analyze each sentence in the list and classify it as either "habit" or "not a habit" based on the given definition and examples.

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit

"""
    llm_dict[
        "Llama 4 Maverick"
    ].output = """Here is the list with the requested classification:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""
    llm_dict[
        "Llama 4 Scout"
    ].output = """Here is the list with the classification results:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""
    llm_dict[
        "Mistral Large 2"
    ].output = """Certainly, let's evaluate each sentence to determine if it describes a habit. Here are the results:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport.' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier.' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel.' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout.' — habit
26. 'nach dem Abendbrot wasche ich ab.' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen.' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der Wohnung gehe.' — habit
29. 'Ich nehme VItamin D tabletten ein.' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade.' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett.' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino.' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren.' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin.' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen.' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut.' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt.' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde.' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt.' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen.' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt.' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt.' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein.' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge.' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst.' — not a habit
63. 'Ich liebe Pommes Frites.' — not a habit
64. 'Ich habe gestern Pommes gegessen.' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""
    llm_dict[
        "Deepseek-V3"
    ].output = """Here is the classification of each sentence as either "habit" or "not a habit" based on the given definition:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — not a habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — not a habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit  

### Key Notes:
- **Habit**: Sentences describing **recurring behaviors triggered by specific cues** (e.g., "After X, I do Y," "Whenever X happens, I do Y," or "Every Saturday I do Z").  
- **Not a Habit**:  
  - One-time actions (e.g., "Gestern habe ich Yoga gemacht").  
  - General preferences/statements (e.g., "Ich jogge," "Ich liebe Pommes").  
  - Intentions/plans (e.g., "Ich plane, morgen ins Schwimmbad zu gehen").  
  - Emotional states or external events (e.g., "Mir geht es schlecht," "Es regnete plötzlich").  

Let me know if you'd like further refinements!
"""

    llm_dict[
        "Llama-3.2-3B"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — not a habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — not a habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — not a habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — not a habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — not a habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — not a habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — not a habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — not a habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — not a habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — not a habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — not a habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — not a habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — not a habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — not a habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — not a habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — not a habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — not a habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — not a habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — not a habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — not a habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — not a habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — not a habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — not a habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — not a habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — not a habit
26. 'nach dem Abendbrot wasche ich ab' — not a habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — not a habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — not a habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — not a habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — not a habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — not a habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — not a habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""
    llm_dict[
        "Llama-3.2-3B"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — not a habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — not a habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — not a habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — not a habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — not a habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — not a habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — not a habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — not a habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — not a habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — not a habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — not a habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — not a habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — not a habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — not a habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — not a habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — not a habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — not a habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — not a habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — not a habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — not a habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — not a habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — not a habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — not a habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — not a habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — not a habit
26. 'nach dem Abendbrot wasche ich ab' — not a habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — not a habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — not a habit
29. 'Ich nehme VItamin D tabletten ein' — not a habit
30. 'Samstags putze ich das Bad.' — not a habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — not a habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — not a habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — not a habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""

    llm_dict[
        "Llama-3.1-8B"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit\n2. 'Immer wenn ich müde bin, mache ich Atemübungen.'— habit\n3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.'— habit\n4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.'— habit\n5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.'— habit\n6. 'Nach dem Aufstehen mache ich Kraftsport' — habit\n7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.'— habit\n8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.'— habit\n9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.'— habit\n10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.'— habit\n11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit\n12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit\n13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit\n14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit\n15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit\n16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit\n17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit\n18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit\n19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit\n20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit\n21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit\n22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit\n23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit\n24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit\n25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit\n26. 'nach dem Abendbrot wasche ich ab' — habit\n27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit\n28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit\n29. 'Ich nehme VItamin D tabletten ein' — habit\n30. 'Samstags putze ich das Bad.' — habit\n31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit\n32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit\n33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett'— habit\n34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit\n35. 'Ich war gestern im Kino' — not a habit\n36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit\n37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit\n38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit\n39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit\n40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit\n41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit\n42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit\n43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit\n44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit\n45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — habit\n46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit\n47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit\n48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit\n49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit\n50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit\n51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit\n52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit\n53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit\n54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit\n55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit\n56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit\n57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit\n58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit\n59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit\n60. 'Ich jogge' — habit\n61. 'Letzte Woche war ich joggen.' — habit\n62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit\n63. 'Ich liebe Pommes Frites' — habit\n64. 'Ich habe gestern Pommes gegessen' — habit\n65. 'Ich mag Eis, aber nicht jedes Mal.' — habit\n66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — habit
"""

    llm_dict[
        "DeepSeek-Coder-V2-Lite-Instruct"
    ].output = """ Here is the evaluation of the sentences provided, classifying each as either a habit or not a habit:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — not a habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke ich einen Cappucino.' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — not a habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "DeepSeek-R1"
    ].output = """

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — not a habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""

    llm_dict[
        "Llama-3.3-70B-Instruct"
    ].output = """Here is the list with the classification results:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — habit
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — habit
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit
26. 'nach dem Abendbrot wasche ich ab' — habit
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit
29. 'Ich nehme VItamin D tabletten ein' — habit
30. 'Samstags putze ich das Bad.' — habit
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett' — habit
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit
35. 'Ich war gestern im Kino' — not a habit
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit
60. 'Ich jogge' — not a habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit

Note that sentences 1-33 describe recurring or routine behaviors, which are classified as habits. Sentences 34-66 do not describe habits, but rather one-time events, plans, or preferences.
"""

    llm_dict["Mistral-7B-Instruct-v0.3"].output = (
        """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kaffee.' — habit\n2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit\n3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — not a habit (This is a response to a specific emotion, not a recurring behavior)\n4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit\n5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit\n6. 'Nach dem Aufstehen mache ich Kraftsport' — habit\n7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — not a habit (This is a response to a specific task, not a recurring behavior)\n8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — not a habit (This is a response to a specific event, not a recurring behavior)\n9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit\n10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit\n11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit\n12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit\n13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit\n14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit\n15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit\n16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit\n17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit\n18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit\n19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit\n20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit\n21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — not a habit (This is a response to a specific stress level, not a recurring behavior)\n22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit\n23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — not a habit (This is a response to a specific situation, not a recurring behavior)\n24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit\n25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit\n26. 'nach dem Abendbrot wasche ich ab' — habit\n27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit\n28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit\n29. 'Ich nehme VItamin D tabletten ein' — habit\n30. 'Samstags putze ich das Bad.' — habit\n31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit\n32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit\n33. 'Nach dem Sport am Abend gehe ich oft spät ins Bett'— habit\n34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit (This is a one-time event, not a recurring behavior)\n35. 'Ich war gestern im Kino' — not a habit (This is a one-time event, not a recurring behavior)\n36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit (This is a future intention, not a recurring behavior)\n37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit (This is a future intention, not a recurring behavior)\n38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit (This is a one-time event, not a recurring behavior)\n39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit (This is a one-time event, not a recurring behavior)\n40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit (This is a one-time event, not a recurring behavior)\n41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit (This is a one-time event, not a recurring behavior)\n42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit (This is a one-time event, not a recurring behavior)\n43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit (This is a one-time event, not a recurring behavior)\n44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit (This is a one-time event, not a recurring behavior)\n45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit (This is a future intention, not a recurring behavior)\n46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit (This is a current health issue, not a recurring behavior)\n47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit (This is a preference, not a recurring behavior)\n48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit (This is a one-time event, not a recurring behavior)\n49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit (This is a current feeling, not a recurring behavior)\n50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit (This is a preference, not a recurring behavior)\n51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit (This is a response to a specific weather condition, not a recurring behavior)\n52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit (This is a one-time event, not a recurring behavior)\n53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit (This is a one-time event, not a recurring behavior)\n54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit (This is a one-time event, not a recurring behavior)\n55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit (This is a one-time event, not a recurring behavior)\n56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit (This is a recurring issue, but not a behavior)\n57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit (This is a future intention, not a recurring behavior)\n58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit (This is a one-time event, not a recurring behavior)\n59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit (This is a one-time event, not a recurring behavior)\n60. 'Ich jogge' — habit\n61. 'Letzte Woche war ich joggen.' — not a habit (This is a one-time event, not a recurring behavior)\n62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit (This is a one-time event, not a recurring behavior)\n63. 'Ich liebe Pommes Frites' — not a habit (This is a preference, not a recurring behavior)\n64. 'Ich habe gestern Pommes gegessen' — not a habit (This is a one-time event, not a recurring behavior)\n65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit (This is a preference, not a recurring behavior)\n66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit (This is a one-time event, not a recurring behavior)"""
    )

    llm_dict[
        "Qwen3-8B"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit  
2. 'Immer wenn ich müde bin, mache ich Atemübungen. ' — habit  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ' — not a habit  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ' — habit  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — not a habit  
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit  
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit  
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — habit  
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ' — habit  
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ' — not a habit  
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit  
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit  
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit  
14. 'Morgens nach dem Gesicht-Ecremen füttere ich die Katze.' — habit  
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit  
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit  
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit  
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — not a habit  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit  
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — not a habit  
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit  
26. 'nach dem Abendbrot wasche ich ab' — not a habit  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der Wohnung gehe' — habit  
29. 'Ich nehme VItamin D tabletten ein' — habit  
30. 'Samstags putze ich das Bad.' — habit  
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit  
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit  
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — habit  
34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit  
35. 'Ich war gestern im Kino' — not a habit  
36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit  
37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit  
38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit  
39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit  
40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit  
41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit  
42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit  
43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit  
44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit  
45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit  
46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit  
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit  
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit  
49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit  
50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit  
51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit  
52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit  
53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit  
54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit  
55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit  
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit  
57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit  
58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit  
59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit  
60. 'Ich jogge' — not a habit  
61. 'Letzte Woche war ich joggen.' — not a habit  
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit  
63. 'Ich liebe Pommes Frites' — not a habit  
64. 'Ich habe gestern Pommes gegessen' — not a habit  
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit  
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""


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
    "llm_all_info_with_cost_performance_fewshot_with_definition.xlsx", index=False
)
