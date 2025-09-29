from LLMInfo import LLMInfo, load_llms_from_excel
import pandas as pd

if __name__ == "__main__":
    habit_df = pd.read_excel("HabitDB.xlsx")
    true_labels = habit_df.iloc[:, -1].dropna().tolist()
    llm_dict = load_llms_from_excel("LLMs_info.xlsx")
    LLMInfo.set_input_prompt(
        """You are a habit recognition expert.

Your task is to determine whether each sentence in a given list describes a habit.

The input is a list of 66 sentences, each enclosed in single quotation marks ('').  
Please evaluate the sentences in the exact order they appear in the list.

For each sentence, assign one of the following labels:  
- "habit" if the sentence describes a recurring or routine behavior,  
- "not a habit" if it does not.

The output should be a numbered list. Each item should include the sentence and your classification result in the following format:

[Number]. [Sentence] — [Label]

Now, please process the list:


['Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.', 'Immer wenn ich müde bin, mache ich Atemübungen. ', 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ', 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ', 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ', 'Nach dem Aufstehen mache ich Kraftsport', 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ', 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ', 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ', 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ', 'Morgens nach dem Aufstehen wasche ich mein Gesicht.', 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.', 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.', 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.', 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.', 'Morgens nach der Tierfütterung trinke ich einen Kaffee.', 'Nach dem Joggen trinke ich einen Proteinshake.', 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier', 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.', 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel', 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.', 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.', 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.', 'wenn ich ins DM gehe, kaufe ich mir was Süßes.', 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout', 'nach dem Abendbrot wasche ich ab', 'Nach dem Aufstehen mache ich ein paar Sprachübungen', 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe', 'Ich nehme VItamin D tabletten ein', 'Samstags putze ich das Bad.', 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.', 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade', 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ', 'Ich habe mir heute eine neue Serie auf Netflix angesehen.', 'Ich war gestern im Kino', 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren', 'Ich plane, morgen ins Schwimmbad zu gehen.', 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.', 'Ich habe heute zum ersten Mal einen Podcast gehört.', 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.', 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.', 'Ich habe letzte Woche meine Wohnung umdekoriert.', 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin', 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.', 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen', 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut', 'Ich bin an die Landschaft in den Bergen gewöhnt', 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.', 'Heute Morgen fühlte ich mich plötzlich sehr müde', 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt', 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen', 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.', 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt', 'Ich habe heute viele neue Freunde kennengelernt', 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.', 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein', 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.', 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.', 'Ich habe mir heute eine neue Pflanze gekauft.', 'Ich jogge', 'Letzte Woche war ich joggen.', 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst', 'Ich liebe Pommes Frites', 'Ich habe gestern Pommes gegessen', 'Ich mag Eis, aber nicht jedes Mal.', 'Gestern habe ich zum ersten Mal Yoga gemacht.']"""
    )

    llm_dict[
        "gpt4.1"
    ].output = """#### Habit Recognition Analysis

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — **habit**
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — **habit**
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — **habit**
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — **habit**
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — **habit**
6. 'Nach dem Aufstehen mache ich Kraftsport' — **habit**
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
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — **not a habit**"""

    llm_dict[
        "gpt4.1 mini"
    ].output = """#### Habit Recognition Results

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
        "o3"
    ].output = """#### Klassifizierung der Sätze

1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — **habit**  
2. Immer wenn ich müde bin, mache ich Atemübungen. — **habit**  
3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — **habit**  
4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — **habit**  
5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — **habit**  
6. Nach dem Aufstehen mache ich Kraftsport — **habit**  
7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — **habit**  
8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — **habit**  
9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — **habit**  
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — **habit**  
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — **habit**  
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — **habit**  
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — **habit**  
14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — **habit**  
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — **habit**  
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — **habit**  
17. Nach dem Joggen trinke ich einen Proteinshake. — **habit**  
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — **habit**  
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — **habit**  
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — **habit**  
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — **habit**  
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — **habit**  
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — **habit**  
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — **habit**  
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — **habit**  
26. nach dem Abendbrot wasche ich ab — **habit**  
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — **habit**  
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe — **habit**  
29. Ich nehme VItamin D tabletten ein — **habit**  
30. Samstags putze ich das Bad. — **habit**  
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — **habit**  
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — **habit**  
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett  — **habit**  
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — **not a habit**  
35. Ich war gestern im Kino — **not a habit**  
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — **not a habit**  
37. Ich plane, morgen ins Schwimmbad zu gehen. — **not a habit**  
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — **not a habit**  
39. Ich habe heute zum ersten Mal einen Podcast gehört. — **not a habit**  
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — **not a habit**  
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — **not a habit**  
42. Ich habe letzte Woche meine Wohnung umdekoriert. — **not a habit**  
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — **not a habit**  
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — **not a habit**  
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — **not a habit**  
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — **not a habit**  
47. Ich bin an die Landschaft in den Bergen gewöhnt — **not a habit**  
48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — **not a habit**  
49. Heute Morgen fühlte ich mich plötzlich sehr müde — **not a habit**  
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — **not a habit**  
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — **not a habit**  
52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — **not a habit**  
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — **not a habit**  
54. Ich habe heute viele neue Freunde kennengelernt — **not a habit**  
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — **not a habit**  
56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — **not a habit**  
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — **not a habit**  
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — **not a habit**  
59. Ich habe mir heute eine neue Pflanze gekauft. — **not a habit**  
60. Ich jogge — **habit**  
61. Letzte Woche war ich joggen. — **not a habit**  
62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — **not a habit**  
63. Ich liebe Pommes Frites — **not a habit**  
64. Ich habe gestern Pommes gegessen — **not a habit**  
65. Ich mag Eis, aber nicht jedes Mal. — **not a habit**  
66. Gestern habe ich zum ersten Mal Yoga gemacht. — **not a habit**"""

    llm_dict[
        "o4 mini (High Effort)"
    ].output = """1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — habit  
2. Immer wenn ich müde bin, mache ich Atemübungen. — habit  
3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — habit  
4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — habit  
5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — habit  
6. Nach dem Aufstehen mache ich Kraftsport — habit  
7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — habit  
8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — habit  
9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — habit  
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — habit  
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — habit  
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — habit  
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — habit  
14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — habit  
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — habit  
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — habit  
17. Nach dem Joggen trinke ich einen Proteinshake. — habit  
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — habit  
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — habit  
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — habit  
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — habit  
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — habit  
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — habit  
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — habit  
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — habit  
26. nach dem Abendbrot wasche ich ab — habit  
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — habit  
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe — habit  
29. Ich nehme VItamin D tabletten ein — habit  
30. Samstags putze ich das Bad. — habit  
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — habit  
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — habit  
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — habit  
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — not a habit  
35. Ich war gestern im Kino — not a habit  
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — not a habit  
37. Ich plane, morgen ins Schwimmbad zu gehen. — not a habit  
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — not a habit  
39. Ich habe heute zum ersten Mal einen Podcast gehört. — not a habit  
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — not a habit  
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — not a habit  
42. Ich habe letzte Woche meine Wohnung umdekoriert. — not a habit  
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — not a habit  
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — not a habit  
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — not a habit  
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — not a habit  
47. Ich bin an die Landschaft in den Bergen gewöhnt — not a habit  
48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — not a habit  
49. Heute Morgen fühlte ich mich plötzlich sehr müde — not a habit  
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — not a habit  
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — not a habit  
52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — not a habit  
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — not a habit  
54. Ich habe heute viele neue Freunde kennengelernt — not a habit  
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — not a habit  
56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — not a habit  
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — not a habit  
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — not a habit  
59. Ich habe mir heute eine neue Pflanze gekauft. — not a habit  
60. Ich jogge — habit  
61. Letzte Woche war ich joggen. — not a habit  
62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — not a habit  
63. Ich liebe Pommes Frites — not a habit  
64. Ich habe gestern Pommes gegessen — not a habit  
65. Ich mag Eis, aber nicht jedes Mal. — not a habit  
66. Gestern habe ich zum ersten Mal Yoga gemacht. — not a habit"""


    llm_dict[
        "o3 mini (High Effort)"
    ].output = """Below is the evaluation of each sentence:

#### Evaluation

1. **'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.'** — habit  
2. **'Immer wenn ich müde bin, mache ich Atemübungen. '** — habit  
3. **'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. '** — habit  
4. **'Abends nach dem Abendbrot trinke ich ein Glas Wein. '** — habit  
5. **'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. '** — habit  
6. **'Nach dem Aufstehen mache ich Kraftsport'** — habit  
7. **'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. '** — habit  
8. **'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. '** — habit  
9. **'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. '** — habit  
10. **'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. '** — habit  
11. **'Morgens nach dem Aufstehen wasche ich mein Gesicht.'** — habit  
12. **'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.'** — habit  
13. **'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.'** — habit  
14. **'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.'** — habit  
15. **'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.'** — habit  
16. **'Morgens nach der Tierfütterung trinke ich einen Kaffee.'** — habit  
17. **'Nach dem Joggen trinke ich einen Proteinshake.'** — habit  
18. **'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier'** — habit  
19. **'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.'** — habit  
20. **'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel'** — habit  
21. **'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.'** — habit  
22. **'Nach dem Aufstehen mache ich mir ein Zitronenwasser.'** — habit  
23. **'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.'** — habit  
24. **'wenn ich ins DM gehe, kaufe ich mir was Süßes.'** — habit  
25. **'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout'** — habit  
26. **'nach dem Abendbrot wasche ich ab'** — habit  
27. **'Nach dem Aufstehen mache ich ein paar Sprachübungen'** — habit  
28. **'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe'** — habit  
29. **'Ich nehme VItamin D tabletten ein'** — habit  
30. **'Samstags putze ich das Bad.'** — habit  
31. **'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.'** — habit  
32. **'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade'** — habit  
33. **'Nach dem Sport am Abend gehe ich oft erst spät ins Bett '** — habit  
34. **'Ich habe mir heute eine neue Serie auf Netflix angesehen.'** — not a habit  
35. **'Ich war gestern im Kino'** — not a habit  
36. **'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren'** — not a habit  
37. **'Ich plane, morgen ins Schwimmbad zu gehen.'** — not a habit  
38. **'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.'** — not a habit  
39. **'Ich habe heute zum ersten Mal einen Podcast gehört.'** — not a habit  
40. **'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.'** — not a habit  
41. **'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.'** — not a habit  
42. **'Ich habe letzte Woche meine Wohnung umdekoriert.'** — not a habit  
43. **'Letzte Woche war ich auf der Hochzeit meiner besten Freundin'** — not a habit  
44. **'Letzte Woche war ich auf der Beerdigung eines guten Freundes.'** — not a habit  
45. **'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen'** — not a habit  
46. **'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut'** — not a habit  
47. **'Ich bin an die Landschaft in den Bergen gewöhnt'** — not a habit  
48. **'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.'** — not a habit  
49. **'Heute Morgen fühlte ich mich plötzlich sehr müde'** — not a habit  
50. **'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt'** — not a habit  
51. **'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen'** — not a habit  
52. **'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.'** — not a habit  
53. **'Heute habe ich versucht zu lernen, wie man einen Kuchen backt'** — not a habit  
54. **'Ich habe heute viele neue Freunde kennengelernt'** — not a habit  
55. **'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.'** — not a habit  
56. **'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein'** — not a habit  
57. **'Vielleicht plane ich, in Zukunft zum Militär zu gehen.'** — not a habit  
58. **'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.'** — not a habit  
59. **'Ich habe mir heute eine neue Pflanze gekauft.'** — not a habit  
60. **'Ich jogge'** — habit  
61. **'Letzte Woche war ich joggen.'** — not a habit  
62. **'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst'** — not a habit  
63. **'Ich liebe Pommes Frites'** — not a habit  
64. **'Ich habe gestern Pommes gegessen'** — not a habit  
65. **'Ich mag Eis, aber nicht jedes Mal.'** — not a habit  
66. **'Gestern habe ich zum ersten Mal Yoga gemacht.'** — not a habit

I hope this detailed evaluation helps clarify which sentences describe recurring or routine behaviors and which do not!"""

    llm_dict[
        "GPT-4o mini"
    ].output = """Here’s the evaluation of the sentences regarding whether they describe a habit or not:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — **habit**
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — **habit**
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — **not a habit**
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — **habit**
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — **habit**
6. 'Nach dem Aufstehen mache ich Kraftsport' — **habit**
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — **habit**
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — **not a habit**
9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — **not a habit**
10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — **not a habit**
11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — **habit**
12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — **habit**
13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — **habit**
14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — **habit**
15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — **habit**
16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — **habit**
17. 'Nach dem Joggen trinke ich einen Proteinshake.' — **habit**
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — **not a habit**
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — **habit**
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — **habit**
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — **not a habit**
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — **habit**
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — **not a habit**
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — **habit**
25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — **habit**
26. 'nach dem Abendbrot wasche ich ab' — **habit**
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — **habit**
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — **habit**
29. 'Ich nehme VItamin D tabletten ein' — **habit**
30. 'Samstags putze ich das Bad.' — **habit**
31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — **habit**
32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — **not a habit**
33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ' — **not a habit**
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

This list categorizes each sentence based on whether it describes a recurring behavior (habit) or not (not a habit)."""


    llm_dict[
        "GPT-4o"
    ].output = """Here is the evaluation of the sentences to determine whether each describes a habit or not. A habit is classified as a recurring or routine behavior, while sentences describing one-time actions, intentions, or unrelated statements are classified as "not a habit."

---

#### Evaluated Sentences:

1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kaffee.' — **habit**  
2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — **habit**  
3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — **habit**  
4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — **habit**  
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappuccino.' — **habit**  
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
18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier.' — **habit**  
19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — **habit**  
20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel.' — **habit**  
21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — **habit**  
22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — **habit**  
23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — **habit**  
24. 'Wenn ich ins DM gehe, kaufe ich mir was Süßes.' — **habit**  
25. 'Nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout.' — **habit**  
26. 'Nach dem Abendbrot wasche ich ab.' — **habit**  
27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen.' — **habit**  
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der Wohnung gehe.' — **habit**  
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

---

#### Summary:
- **Habits**: 33 sentences  
- **Not habits**: 33 sentences"""

    llm_dict[
        "Claude Sonnet 4 (Extended)"
    ].output = """I'll analyze each sentence to determine whether it describes a habit (recurring/routine behavior) or not. Here's my evaluation:

1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — **habit**

2. Immer wenn ich müde bin, mache ich Atemübungen. — **habit**

3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — **habit**

4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — **habit**

5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — **habit**

6. Nach dem Aufstehen mache ich Kraftsport — **habit**

7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — **habit**

8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — **habit**

9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — **habit**

10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — **habit**

11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — **habit**

12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — **habit**

13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — **habit**

14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — **habit**

15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — **habit**

16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — **habit**

17. Nach dem Joggen trinke ich einen Proteinshake. — **habit**

18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — **habit**

19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — **habit**

20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — **habit**

21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — **habit**

22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — **habit**

23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — **habit**

24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — **habit**

25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — **habit**

26. nach dem Abendbrot wasche ich ab — **habit**

27. Nach dem Aufstehen mache ich ein paar Sprachübungen — **habit**

28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe — **habit**

29. Ich nehme VItamin D tabletten ein — **habit**

30. Samstags putze ich das Bad. — **habit**

31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — **habit**

32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — **habit**

33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — **habit**

34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — **not a habit**

35. Ich war gestern im Kino — **not a habit**

36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — **not a habit**

37. Ich plane, morgen ins Schwimmbad zu gehen. — **not a habit**

38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — **not a habit**

39. Ich habe heute zum ersten Mal einen Podcast gehört. — **not a habit**

40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — **not a habit**

41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — **not a habit**

42. Ich habe letzte Woche meine Wohnung umdekoriert. — **not a habit**

43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — **not a habit**

44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — **not a habit**

45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — **not a habit**

46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — **not a habit**

47. Ich bin an die Landschaft in den Bergen gewöhnt — **not a habit**

48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — **not a habit**

49. Heute Morgen fühlte ich mich plötzlich sehr müde — **not a habit**

50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — **not a habit**

51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — **not a habit**

52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — **not a habit**

53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — **not a habit**

54. Ich habe heute viele neue Freunde kennengelernt — **not a habit**

55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — **not a habit**

56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — **not a habit**

57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — **not a habit**

58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — **not a habit**

59. Ich habe mir heute eine neue Pflanze gekauft. — **not a habit**

60. Ich jogge — **habit**

61. Letzte Woche war ich joggen. — **not a habit**

62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — **not a habit**

63. Ich liebe Pommes Frites — **not a habit**

64. Ich habe gestern Pommes gegessen — **not a habit**

65. Ich mag Eis, aber nicht jedes Mal. — **not a habit**

66. Gestern habe ich zum ersten Mal Yoga gemacht. — **not a habit**"""

    llm_dict[
        "Claude Sonnet 4"
    ].output = """I'll analyze each sentence to determine whether it describes a habit (recurring/routine behavior) or not. Here's my evaluation:

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
        "Claude Sonnet 3.7 (Extended)"
    ].output = """# Habit Classification Results

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
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""


    llm_dict[
        "Claude Sonnet 3.7"
    ].output = """I'll evaluate each sentence to determine whether it describes a habit or not. I'll provide a numbered list with my classification for each sentence.

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
56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — habit
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
        "Claude Sonnet 3.5"
    ].output = """I'll help evaluate each sentence to determine if it describes a habit. I'll analyze them based on indicators of recurring behavior, routine actions, or regular patterns.

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
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""


    llm_dict[
        "Claude Opus 4 (Extended)"
    ].output = """I'll analyze each sentence to determine if it describes a recurring or routine behavior (habit) or not:

1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — habit
2. Immer wenn ich müde bin, mache ich Atemübungen. — habit
3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — habit
4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — habit
5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — habit
6. Nach dem Aufstehen mache ich Kraftsport — habit
7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — habit
8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — habit
9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — habit
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — habit
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — habit
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — habit
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — habit
14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — habit
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — habit
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — habit
17. Nach dem Joggen trinke ich einen Proteinshake. — habit
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — habit
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — habit
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — habit
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — habit
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — habit
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — habit
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — habit
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — habit
26. nach dem Abendbrot wasche ich ab — habit
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — habit
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe — habit
29. Ich nehme VItamin D tabletten ein — habit
30. Samstags putze ich das Bad. — habit
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — habit
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — habit
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — habit
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — not a habit
35. Ich war gestern im Kino — not a habit
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — not a habit
37. Ich plane, morgen ins Schwimmbad zu gehen. — not a habit
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — not a habit
39. Ich habe heute zum ersten Mal einen Podcast gehört. — not a habit
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — not a habit
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — not a habit
42. Ich habe letzte Woche meine Wohnung umdekoriert. — not a habit
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — not a habit
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — not a habit
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — not a habit
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — not a habit
47. Ich bin an die Landschaft in den Bergen gewöhnt — not a habit
48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — not a habit
49. Heute Morgen fühlte ich mich plötzlich sehr müde — not a habit
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — not a habit
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — not a habit
52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — not a habit
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — not a habit
54. Ich habe heute viele neue Freunde kennengelernt — not a habit
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — not a habit
56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — not a habit
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — not a habit
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — not a habit
59. Ich habe mir heute eine neue Pflanze gekauft. — not a habit
60. Ich jogge — habit
61. Letzte Woche war ich joggen. — not a habit
62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — not a habit
63. Ich liebe Pommes Frites — not a habit
64. Ich habe gestern Pommes gegessen — not a habit
65. Ich mag Eis, aber nicht jedes Mal. — not a habit
66. Gestern habe ich zum ersten Mal Yoga gemacht. — not a habit"""


    llm_dict[
        "Claude Opus 4"
    ].output = """I'll evaluate each sentence to determine whether it describes a habit or not. Here's my analysis:

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
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""


    llm_dict[
        "Claude Opus 3"
    ].output = """Here is the list of sentences with habit classifications:

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
47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — habit
48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit
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
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit"""

    llm_dict[
        "Gemini 2.5 pro"
    ].output = """Of course. As a habit recognition expert, I will evaluate each sentence to determine if it describes a recurring or routine behavior. Here is the classified list:

1.  Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — habit
2.  Immer wenn ich müde bin, mache ich Atemübungen. — habit
3.  Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — habit
4.  Abends nach dem Abendbrot trinke ich ein Glas Wein. — habit
5.  Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — habit
6.  Nach dem Aufstehen mache ich Kraftsport — habit
7.  Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — habit
8.  Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — habit
9.  Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — habit
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — habit
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — habit
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — habit
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — habit
14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — habit
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — habit
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — habit
17. Nach dem Joggen trinke ich einen Proteinshake. — habit
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — habit
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — habit
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — habit
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — habit
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — habit
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — habit
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — habit
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — habit
26. nach dem Abendbrot wasche ich ab — habit
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — habit
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe — habit
29. Ich nehme VItamin D tabletten ein — habit
30. Samstags putze ich das Bad. — habit
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — habit
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — habit
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — habit
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — not a habit
35. Ich war gestern im Kino — not a habit
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — not a habit
37. Ich plane, morgen ins Schwimmbad zu gehen. — not a habit
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — not a habit
39. Ich habe heute zum ersten Mal einen Podcast gehört. — not a habit
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — not a habit
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — not a habit
42. Ich habe letzte Woche meine Wohnung umdekoriert. — not a habit
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — not a habit
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — not a habit
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — not a habit
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — not a habit
47. Ich bin an die Landschaft in den Bergen gewöhnt — not a habit
48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — not a habit
49. Heute Morgen fühlte ich mich plötzlich sehr müde — not a habit
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — not a habit
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — not a habit
52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — not a habit
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — not a habit
54. Ich habe heute viele neue Freunde kennengelernt — not a habit
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — not a habit
56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — not a habit
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — not a habit
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — not a habit
59. Ich habe mir heute eine neue Pflanze gekauft. — not a habit
60. Ich jogge — habit
61. Letzte Woche war ich joggen. — not a habit
62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — not a habit
63. Ich liebe Pommes Frites — not a habit
64. Ich habe gestern Pommes gegessen — not a habit
65. Ich mag Eis, aber nicht jedes Mal. — not a habit
66. Gestern habe ich zum ersten Mal Yoga gemacht. — not a habit"""

    llm_dict[
        "Gemini 2.0 Flash"
    ].output = """Here's the classification of each sentence:

1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — habit
2. Immer wenn ich müde bin, mache ich Atemübungen. — habit
3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — habit
4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — habit
5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — habit
6. Nach dem Aufstehen mache ich Kraftsport — habit
7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — habit
8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — habit
9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — habit
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — habit
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — habit
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — habit
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — habit
14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — habit
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — habit
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — habit
17. Nach dem Joggen trinke ich einen Proteinshake. — habit
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — habit
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — habit
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — habit
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — habit
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — habit
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — habit
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — habit
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — habit
26. nach dem Abendbrot wasche ich ab — habit
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — habit
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe — habit
29. Ich nehme VItamin D tabletten ein — habit
30. Samstags putze ich das Bad. — habit
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — habit
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — habit
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — habit
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — not a habit
35. Ich war gestern im Kino — not a habit
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — not a habit
37. Ich plane, morgen ins Schwimmbad zu gehen. — not a habit
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — not a habit
39. Ich habe heute zum ersten Mal einen Podcast gehört. — not a habit
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — not a habit
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — not a habit
42. Ich habe letzte Woche meine Wohnung umdekoriert. — not a habit
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — not a habit
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — not a habit
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — not a habit
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — not a habit
47. Ich bin an die Landschaft in den Bergen gewöhnt — not a habit
48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — not a habit
49. Heute Morgen fühlte ich mich plötzlich sehr müde — not a habit
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — not a habit
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — not a habit
52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — not a habit
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — not a habit
54. Ich habe heute viele neue Freunde kennengelernt — not a habit
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — not a habit
56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — not a habit
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — not a habit
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — not a habit
59. Ich habe mir heute eine neue Pflanze gekauft. — not a habit
60. Ich jogge — habit
61. Letzte Woche war ich joggen. — not a habit
62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — not a habit
63. Ich liebe Pommes Frites — not a habit
64. Ich habe gestern Pommes gegessen — not a habit
65. Ich mag Eis, aber nicht jedes Mal. — not a habit
66. Gestern habe ich zum ersten Mal Yoga gemacht. — not a habit
"""
    llm_dict[
        "Llama 4 Maverick"
    ].output = """Here is the numbered list with the sentence and the corresponding label:

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
5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ' — not a habit
6. 'Nach dem Aufstehen mache ich Kraftsport' — habit
7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ' — habit
8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ' — not a habit
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
24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — not a habit
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

Note that some sentences could be argued to be habits or not habits depending on the context, but I've made my classification based on the information provided.
"""
    llm_dict[
        "Mistral Large 2"
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

Note that some sentences could be argued to be habits or not habits depending on the context, but I've made my classification based on the information provided.
"""
    llm_dict[
        "Deepseek-V3"
    ].output = """Here is the numbered list with classifications for each sentence:

Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — habit

Immer wenn ich müde bin, mache ich Atemübungen. — habit

Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — not a habit

Abends nach dem Abendbrot trinke ich ein Glas Wein. — habit

Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — habit

Nach dem Aufstehen mache ich Kraftsport — habit

Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — habit

Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — habit

Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — habit

Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — habit

Morgens nach dem Aufstehen wasche ich mein Gesicht. — habit

Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — habit

Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — habit

Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — habit

Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — habit

Morgens nach der Tierfütterung trinke ich einen Kaffee. — habit

Nach dem Joggen trinke ich einen Proteinshake. — habit

Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — not a habit

Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — habit

Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — habit

Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — habit

Nach dem Aufstehen mache ich mir ein Zitronenwasser. — habit

Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — habit

wenn ich ins DM gehe, kaufe ich mir was Süßes. — habit

nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — habit

nach dem Abendbrot wasche ich ab — habit

Nach dem Aufstehen mache ich ein paar Sprachübungen — habit

Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe — habit

Ich nehme VItamin D tabletten ein — habit

Samstags putze ich das Bad. — habit

Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — habit

Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — habit

Nach dem Sport am Abend gehe ich oft erst spät ins Bett — habit

Ich habe mir heute eine neue Serie auf Netflix angesehen. — not a habit

Ich war gestern im Kino — not a habit

Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — not a habit

Ich plane, morgen ins Schwimmbad zu gehen. — not a habit

Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — not a habit

Ich habe heute zum ersten Mal einen Podcast gehört. — not a habit

Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — not a habit

Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — not a habit

Ich habe letzte Woche meine Wohnung umdekoriert. — not a habit

Letzte Woche war ich auf der Hochzeit meiner besten Freundin — not a habit

Letzte Woche war ich auf der Beerdigung eines guten Freundes. — not a habit

Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — not a habit

Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — not a habit

Ich bin an die Landschaft in den Bergen gewöhnt — not a habit

Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — not a habit

Heute Morgen fühlte ich mich plötzlich sehr müde — not a habit

Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — not a habit

Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — not a habit

Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — not a habit

Heute habe ich versucht zu lernen, wie man einen Kuchen backt — not a habit

Ich habe heute viele neue Freunde kennengelernt — not a habit

Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — not a habit

Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — not a habit

Vielleicht plane ich, in Zukunft zum Militär zu gehen. — not a habit

Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — not a habit

Ich habe mir heute eine neue Pflanze gekauft. — not a habit

Ich jogge — habit

Letzte Woche war ich joggen. — not a habit

Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — not a habit

Ich liebe Pommes Frites — not a habit

Ich habe gestern Pommes gegessen — not a habit

Ich mag Eis, aber nicht jedes Mal. — not a habit

Gestern habe ich zum ersten Mal Yoga gemacht. — not a habit
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
64. 'Ich habe gestern Pommes gegessen' — not a habitDeepSeek-Coder-V2-Lite-Instruct
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""

    llm_dict[
        "Llama-3.1-8B"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit\n2. 'Immer wenn ich müde bin, mache ich Atemübungen.'— habit\n3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.'— habit\n4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.'— habit\n5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.'— habit\n6. 'Nach dem Aufstehen mache ich Kraftsport' — habit\n7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.'— habit\n8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.'— habit\n9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.'— habit\n10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.'— habit\n11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit\n12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit\n13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit\n14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit\n15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit\n16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit\n17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit\n18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit\n19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit\n20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit\n21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit\n22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit\n23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — habit\n24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit\n25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit\n26. 'nach dem Abendbrot wasche ich ab' — habit\n27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit\n28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — habit\n29. 'Ich nehme VItamin D tabletten ein' — habit\n30. 'Samstags putze ich das Bad.' — habit\n31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit\n32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit\n33. 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett'— habit\n34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit\n35. 'Ich war gestern im Kino' — not a habit\n36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit\n37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit\n38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit\n39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit\n40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit\n41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit\n42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit\n43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit\n44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit\n45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — habit\n46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit\n47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit\n48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit\n49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit\n50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit\n51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit\n52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit\n53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit\n54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit\n55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit\n56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit\n57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit\n58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit\n59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit\n60. 'Ich jogge' — habit\n61. 'Letzte Woche war ich joggen.' — habit\n62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit\n63. 'Ich liebe Pommes Frites' — habit\n64. 'Ich habe gestern Pommes gegessen' — habit\n65. 'Ich mag Eis, aber nicht jedes Mal.' — habit\n66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — habit"""
    llm_dict[
        "DeepSeek-Coder-V2-Lite-Instruct"
    ].output = """ 1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — not a habit  
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
28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe' — not a habit  
29. 'Ich nehme Vitamin D tabletten ein' — habit  
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

Here's the classification for each sentence based on whether it describes a recurring/routine behavior (habit) or not:

1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — **habit**  
2. Immer wenn ich müde bin, mache ich Atemübungen. — **habit**  
3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — **habit**  
4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — **habit**  
5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — **habit**  
6. Nach dem Aufstehen mache ich Kraftsport — **habit**  
7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — **habit**  
8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — **habit**  
9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — **habit**  
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — **habit**  
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — **habit**  
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — **habit**  
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — **habit**  
14. Morgens nach dem Gesicht-Eincremen füttere ich die Katze. — **habit**  
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — **habit**  
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — **habit**  
17. Nach dem Joggen trinke ich einen Proteinshake. — **habit**  
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — **not a habit** (preference, not routine)  
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — **habit**  
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — **habit**  
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — **habit**  
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — **habit**  
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — **habit**  
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — **habit**  
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — **habit**  
26. nach dem Abendbrot wasche ich ab — **habit**  
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — **habit**  
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe — **habit**  
29. Ich nehme VItamin D tabletten ein — **habit** (if done regularly)  
30. Samstags putze ich das Bad. — **habit**  
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — **habit**  
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — **habit**  
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — **habit**  
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — **not a habit** (one-time event)  
35. Ich war gestern im Kino — **not a habit**  
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — **not a habit** (future intent)  
37. Ich plane, morgen ins Schwimmbad zu gehen. — **not a habit**  
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — **not a habit**  
39. Ich habe heute zum ersten Mal einen Podcast gehört. — **not a habit**  
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — **not a habit**  
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — **not a habit**  
42. Ich habe letzte Woche meine Wohnung umdekoriert. — **not a habit**  
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — **not a habit**  
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — **not a habit**  
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — **not a habit** (future plan)  
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — **not a habit** (temporary state)  
47. Ich bin an die Landschaft in den Bergen gewöhnt — **not a habit** (state of being)  
48. Letzten Mittwoch... in ein Café gegangen... — **not a habit** (one-time discovery)  
49. Heute Morgen fühlte ich mich plötzlich sehr müde — **not a habit** (temporary state)  
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — **not a habit** (preference)  
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — **not a habit** (conditional reaction)  
52. Ich habe mir den Rap einmal angehört... — **not a habit**  
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — **not a habit**  
54. Ich habe heute viele neue Freunde kennengelernt — **not a habit**  
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — **not a habit**  
56. Wenn ich versuche zu bezahlen, friert die Webseite... — **not a habit** (technical issue, not behavior)  
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — **not a habit**  
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — **not a habit**  
59. Ich habe mir heute eine neue Pflanze gekauft. — **not a habit**  
60. Ich jogge — **habit** (present tense implies regularity)  
61. Letzte Woche war ich joggen. — **not a habit** (past action)  
62. Ich habe einmal Tischtennis gespielt... — **not a habit**  
63. Ich liebe Pommes Frites — **not a habit** (preference)  
64. Ich habe gestern Pommes gegessen — **not a habit**  
65. Ich mag Eis, aber nicht jedes Mal. — **not a habit** (preference with exceptions)  
66. Gestern habe ich zum ersten Mal Yoga gemacht. — **not a habit**
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
60. 'Ich jogge' — habit
61. 'Letzte Woche war ich joggen.' — not a habit
62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit
63. 'Ich liebe Pommes Frites' — not a habit
64. 'Ich habe gestern Pommes gegessen' — not a habit
65. 'Ich mag Eis, aber nicht jedes Mal.' — not a habit
66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit
"""

    llm_dict[
        "Mistral-7B-Instruct-v0.3"
    ].output = """1. 'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.' — habit\n2. 'Immer wenn ich müde bin, mache ich Atemübungen.' — habit\n3. 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.' — not a habit (This is a response to a specific emotion, not a recurring behavior)\n4. 'Abends nach dem Abendbrot trinke ich ein Glas Wein.' — habit\n5. 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.' — habit\n6. 'Nach dem Aufstehen mache ich Kraftsport' — habit\n7. 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.' — habit\n8. 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.' — not a habit (This is a response to a specific event, not a recurring behavior)\n9. 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.' — habit\n10. 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.' — habit (although not daily, it is a recurring behavior)\n11. 'Morgens nach dem Aufstehen wasche ich mein Gesicht.' — habit\n12. 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.' — habit\n13. 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.' — habit\n14. 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.' — habit\n15. 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.' — habit\n16. 'Morgens nach der Tierfütterung trinke ich einen Kaffee.' — habit\n17. 'Nach dem Joggen trinke ich einen Proteinshake.' — habit\n18. 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier' — habit (although not always, it is a recurring behavior when the desire arises)\n19. 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.' — habit\n20. 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel' — habit\n21. 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.' — habit\n22. 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.' — habit\n23. 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.' — not a habit (This is a response to a specific situation, not a recurring behavior)\n24. 'wenn ich ins DM gehe, kaufe ich mir was Süßes.' — habit\n25. 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout' — habit\n26. 'nach dem Abendbrot wasche ich ab' — habit\n27. 'Nach dem Aufstehen mache ich ein paar Sprachübungen' — habit\n28. 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe' — habit\n29. 'Ich nehme VItamin D tabletten ein' — habit\n30. 'Samstags putze ich das Bad.' — habit\n31. 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.' — habit\n32. 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade' — habit\n33. 'Nach dem Sport am Abend gehe ich oft spät ins Bett'— habit\n34. 'Ich habe mir heute eine neue Serie auf Netflix angesehen.' — not a habit (This is a one-time event, not a recurring behavior)\n35. 'Ich war gestern im Kino' — not a habit (This is a one-time event, not a recurring behavior)\n36. 'Ich habe vor, einen neuen Getränkegeschmack auszuprobieren' — not a habit (This is a future intention, not a recurring behavior)\n37. 'Ich plane, morgen ins Schwimmbad zu gehen.' — not a habit (This is a future intention, not a recurring behavior)\n38. 'Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht.' — not a habit (This is a one-time event, not a recurring behavior)\n39. 'Ich habe heute zum ersten Mal einen Podcast gehört.' — not a habit (This is a one-time event, not a recurring behavior)\n40. 'Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht.' — not a habit (This is a one-time event, not a recurring behavior)\n41. 'Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht.' — not a habit (This is a one-time event, not a recurring behavior)\n42. 'Ich habe letzte Woche meine Wohnung umdekoriert.' — not a habit (This is a one-time event, not a recurring behavior)\n43. 'Letzte Woche war ich auf der Hochzeit meiner besten Freundin' — not a habit (This is a one-time event, not a recurring behavior)\n44. 'Letzte Woche war ich auf der Beerdigung eines guten Freundes.' — not a habit (This is a one-time event, not a recurring behavior)\n45. 'Ich habe vor, nächsten Mittwoch zum Arzt zu gehen' — not a habit (This is a future intention, not a recurring behavior)\n46. 'Mir geht es jetzt sehr schlecht, weil mein Magen weh tut' — not a habit (This is a current state, not a recurring behavior)\n47. 'Ich bin an die Landschaft in den Bergen gewöhnt' — not a habit (This is a preference, not a recurring behavior)\n48. 'Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat.' — not a habit (This is a one-time event, not a recurring behavior)\n49. 'Heute Morgen fühlte ich mich plötzlich sehr müde' — not a habit (This is a current state, not a recurring behavior)\n50. 'Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt' — not a habit (This is a preference, not a recurring behavior)\n51. 'Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen' — not a habit (This is a response to a specific situation, not a recurring behavior)\n52. 'Ich habe mir den Rap einmal angehört und er klang ziemlich gut.' — not a habit (This is a one-time event, not a recurring behavior)\n53. 'Heute habe ich versucht zu lernen, wie man einen Kuchen backt' — not a habit (This is a one-time event, not a recurring behavior)\n54. 'Ich habe heute viele neue Freunde kennengelernt' — not a habit (This is a one-time event, not a recurring behavior)\n55. 'Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt.' — not a habit (This is a one-time event, not a recurring behavior)\n56. 'Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein' — not a habit (This is a response to a specific situation, not a recurring behavior)\n57. 'Vielleicht plane ich, in Zukunft zum Militär zu gehen.' — not a habit (This is a future intention, not a recurring behavior)\n58. 'Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen.' — not a habit (This is a one-time event, not a recurring behavior)\n59. 'Ich habe mir heute eine neue Pflanze gekauft.' — not a habit (This is a one-time event, not a recurring behavior)\n60. 'Ich jogge' — habit\n61. 'Letzte Woche war ich joggen.' — not a habit (This is a one-time event, not a recurring behavior)\n62. 'Ich habe einmal Tischtennis gespielt und es nie wieder angefasst' — not a habit (This is a one-time event, not a recurring behavior)\n63. 'Ich liebe Pommes Frites' — preference, not a habit\n64. 'Ich habe gestern Pommes gegessen' — not a habit (This is a one-time event, not a recurring behavior)\n65. 'Ich mag Eis, aber nicht jedes Mal.' — preference, not a habit\n66. 'Gestern habe ich zum ersten Mal Yoga gemacht.' — not a habit (This is a one-time event, not a recurring behavior)"""

    llm_dict[
        "Qwen3-8B"
    ].output = """1. Morgens nach dem Aufstehen trinke ich direkt einen Kafffe. — habit  
2. Immer wenn ich müde bin, mache ich Atemübungen. — habit  
3. Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. — not a habit  
4. Abends nach dem Abendbrot trinke ich ein Glas Wein. — habit  
5. Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. — not a habit  
6. Nach dem Aufstehen mache ich Kraftsport — habit  
7. Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. — habit  
8. Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. — habit  
9. Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. — not a habit  
10. Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. — habit  
11. Morgens nach dem Aufstehen wasche ich mein Gesicht. — habit  
12. Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne. — habit  
13. Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein. — habit  
14. Morgens nach dem Gesicht-Ecremen füttere ich die Katze. — habit  
15. Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange. — habit  
16. Morgens nach der Tierfütterung trinke ich einen Kaffee. — habit  
17. Nach dem Joggen trinke ich einen Proteinshake. — habit  
18. Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier — not a habit  
19. Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr. — habit  
20. Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel — habit  
21. Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen. — habit  
22. Nach dem Aufstehen mache ich mir ein Zitronenwasser. — habit  
23. Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media. — habit  
24. wenn ich ins DM gehe, kaufe ich mir was Süßes. — not a habit  
25. nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout — habit  
26. nach dem Abendbrot wasche ich ab — not a habit  
27. Nach dem Aufstehen mache ich ein paar Sprachübungen — habit  
28. Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der Wohnung gehe — habit  
29. Ich nehme VItamin D tabletten ein — habit  
30. Samstags putze ich das Bad. — habit  
31. Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum. — habit  
32. Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade — habit  
33. Nach dem Sport am Abend gehe ich oft erst spät ins Bett — habit  
34. Ich habe mir heute eine neue Serie auf Netflix angesehen. — not a habit  
35. Ich war gestern im Kino — not a habit  
36. Ich habe vor, einen neuen Getränkegeschmack auszuprobieren — not a habit  
37. Ich plane, morgen ins Schwimmbad zu gehen. — not a habit  
38. Ich habe am Wochenende meine Freunde in einer anderen Stadt besucht. — not a habit  
39. Ich habe heute zum ersten Mal einen Podcast gehört. — not a habit  
40. Ich habe heute zum ersten Mal ein Selfie mit meiner neuen Kamera gemacht. — not a habit  
41. Heute habe ich einen langen Spaziergang durch eine fremde Gegend gemacht. — not a habit  
42. Ich habe letzte Woche meine Wohnung umdekoriert. — not a habit  
43. Letzte Woche war ich auf der Hochzeit meiner besten Freundin — not a habit  
44. Letzte Woche war ich auf der Beerdigung eines guten Freundes. — not a habit  
45. Ich habe vor, nächsten Mittwoch zum Arzt zu gehen — not a habit  
46. Mir geht es jetzt sehr schlecht, weil mein Magen weh tut — not a habit  
47. Ich bin an die Landschaft in den Bergen gewöhnt — not a habit  
48. Letzten Mittwoch hat es plötzlich geregnet, also bin ich in ein Café gegangen, das ich vorher nicht kannte, um Schutz vor dem Regen zu suchen, und ich habe festgestellt, dass es mir wirklich gut gefallen hat. — not a habit  
49. Heute Morgen fühlte ich mich plötzlich sehr müde — not a habit  
50. Haferbrei schmeckt besser, wenn man Blaubeeren dazu gibt — not a habit  
51. Es regnet heute, deshalb möchte ich nicht ins Fitnessstudio gehen — not a habit  
52. Ich habe mir den Rap einmal angehört und er klang ziemlich gut. — not a habit  
53. Heute habe ich versucht zu lernen, wie man einen Kuchen backt — not a habit  
54. Ich habe heute viele neue Freunde kennengelernt — not a habit  
55. Ich habe heute viele neue Möbel zur Einrichtung meines neuen Hauses bestellt. — not a habit  
56. Wenn ich versuche zu bezahlen, friert die Webseite aus unbekannten Gründen immer wieder ein — not a habit  
57. Vielleicht plane ich, in Zukunft zum Militär zu gehen. — not a habit  
58. Ich habe gestern einen Film auf Englisch ohne Untertitel gesehen. — not a habit  
59. Ich habe mir heute eine neue Pflanze gekauft. — not a habit  
60. Ich jogge — habit  
61. Letzte Woche war ich joggen. — not a habit  
62. Ich habe einmal Tischtennis gespielt und es nie wieder angefasst — not a habit  
63. Ich liebe Pommes Frites — not a habit  
64. Ich habe gestern Pommes gegessen — not a habit  
65. Ich mag Eis, aber nicht jedes Mal. — not a habit  
66. Gestern habe ich zum ersten Mal Yoga gemacht. — not a habit"""
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



evaluate_and_report(llm_dict, true_labels, metric_names=['accuracy',"precision", "recall","f1","mcc","kappa"])
df=summarize_llm_full_info(llm_dict,20)
df.to_excel("llm_all_info_with_cost_performance_zeroshot.xlsx", index=False)



