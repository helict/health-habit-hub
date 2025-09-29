from narwhals import String
from LLMInfo import LLMInfo, load_llms_from_excel
import pandas as pd
import os


contextual_components = [
    "TIME",
    "PHYSICAL SETTING",
    "PRIOR BEHAVIOR",
    "OTHER PEOPLE",
    "INTERNAL STATE",
    "BEHAVIOR"
]

def extract_contextual_columns_with_multiple_labels(file_path):
    """
    Extracts the context field from the table into the form {component: [ [label1, label2], ... ] } .
    Multiple labels separated by '//' are supported, automatically converted to lowercase, and trailing punctuation (., , .) is removed.
    """
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Only .csv or .xlsx files are supported")

    contextual_components = [
        "TIME", "PHYSICAL SETTING", "PRIOR BEHAVIOR",
        "OTHER PEOPLE", "INTERNAL STATE", "BEHAVIOR"
    ]

    context_dict = {}

    for component in contextual_components:
        column_values = df[component].fillna("").astype(str)
        processed_values = []

        for val in column_values:
            if "//" in val:
                parts = [
                    v.strip().rstrip(".,，。").lower()
                    for v in val.split("//")
                    if v.strip()
                ]
                processed_values.append(parts)
            elif val.strip():
                cleaned = val.strip().rstrip(".,，。").lower()
                processed_values.append([cleaned])
            else:
                processed_values.append([])

        context_dict[component] = processed_values

    return context_dict

if __name__ == "__main__":
    true_labels = extract_contextual_columns_with_multiple_labels("Habit_contexts_DB.xlsx")
    llm_dict = load_llms_from_excel("LLMs_info.xlsx")
    LLMInfo.set_input_prompt(
        """You are a behavioral-scientist LLM specializing in habit context recognition.

Your task is to analyze each sentence in the provided list. For each of the six contextual components, you must:

1. Extract the exact text snippet from the sentence that represents the component.
2. Assign a probabilistic confidence value (0.00-1.00, two decimals) for that extraction.
3. Combine them into the format: `"Extracted Text (confidence)"`.

Contextual components: 

1. TIME: A regularly recurring point or period of time that serves as a temporal cue for the occurrence of a habit.  
    e.g., "every morning", "before going to bed", "at 8 p.m.", "on Sundays"
2. PHYSICAL SETTING: A physical environment in which a habit is typically performed.  
    e.g., "in the kitchen", "at the gym", "in the office", "on the balcony"
3. PRIOR BEHAVIOR: An immediately preceding behavior that unconsciously triggers the execution of the habitual behavior.  
    e.g., "after brushing teeth", "after finishing lunch", "after turning off the alarm"
4. OTHER PEOPLE: Individuals who are consistently present or involved in the context where the habit occurs; their presence functions as a recurring cue that can automatically trigger or modulate the habitual behavior.  
    e.g., "when I'm with colleagues", "if my partner is around", "when no one else is home"
5. INTERNAL STATE: An internal psychological, physiological, or emotional condition that accompanies or prompts the habitual behavior.  
    e.g., "when I feel tired", "when I'm anxious", "when I'm in a good mood"
6. BEHAVIOR: The observable action or sequence of actions that occurs under the influence of the above cues, typically executed with low conscious control and high efficiency.  
    e.g., "drinking coffee", "checking the phone", "taking a walk", "opening a news app"

OUTPUT FORMAT:

- If a component is not present in the sentence, leave the corresponding cell in the CSV entirely blank.
- The output must be strictly in valid CSV format.
- The first line of the header must be:
Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR.
- The output format must strictly adhere to the following:
`Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"`
- The "Original Sentence" column must contain the sentence exactly as provided, without correcting spelling or punctuation.
- Do not output anything outside of the CSV table.

Now, please process the following list of sentences:


['Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.', 'Immer wenn ich müde bin, mache ich Atemübungen. ', 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ', 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ', 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ', 'Nach dem Aufstehen mache ich Kraftsport', 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ', 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ', 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ', 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ', 'Morgens nach dem Aufstehen wasche ich mein Gesicht.', 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.', 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.', 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.', 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.', 'Morgens nach der Tierfütterung trinke ich einen Kaffee.', 'Nach dem Joggen trinke ich einen Proteinshake.', 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier', 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.', 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel', 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.', 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.', 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.', 'wenn ich ins DM gehe, kaufe ich mir was Süßes.', 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout', 'nach dem Abendbrot wasche ich ab', 'Nach dem Aufstehen mache ich ein paar Sprachübungen', 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe', 'Ich nehme VItamin D tabletten ein', 'Samstags putze ich das Bad.', 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.', 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade', 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ']"""
    )
    llm_dict[
        "gpt4.1"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (0.98)",,"nach dem Aufstehen (0.97)",,,"trinke ich direkt einen Kafffe (0.99)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","Immer (0.80)",,,"","wenn ich müde bin (0.99)","mache ich Atemübungen (0.99)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,"wenn ich ein negatives Gefühl stark fühle (0.98)","versuche ich es auszufühlen (0.95)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (0.98)",,"nach dem Abendbrot (0.97)",,,"trinke ich ein Glas Wein (0.99)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.97)",,,"","wenn ich am Wochenende zum Bäcker gehe (0.96)","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.98)"
6,"Nach dem Aufstehen mache ich Kraftsport",,,"Nach dem Aufstehen (0.97)",,,"mache ich Kraftsport (0.98)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,,"","Sobald ich eine Aufgabe sehe (0.92)","trage ich sie in Notion ein (0.97)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,,,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.95)","trete ich dem Meeting bei (0.98)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.90)",,"","noch niemand daheim erwartet (0.93)","","spaziere ich nach Hause (0.99)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.97)","in Dresden (0.98)",,,, "verbringe ich einen Tag mit mir allein (0.98)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (0.98)",,"nach dem Aufstehen (0.97)",,,"wasche ich mein Gesicht (0.98)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (0.96)",,"nach dem Gesichtwaschen (0.97)",,,"putze ich meine Zähne (0.99)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (0.96)",,"nach dem Zähneputzen (0.97)",,,"creme ich mein Gesicht ein (0.98)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (0.98)",,"nach dem Gesicht-Eincremen (0.96)",,,"füttere ich die Katze (0.98)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (0.98)",,"nach der Katzenfütterung (0.97)",,,"bekommt der Hund eine Kaustange (0.97)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (0.98)",,"nach der Tierfütterung (0.97)",,,"trinke ich einen Kaffee (0.99)"
17,"Nach dem Joggen trinke ich einen Proteinshake",,,"Nach dem Joggen (0.98)",,,"trinke ich einen Proteinshake (0.98)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"Wenn ich Lust auf ein Bier/Wein habe (0.96)","trinke ich ein Malzbier (0.97)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.97)",,,,"","mache ich meine Ohrstöpsel ins Ohr (0.97)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.97)",,,,"","nehme ich meine Nahrungsergänzungsmittel (0.98)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"Wenn ich gestresst bin (0.99)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.98)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,,"Nach dem Aufstehen (0.97)",,,"mache ich mir ein Zitronenwasser (0.97)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.89)","ins Bett (0.91)","","","","scrolle ich sinnlos durch social media (0.98)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM gehe (0.97)",,,"","kaufe ich mir was Süßes (0.98)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.95)",,,"mach ich ein kurzes HIT Workout (0.97)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.97)",,,"wasche ich ab (0.95)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.97)",,,"mache ich ein paar Sprachübungen (0.97)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,,"wenn ich aus der  WOhnung gehe (0.97)","","Ich prüfe ob ich meinen Schlüssel dabeihabe (0.95)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"Ich nehme VItamin D tabletten ein (0.98)"
30,"Samstags putze ich das Bad.","Samstags (0.99)",,,,"","putze ich das Bad (0.99)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.93)",,"","Wenn es nicht regnet (0.91)","","gieße ich den Apfelbaum (0.97)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade",,,"Nach dem Abendbrot (0.97)",,,"an einem stressigen Tag (0.92)","esse ich gern ein Stück Schokolade (0.97)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.95)","ins Bett (0.91)","Nach dem Sport (0.96)",,,"gehe ich oft erst spät ins Bett (0.95)"
"""

    llm_dict[
        "gpt4.1 mini"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)","","","",,"trinke ich direkt einen Kafffe (0.95)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","Immer wenn ich müde bin (0.90)","","","","müde bin (0.90)","mache ich Atemübungen (0.95)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","Wenn ich ein negatives Gefühl stark fühle (0.90)","","","","ein negatives Gefühl stark fühle (0.90)","versuche ich es auszufühlen (0.90)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.95)","","","",,"trinke ich ein Glas Wein (0.95)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.90)","zum Bäcker (0.85)","zum Bäcker gehe (0.85)",,"","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.90)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)","","Nach dem Aufstehen (0.85)",,"mache ich Kraftsport (0.95)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","Sobald ich eine Aufgabe sehe (0.85)","","Sobald ich eine Aufgabe sehe (0.85)",,,"trage ich sie in Notion ein (0.90)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","",,"","ein Kollege im EvalGiGe Meeting (0.90)",,"trete ich dem Meeting bei (0.85)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.95)","daheim (0.85)","","niemand daheim erwartet (0.85)",,"spaziere ich nach Hause (0.90)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.95)","","","mit mir allein (0.85)",,"verbringe ich einen Tag in Dresden (0.85)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)","","","",,"wasche ich mein Gesicht (0.90)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.90)","","nach dem Gesichtwaschen (0.90)","","","putze ich meine Zähne (0.95)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.90)","","nach dem Zähneputzen (0.90)","","","creme ich mein Gesicht ein (0.95)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.90)","","nach dem Gesicht-Eincremen (0.90)","","","füttere ich die Katze (0.95)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.95)","","nach der Katzenfütterung (0.90)","","","bekommt der Hund eine Kaustange (0.90)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.95)","","nach der Tierfütterung (0.90)","","","trinke ich einen Kaffee (0.90)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","","",Nach dem Joggen (0.95),,"","trinke ich einen Proteinshake (0.95)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","","","","Lust auf ein Bier/Wein habe (0.85)","trinke ich ein Malzbier (0.90)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.90)","","","",,"mache ich meine Ohrstöpsel ins Ohr (0.90)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.90)","","","",,"nehme ich meine Nahrungsergänzungsmittel (0.90)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","",,"","",gestresst bin (0.90),"gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.90)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)","","","",,"mache ich mir ein Zitronenwasser (0.90)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.85)","","","",,"scrolle ich sinnlos durch social media (0.90)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","",,"wenn ich ins DM gehe (0.85)","","","kaufe ich mir was Süßes (0.90)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen trinken und Medikamenteinnahme (0.90)","","nach dem Aufstehen trinken und Medikamenteinnahme (0.90)","","","mach ich ein kurzes HIT Workout (0.90)"
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.95)","","","",,"wasche ich ab (0.90)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)","","","",,"mache ich ein paar Sprachübungen (0.90)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe","",,"wenn ich aus der  WOhnung gehe (0.90)","","","Ich prüfe ob ich meinen Schlüssel dabeihabe (0.90)"
29,"Ich nehme VItamin D tabletten ein","","","","","","nehme VItamin D tabletten ein (0.95)"
30,"Samstags putze ich das Bad.","Samstags (0.95)","das Bad (0.90)","","","","putze ich das Bad (0.90)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.90)","","","",,"gieße ich den Apfelbaum (0.90)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.90)","","","",stressigen Tag (0.85),"esse ich gern ein Stück Schokolade (0.90)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.95)","","Nach dem Sport (0.90)","","","gehe ich oft erst spät ins Bett (0.90)"
"""

    llm_dict[
        "o3"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (0.90)",,"nach dem Aufstehen (0.90)",,,"trinke ich direkt einen Kafffe (0.90)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,,"wenn ich müde bin (0.85)","mache ich Atemübungen (0.90)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,,"Wenn ich ein negatives Gefühl stark fühle (0.80)","versuche ich es auszufühlen (0.80)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (0.90)",,"nach dem Abendbrot (0.85)",,,"trinke ich ein Glas Wein (0.90)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.70)","zum Bäcker (0.50)","zum Bäcker gehe (0.60)",,,"mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.80)"
6,"Nach dem Aufstehen mache ich Kraftsport",,,"Nach dem Aufstehen (0.90)",,,"mache ich Kraftsport (0.90)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.70)",,,"trage ich sie in Notion ein (0.85)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,"Wenn mir in Teams angezeigt wird (0.50)","dass sich ein Kollege im EvalGiGe Meeting befindet (0.70)",,"trete ich dem Meeting bei (0.80)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.80)",,,"","noch niemand daheim erwartet (0.70)",,"spaziere ich nach Hause (0.85)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.80)","in Dresden (0.75)",,"mit mir allein (0.50)",,"verbringe ich einen Tag (0.70)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (0.90)",,"nach dem Aufstehen (0.90)",,,"wasche ich mein Gesicht (0.90)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (0.85)",,"nach dem Gesichtwaschen (0.85)",,,"putze ich meine Zähne (0.85)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (0.85)",,"nach dem Zähneputzen (0.85)",,,"creme ich mein Gesicht ein (0.85)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (0.90)",,"nach dem Gesicht-Eincremen (0.90)",,,"füttere ich die Katze (0.90)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (0.90)",,"nach der Katzenfütterung (0.90)",,,"bekommt der Hund eine Kaustange (0.80)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (0.90)",,"nach der Tierfütterung (0.90)",,,"trinke ich einen Kaffee (0.90)"
17,"Nach dem Joggen trinke ich einen Proteinshake",,,"Nach dem Joggen (0.90)",,,"trinke ich einen Proteinshake (0.90)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,,"Lust auf ein Bier/Wein habe (0.80)","trinke ich ein Malzbier (0.85)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.80)",,,,"","mache ich meine Ohrstöpsel ins Ohr (0.85)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.80)",,,,"","nehme ich meine Nahrungsergänzungsmittel (0.85)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,"zum Kühlschrank (0.80)",,,"gestresst bin (0.85)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.85)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,,"Nach dem Aufstehen (0.90)",,,"mache ich mir ein Zitronenwasser (0.90)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.80)",,"mich abends ins Bett lege (0.75)",,,"scrolle ich sinnlos durch social media (0.90)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM (0.80)","ins DM gehe (0.75)",,,,"kaufe ich mir was Süßes (0.90)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.70)",,,"mach ich ein kurzes HIT Workout (0.85)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.90)",,,"wasche ich ab (0.80)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.90)",,,"mache ich ein paar Sprachübungen (0.85)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der  WOhnung gehe (0.80)",,,"Ich prüfe ob ich meinen Schlüssel dabeihabe (0.85)"
29,"Ich nehme VItamin D tabletten ein",,,,,,,"Ich nehme VItamin D tabletten ein (0.60)"
30,"Samstags putze ich das Bad.","Samstags (0.90)","das Bad (0.60)",,,,"putze ich das Bad (0.90)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.80)",,,,"","gieße ich den Apfelbaum (0.85)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade",,,"Nach dem Abendbrot (0.90)",,"an einem stressigen Tag (0.75)","esse ich gern ein Stück Schokolade (0.90)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.80)",,"Nach dem Sport (0.90)",,,"gehe ich oft erst spät ins Bett (0.85)"
"""

    llm_dict[
        "o4 mini (High Effort)"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (0.95)","","nach dem Aufstehen (0.95)","","","trinke ich direkt einen Kafffe (0.95)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","","","","Wenn ich müde bin (0.95)","mache ich Atemübungen (0.95)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","","","","Wenn ich ein negatives Gefühl stark fühle (0.95)","versuche ich es auszufühlen (0.95)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (0.95)","","nach dem Abendbrot (0.95)","","","trinke ich ein Glas Wein (0.95)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.95)","in mein Lieblingscafe (0.90)","Wenn ich am Wochenende zum Bäcker gehe (0.90)","","","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.90)"
6,"Nach dem Aufstehen mache ich Kraftsport","","","nach dem Aufstehen (0.95)","","","mache ich Kraftsport (0.95)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","","","Sobald ich eine Aufgabe sehe (0.95)","","","trage ich sie in Notion ein (0.95)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","","","Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.95)","ein Kollege (0.90)","trete ich dem Meeting bei (0.95)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.95)","","","noch niemand daheim erwartet (0.90)","spaziere ich nach Hause (0.95)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.95)","in Dresden (0.90)","","","verbringe ich einen Tag mit mir allein (0.95)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (0.95)","","nach dem Aufstehen (0.95)","","","wasche ich mein Gesicht (0.95)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (0.90)","","nach dem Gesichtwaschen (0.95)","","","putze ich meine Zähne (0.95)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (0.90)","","nach dem Zähneputzen (0.95)","","","creme ich mein Gesicht ein (0.95)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (0.95)","","nach dem Gesicht-Eincremen (0.95)","","","füttere ich die Katze (0.95)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (0.95)","","nach der Katzenfütterung (0.95)","","","bekommt der Hund eine Kaustange (0.95)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (0.95)","","nach der Tierfütterung (0.95)","","","trinke ich einen Kaffee (0.95)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","","","Nach dem Joggen (0.95)","","","trinke ich einen Proteinshake (0.95)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","","","","","Wenn ich Lust auf ein Bier/Wein habe (0.95)","trinke ich ein Malzbier (0.95)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)","","","","","mache ich meine Ohrstöpsel ins Ohr (0.95)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)","","","","","nehme ich meine Nahrungsergänzungsmittel (0.95)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","","","","Wenn ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.95)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","","","Nach dem Aufstehen (0.95)","","","mache ich mir ein Zitronenwasser (0.95)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","","","","Wenn ich mich abends ins Bett lege (0.95)","scrolle ich sinnlos durch social media (0.95)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","","","wenn ich ins DM gehe (0.95)","","","kaufe ich mir was Süßes (0.95)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","","","nach dem Aufstehen trinken und Medikamenteinnahme (0.85)","","","mach ich ein kurzes HIT Workout (0.95)"
26,"nach dem Abendbrot wasche ich ab","","","nach dem Abendbrot (0.95)","","","wasche ich ab (0.95)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","","","Nach dem Aufstehen (0.95)","","","mache ich ein paar Sprachübungen (0.95)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe","","","wenn ich aus der  WOhnung gehe (0.95)","","","Ich prüfe ob ich meinen Schlüssel dabeihabe (0.95)"
29,"Ich nehme VItamin D tabletten ein","","","","","nehme VItamin D tabletten ein (0.95)"
30,"Samstags putze ich das Bad.","Samstags (0.95)","","","","","putze ich das Bad (0.95)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.95)","","Wenn es nicht regnet (0.90)","","","gieße ich den Apfelbaum (0.95)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade.","an einem stressigen Tag (0.90)","","Nach dem Abendbrot (0.95)","","","esse ich gern ein Stück Schokolade (0.95)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett.","","","Nach dem Sport am Abend (0.95)","","","gehe ich oft erst spät ins Bett (0.95)"
"""

    llm_dict[
        "o3 mini (High Effort)"
    ].output = """Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (0.95)",,"nach dem Aufstehen (0.95)",, "trinke ich direkt einen Kafffe (0.95)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,"",,"müde bin (0.95)","mache ich Atemübungen (0.95)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,"","ein negatives Gefühl stark fühle (0.95)","versuche ich es auszufühlen (0.95)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (0.95)",,"nach dem Abendbrot (0.95)",, "trinke ich ein Glas Wein (0.95)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.95)","zum Bäcker (0.95)","zum Bäcker gehe (0.95)",, "mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.95)"
6,"Nach dem Aufstehen mache ich Kraftsport",,,"Nach dem Aufstehen (0.95)",, "mache ich Kraftsport (0.95)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.95)",, "trage ich sie in Notion ein (0.95)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,,"ein Kollege (0.95)", "trete ich dem Meeting bei (0.95)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.95)",,,"niemand daheim (0.90)", "spaziere ich nach Hause (0.95)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.95)","in Dresden (0.95)",,,"","verbringe ich einen Tag (0.95)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (0.95)",,"nach dem Aufstehen (0.95)",, "wasche ich mein Gesicht (0.95)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (0.95)",,"nach dem Gesichtwaschen (0.95)",, "putze ich meine Zähne (0.95)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (0.95)",,"nach dem Zähneputzen (0.95)",, "creme ich mein Gesicht ein (0.95)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (0.95)",,"nach dem Gesicht-Eincremen (0.95)",, "füttere ich die Katze (0.95)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (0.95)",,"nach der Katzenfütterung (0.95)",, "bekommt der Hund eine Kaustange (0.95)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (0.95)",,"nach der Tierfütterung (0.95)",, "trinke ich einen Kaffee (0.95)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,,"Nach dem Joggen (0.95)",, "trinke ich einen Proteinshake (0.95)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,"",, "Lust auf ein Bier/Wein habe (0.95)","trinke ich ein Malzbier (0.95)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)",,,"",, "mache ich meine Ohrstöpsel ins Ohr (0.95)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)",,,"",, "nehme ich meine Nahrungsergänzungsmittel (0.95)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,"zum Kühlschrank (0.95)",,,"gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.95)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,,"Nach dem Aufstehen (0.95)",, "mache ich mir ein Zitronenwasser (0.95)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","mich abends ins Bett lege (0.95)",,,"",, "scrolle ich sinnlos durch social media (0.95)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM (0.95)","ins DM gehe (0.95)",, "kaufe ich mir was Süßes (0.95)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.95)",, "mach ich ein kurzes HIT Workout (0.95)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.95)",, "wasche ich ab (0.95)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.95)",, "mache ich ein paar Sprachübungen (0.95)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,"der  WOhnung (0.95)","wenn ich aus der  WOhnung gehe (0.95)",, "Ich prüfe ob ich meinen Schlüssel dabeihabe (0.95)"
29,"Ich nehme VItamin D tabletten ein",,,,, "Ich nehme VItamin D tabletten ein (0.95)"
30,"Samstags putze ich das Bad.","Samstags (0.95)",,,"",, "putze ich das Bad (0.95)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.95)",,,"",, "gieße ich im Sommer jeden Tag den Apfelbaum (0.95)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade",,,"Nach dem Abendbrot (0.95)",, "an einem stressigen Tag (0.95)","esse ich gern ein Stück Schokolade (0.95)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett.","am Abend (0.95)",, "Nach dem Sport (0.95)",, "gehe ich oft erst spät ins Bett (0.95)"
"""

    llm_dict[
        "GPT-4o mini"
    ].output = """```csv
Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR.
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)","",""," "," ","trinke ich direkt einen Kafffe (0.90)."
2,"Immer wenn ich müde bin, mache ich Atemübungen.",""," "," "," ","wenn ich müde bin (0.90)","mache ich Atemübungen (0.95)."
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",""," "," "," ","ein negatives Gefühl stark fühle (0.85)","versuche ich es auszufühlen (0.90)."
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (0.85)","",""," "," ","trinke ich ein Glas Wein (0.90)."
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.90)","",""," "," ","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.95)."
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)","",""," "," ","mache ich Kraftsport (0.85)."
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",""," ","siehe eine Aufgabe (0.90)"," "," ","trage ich sie in Notion ein (0.90)."
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",""," "," ","Kollege (0.80)"," ","trete ich dem Meeting bei (0.85)."
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.",""," "," ","niemand daheim erwartet (0.80)"," ","spaziere ich nach Hause (0.90)."
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.85)","",""," "," ","verbringe ich einen Tag mit mir allein in Dresden (0.90)."
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)","",""," "," ","wasche ich mein Gesicht (0.90)."
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.90)","",""," "," ","putze ich meine Zähne (0.85)."
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.90)","",""," "," ","creme ich mein Gesicht ein (0.85)."
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.90)","",""," "," ","füttere ich die Katze (0.90)."
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.90)","",""," "," ","bekommt der Hund eine Kaustange (0.85)."
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.90)","",""," "," ","trinke ich einen Kaffee (0.90)."
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.90)","",""," "," ","trinke ich einen Proteinshake (0.85)."
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier"," "," "," "," ","Lust auf ein Bier/Wein habe (0.85)","trinke ich ein Malzbier (0.90)."
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.90)","",""," "," ","mache ich meine Ohrstöpsel ins Ohr (0.85)."
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.90)","",""," "," ","nehme ich meine Nahrungsergänzungsmittel (0.90)."
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",""," "," ","gestresst bin (0.90)"," ","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.85)."
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)","",""," "," ","mache ich mir ein Zitronenwasser (0.90)."
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.80)","",""," "," ","scrolle ich sinnlos durch social media (0.90)."
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",""," ","ins DM gehe (0.80)"," "," ","kaufe ich mir was Süßes (0.90)."
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen (0.95)","",""," "," ","mach ich ein kurzes HIT Workout (0.85)."
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.90)","",""," "," ","wasche ich ab (0.80)."
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)","",""," "," ","mache ich ein paar Sprachübungen (0.90)."
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe"," "," ","wenn ich aus der WOhnung gehe (0.85)"," "," ","prüfe ob ich meinen Schlüssel dabeihabe (0.90)."
29,"Ich nehme VItamin D tabletten ein"," "," "," "," "," ","nehme Vitamin D tabletten ein (0.90)."
30,"Samstags putze ich das Bad.","Samstags (0.90)","",""," "," ","putze ich das Bad (0.90)."
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.85)","",""," "," ","gieße ich den Apfelbaum (0.90)."
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.85)","",""," ","stressigen Tag (0.80)","esse ich gern ein Stück Schokolade (0.90)."
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.90)","",""," "," ","gehe ich oft erst spät ins Bett (0.90)."
```
"""

    llm_dict[
        "GPT-4o"
    ].output = """```csv
Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (0.90)",,"nach dem Aufstehen (0.95)",,,"trinke ich direkt einen Kafffe. (0.95)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,"wenn ich müde bin (0.95)","mache ich Atemübungen. (0.95)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,,"versuche ich es auszufühlen. (0.85)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (0.85)",,"nach dem Abendbrot (0.90)",,,"trinke ich ein Glas Wein. (0.90)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.",,,,"wenn ich am Wochenende zum Bäcker gehe (0.85)","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. (0.85)"
6,"Nach dem Aufstehen mache ich Kraftsport",,,"Nach dem Aufstehen (0.95)",,,"mache ich Kraftsport (0.95)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,,,"trage ich sie in Notion ein. (0.85)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,,,"wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)","dann trete ich dem Meeting bei. (0.85)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.",,,,,"wenn mich nach Feierabend noch niemand daheim erwartet (0.90)","dann spaziere ich nach Hause. (0.85)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.80)","in Dresden (0.85)",,,,"verbringe ich einen Tag mit mir allein (0.85)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (0.90)",,"nach dem Aufstehen (0.95)",,,"wasche ich mein Gesicht. (0.95)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (0.85)",,"nach dem Gesichtwaschen (0.95)",,,"putze ich meine Zähne. (0.95)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (0.85)",,"nach dem Zähneputzen (0.95)",,,"creme ich mein Gesicht ein. (0.95)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (0.90)",,"nach dem Gesicht-Eincremen (0.95)",,,"füttere ich die Katze. (0.95)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (0.90)",,"nach der Katzenfütterung (0.95)",,,"bekommt der Hund eine Kaustange. (0.95)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (0.90)",,"nach der Tierfütterung (0.95)",,,"trinke ich einen Kaffee. (0.95)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,,"Nach dem Joggen (0.95)",,,"trinke ich einen Proteinshake. (0.95)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"wenn ich Lust auf ein Bier/Wein habe (0.90)","trinke ich ein Malzbier (0.90)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.90)",,,,"mache ich meine Ohrstöpsel ins Ohr. (0.90)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.90)",,,,"nehme ich meine Nahrungsergänzungsmittel (0.90)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"wenn ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.90)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,,"Nach dem Aufstehen (0.95)",,,"mache ich mir ein Zitronenwasser (0.95)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.",,,"Wenn ich mich abends ins Bett lege (0.85)",,"scrolle ich sinnlos durch social media (0.90)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,,,"wenn ich ins DM gehe (0.85)","kaufe ich mir was Süßes. (0.85)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.85)",,,"mach ich ein kurzes HIT Workout (0.90)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.90)",,,"wasche ich ab (0.90)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.95)",,,"mache ich ein paar Sprachübungen (0.95)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,,"wenn ich aus der  WOhnung gehe (0.85)","prüfe ob ich meinen Schlüssel dabeihabe (0.85)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"Ich nehme VItamin D tabletten ein (0.80)"
30,"Samstags putze ich das Bad.","Samstags (0.85)",,,,,"putze ich das Bad. (0.85)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.",,"im Sommer (0.85)",,"Wenn es nicht regnet (0.90)","gieße ich jeden Tag den Apfelbaum (0.90)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade",,,"Nach dem Abendbrot an einem stressigen Tag (0.85)",,"esse ich gern ein Stück Schokolade (0.90)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.85)",,"Nach dem Sport (0.90)",,,"gehe ich oft erst spät ins Bett (0.85)"
```
"""

    llm_dict[
        "DeepSeek-Coder-V2-Lite-Instruct"
    ].output = """ ```csv
Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens","in the kitchen",,"","","drink coffee"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","","",,"","when I'm tired","do breathing exercises"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","","",,"","when I feel a negative emotion","try to express it"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends","in the living room",,"","","drink a glass of wine"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","on Sundays","in the cafe",,"","","drink a cappuccino"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen","at the gym",,"","","do strength training"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","","in the office",,"","when I see a task","enter it in Notion"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","","in the office",,"when I see a colleague in a meeting","","join the meeting"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","after work","in the city",,"when no one is home","","go for a walk home"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","once a month","in Dresden",,"","","spend a day alone"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens","in the bathroom",,"","","wash my face"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","","in the bathroom",,"","","brush my teeth"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","","in the bathroom",,"","","apply face cream"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens","in the kitchen",,"","","feed the cat"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens","in the kitchen",,"after feeding the cat","","give the dog a chew toy"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens","in the kitchen",,"after feeding the cat and dog","","drink coffee"
17,"Nach dem Joggen trinke ich einen Proteinshake.","after jogging","in the kitchen",,"","","drink a protein shake"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","when I want","in the living room",,"","","drink craft beer/wine"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","before sleeping","in the bedroom",,"","","put earplugs in"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","before sleeping","in the bedroom",,"","","take my supplements"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","when I'm stressed","in the kitchen",,"","","grab something to eat from the fridge"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","after waking up","in the kitchen",,"","","make lemon water"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","before bed","in the bedroom",,"","","scroll through social media"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","when I go to DM","in the store",,"","","buy something sweet"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","after waking up","in the living room",,"","","do a short HIIT workout"
26,"nach dem Abendbrot wasche ich ab","after dinner","in the bathroom",,"","","take a shower"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","after waking up","in the living room",,"","","do language exercises"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe","when I leave the house","in the hallway",,"","","check if I have my keys"
29,"Ich nehme Vitamin D tabletten ein","every day","in the kitchen",,"","","take vitamin D supplements"
30,"Samstags putze ich das Bad.","on Saturdays","in the bathroom",,"","","clean the bathroom"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","if it doesn't rain","in the garden",,"","","water the apple tree"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","after dinner on a stressful day","in the living room",,"","","eat a piece of chocolate"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","after the gym in the evening","in the bedroom",,"","","go to bed late"
```
"""
    llm_dict[
        "DeepSeek-R1"
    ].output = """

Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (1.00)","","nach dem Aufstehen (0.95)","","","trinke ich direkt einen Kafffe (0.90)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","","","","","wenn ich müde bin (0.95)","mache ich Atemübungen (0.95)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","","","","","ein negatives Gefühl stark fühle (0.90)","versuche ich es auszufühlen (0.85)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (1.00)","","nach dem Abendbrot (0.95)","","","trinke ich ein Glas Wein (0.95)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (1.00)","in mein Lieblingscafe (0.80)","zum Bäcker gehe (0.90)","","","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.95)"
6,"Nach dem Aufstehen mache ich Kraftsport","","","Nach dem Aufstehen (0.95)","","","mache ich Kraftsport (0.95)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","","","eine Aufgabe sehe (0.90)","","","trage ich sie in Notion ein (0.95)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","","","","ein Kollege (0.80)","","trete ich dem Meeting bei (0.95)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.85)","","","niemand daheim erwartet (0.90)","","spaziere ich nach Hause (0.95)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.95)","in Dresden (0.80)","","","","verbringe ich einen Tag mit mir allein (0.90)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (1.00)","","nach dem Aufstehen (0.95)","","","wasche ich mein Gesicht (0.95)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (1.00)","","nach dem Gesichtwaschen (0.95)","","","putze ich meine Zähne (0.95)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (1.00)","","nach dem Zähneputzen (0.95)","","","creme ich mein Gesicht ein (0.95)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (1.00)","","nach dem Gesicht-Eincremen (0.95)","","","füttere ich die Katze (0.95)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (1.00)","","nach der Katzenfütterung (0.95)","","","bekommt der Hund eine Kaustange (0.95)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (1.00)","","nach der Tierfütterung (0.95)","","","trinke ich einen Kaffee (0.95)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","","","Nach dem Joggen (0.95)","","","trinke ich einen Proteinshake (0.95)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","","","","","Lust auf ein Bier/Wein habe (0.90)","trinke ich ein Malzbier (0.95)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)","","","","","mache ich meine Ohrstöpsel ins Ohr (0.95)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)","","","","","nehme ich meine Nahrungsergänzungsmittel (0.95)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","","","","","gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.95)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","","","Nach dem Aufstehen (0.95)","","","mache ich mir ein Zitronenwasser (0.95)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (1.00)","ins Bett (0.90)","mich ins Bett lege (0.90)","","","scrolle ich sinnlos durch social media (0.95)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","","","ins DM gehe (0.90)","","","kaufe ich mir was Süßes (0.95)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","","","nach dem Aufstehen trinken und Medikamenteinnahme (0.90)","","","mach ich ein kurzes HIT Workout (0.95)"
26,"nach dem Abendbrot wasche ich ab","","","nach dem Abendbrot (0.95)","","","wasche ich ab (0.95)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","","","Nach dem Aufstehen (0.95)","","","mache ich ein paar Sprachübungen (0.95)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe","","","","","","prüfe ob ich meinen Schlüssel dabeihabe (0.95)"
29,"Ich nehme VItamin D tabletten ein","","","","","","nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (1.00)","","","","","putze ich das Bad (0.95)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.90)","","","","","gieße ich den Apfelbaum (0.95)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","","","Nach dem Abendbrot (0.95)","","","esse ich gern ein Stück Schokolade (0.95)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.95)","","Nach dem Sport (0.95)","","","gehe ich oft erst spät ins Bett (0.95)"
"""

    llm_dict[
        "Llama-3.3-70B-Instruct"
    ].output = """Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.90)","" ,"nach dem Aufstehen (0.80)","","","trinke ich direkt einen Kafffe (0.95)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","" ,"","" ,"","müde bin (0.85)","mache ich Atemübungen (0.90)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","" ,"","" ,"","ein negatives Gefühl stark fühle (0.80)","versuche ich es auszufühlen (0.85)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.90)","" ,"nach dem Abendbrot (0.80)","","","trinke ich ein Glas Wein (0.95)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","am Wochenende (0.80)","zum Bäcker (0.70)", "zum Bäcker gehe (0.75)","","","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (0.90)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.90)","" ,"nach dem Aufstehen (0.80)","","","mache ich Kraftsport (0.95)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","" ,"","" ,"","" ,"trage ich sie in Notion ein (0.90)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","" ,"in Teams (0.70)","" ,"ein Kollege (0.80)","","trete ich dem Meeting bei (0.90)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.80)","" ,"nach Feierabend (0.75)","niemand (0.70)","","spaziere ich nach Hause (0.90)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.90)","in Dresden (0.85)","" ,"mit mir allein (0.80)","","verbringe ich einen Tag (0.90)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.90)","" ,"nach dem Aufstehen (0.80)","","","wasche ich mein Gesicht (0.95)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.90)","" ,"nach dem Gesichtwaschen (0.85)","","","putze ich meine Zähne (0.95)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.90)","" ,"nach dem Zähneputzen (0.85)","","","creme ich mein Gesicht ein (0.95)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.90)","" ,"nach dem Gesicht-Eincremen (0.85)","","","füttere ich die Katze (0.95)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.90)","" ,"nach der Katzenfütterung (0.85)","","","bekommt der Hund eine Kaustange (0.95)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.90)","" ,"nach der Tierfütterung (0.85)","","","trinke ich einen Kaffee (0.95)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.90)","" ,"nach dem Joggen (0.85)","","","trinke ich einen Proteinshake (0.95)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","" ,"","" ,"","Lust auf ein Bier/Wein habe (0.80)","trinke ich ein Malzbier (0.90)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.90)","" ,"bevor ich schlafe (0.85)","","","mache ich meine Ohrstöpsel ins Ohr (0.95)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.90)","" ,"bevor ich schlafen gehe (0.85)","","","nehme ich meine Nahrungsergänzungsmittel (0.95)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","" ,"zum Kühlschrank (0.80)","" ,"","gestresst bin (0.85)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.90)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.90)","" ,"nach dem Aufstehen (0.80)","","","mache ich mir ein Zitronenwasser (0.95)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.70)","ins Bett (0.75)","mich abends ins Bett lege (0.80)","","","scrolle ich sinnlos durch social media (0.90)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","" ,"ins DM (0.80)","ins DM gehe (0.75)","","","kaufe ich mir was Süßes (0.90)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen (0.90)","" ,"nach dem Aufstehen (0.80)","","","mach ich ein kurzes HIT Workout (0.95)"
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.90)","" ,"nach dem Abendbrot (0.80)","","","wasche ich ab (0.95)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.90)","" ,"nach dem Aufstehen (0.80)","","","mache ich ein paar Sprachübungen (0.95)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe","" ,"aus der  WOhnung (0.75)","aus der  WOhnung gehe (0.80)","","","prüfe ob ich meinen Schlüssel dabeihabe (0.90)"
29,"Ich nehme VItamin D tabletten ein","" ,"","" ,"","","nehme VItamin D tabletten ein (0.90)"
30,"Samstags putze ich das Bad.","Samstags (0.90)","das Bad (0.85)","" ,"","","putze ich das Bad (0.95)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer (0.80)","" ,"Wenn es nicht regnet (0.75)","","","gieße ich im Sommer jeden Tag den Apfelbaum (0.90)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot (0.90)","" ,"nach dem Abendbrot (0.80)","","an einem stressigen Tag (0.85)","esse ich gern ein Stück Schokolade (0.95)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.90)","" ,"nach dem Sport (0.80)","","","gehe ich oft erst spät ins Bett (0.95)"
"""


    llm_dict[
        "gpt-oss-120b"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"'Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.'","Morgens nach dem Aufstehen (0.98)","","nach dem Aufstehen (0.95)","","","trinke ich direkt einen Kafffe (0.97)"
2,"'Immer wenn ich müde bin, mache ich Atemübungen.'","","","","","wenn ich müde bin (0.96)","mache ich Atemübungen (0.96)"
3,"'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.'","","","","","wenn ich ein negatives Gefühl stark fühle (0.95)","versuche ich es auszufühlen (0.94)"
4,"'Abends nach dem Abendbrot trinke ich ein Glas Wein.'","Abends nach dem Abendbrot (0.98)","","nach dem Abendbrot (0.93)","","","trinke ich ein Glas Wein (0.97)"
5,"'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.'","am Wochenende (0.90)","mein Lieblingscafe (0.93)","gehe zum Bäcker (0.90)","","","trinke einen Cappucino (0.95)"
6,"'Nach dem Aufstehen mache ich Kraftsport'","","","nach dem Aufstehen (0.96)","","","mache ich Kraftsport (0.96)"
7,"'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.'","","","","","","trage ich sie in Notion ein (0.96)"
8,"'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.'","","","","ein Kollege im EvalGiGe Meeting (0.90)","","trete ich dem Meeting bei (0.94)"
9,"'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.'","nach Feierabend (0.95)","","","niemand daheim (0.85)","","spaziere ich nach Hause (0.96)"
10,"'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.'","Einmal im Monat (0.97)","in Dresden (0.95)","","","", "verbringe ich einen Tag (0.93)"
11,"'Morgens nach dem Aufstehen wasche ich mein Gesicht.'","Morgens nach dem Aufstehen (0.98)","","nach dem Aufstehen (0.95)","","","wasche ich mein Gesicht (0.96)"
12,"'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.'","Morgens/Abends (0.97)","","nach dem Gesichtwaschen (0.94)","","","putze ich meine Zähne (0.96)"
13,"'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.'","Morgens/Abends (0.97)","","nach dem Zähneputzen (0.94)","","","creme ich mein Gesicht ein (0.96)"
14,"'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.'","Morgens nach dem Gesicht-Eincremen (0.95)","","nach dem Gesicht-Eincremen (0.94)","","","füttere ich die Katze (0.96)"
15,"'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.'","Morgens nach der Katzenfütterung (0.95)","","nach der Katzenfütterung (0.94)","","","bekommt der Hund eine Kaustange (0.90)"
16,"'Morgens nach der Tierfütterung trinke ich einen Kaffee.'","Morgens nach der Tierfütterung (0.95)","","nach der Tierfütterung (0.94)","","","trinke ich einen Kaffee (0.96)"
17,"'Nach dem Joggen trinke ich einen Proteinshake.'","","","nach dem Joggen (0.96)","","","trinke ich einen Proteinshake (0.96)"
18,"'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier'","","","","","wenn ich Lust auf ein Bier/Wein habe (0.95)","trinke ich ein Malzbier (0.96)"
19,"'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.'","Bevor ich schlafe (0.96)","","","","","mache ich meine Ohrstöpsel ins Ohr (0.94)"
20,"'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel'","Bevor ich schlafen gehe (0.96)","","","","","nehme ich meine Nahrungsergänzungsmittel (0.94)"
21,"'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.'","","","","","wenn ich gestresst bin (0.96)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.94)"
22,"'Nach dem Aufstehen mache ich mir ein Zitronenwasser.'","","","nach dem Aufstehen (0.96)","","","mache ich mir ein Zitronenwasser (0.95)"
23,"'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.'","abends (0.90)","","wenn ich mich abends ins Bett lege (0.90)","","","scrolle ich sinnlos durch social media (0.96)"
24,"'wenn ich ins DM gehe, kaufe ich mir was Süßes.'","","","","wenn ich ins DM gehe (0.90)","","","kaufe ich mir was Süßes (0.95)"
25,"'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout'","","","nach dem Aufstehen (0.95)","","","mach ich ein kurzes HIT Workout (0.95)"
26,"'nach dem Abendbrot wasche ich ab'","","","nach dem Abendbrot (0.95)","","","wasche ich ab (0.94)"
27,"'Nach dem Aufstehen mache ich ein paar Sprachübungen'","","","Nach dem Aufstehen (0.96)","","","mache ich ein paar Sprachübungen (0.95)"
28,"'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe'","","","","wenn ich aus der  WOhnung gehe (0.90)","","","prüfe ob ich meinen Schlüssel dabeihabe (0.92)"
29,"'Ich nehme VItamin D tabletten ein'","","","","","","nehme VItamin D tabletten ein (0.95)"
30,"'Samstags putze ich das Bad.'","Samstags (0.97)","","","","","putze ich das Bad (0.96)"
31,"'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.'","","","wenn es nicht regnet (0.90)","","","gieße ich im Sommer jeden Tag den Apfelbaum (0.96)","im Sommer (0.90)"
32,"'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade'","","","Nach dem Abendbrot (0.95)","","an einem stressigen Tag (0.90)","esse ich gern ein Stück Schokolade (0.96)"
33,"'Nach dem Sport am Abend gehe ich oft meist spät ins Bett'","","","Nach dem Sport am Abend (0.95)","","","gehe ich oft meist spät ins Bett (0.94)"
"""
    llm_dict[
        "Llama-4-Scout-17B-16E-Instruct"
    ].output = """Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens (1.00)","",nach dem Aufstehen (1.00),,"","trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","",,,"","müde bin (1.00)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","",,,"","ein negatives Gefühl stark fühle (1.00)","versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends (1.00)","","nach dem Abendbrot (1.00)",,"","trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","","zum Bäcker gehe (1.00)","am Wochenende (0.80)",,"","mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","","",nach dem Aufstehen (1.00),,"","mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","",,,"","sobald ich eine Aufgabe sehe (0.90)","trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","","in Teams (0.90)","","wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)","","trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","","nach Feierabend (0.80)","","noch niemand daheim erwartet (0.80)","","dann spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.90)","in Dresden (0.80)",,"","","verbringe ich einen Tag mit mir allein (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens (1.00)","","nach dem Aufstehen (1.00)",,"","wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends (0.80)","","nach dem Gesichtwaschen (1.00)",,"","putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends (0.80)","","nach dem Zähneputzen (1.00)",,"","creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens (1.00)","","nach dem Gesicht-Eincremen (1.00)",,"","füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens (1.00)","","nach der Katzenfütterung (1.00)",,"","bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens (1.00)","","nach der Tierfütterung (1.00)",,"","trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","","","nach dem Joggen (1.00)",,"","trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","",,,"","Lust auf ein Bier/Wein habe (1.00)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","","","bevor ich schlafe (0.90)",,"","mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","","","bevor ich schlafen gehe (0.90)",,"","nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","",,,"","gestresst bin (1.00)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","","",nach dem Aufstehen (1.00),,"","mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","Abends (1.00)","","ins Bett lege (0.90)",,"","scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","","ins DM gehe (1.00)",,"","","kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","","",nach dem Aufstehen (1.00),,"","trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout (0.90)"
26,"nach dem Abendbrot wasche ich ab","","","nach dem Abendbrot (1.00)",,"","wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","","",nach dem Aufstehen (1.00),,"","mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  Wohnung gehe","","","wenn ich aus der  Wohnung gehe (0.90)",,"","prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein","",,,"","","nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (1.00)","","",,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","","im Sommer (0.80)","","es nicht regnet (0.90)","","gieße ich jeden Tag den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","","","nach dem Abendbrot (1.00)","","an einem stressigen Tag (0.90)","esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","","am Abend (0.80)","","nach dem Sport (1.00)",,"","gehe ich oft erst spät ins Bett (1.00)"
"""
def evaluate_and_report(llm_dict: dict, true_labels: list, metric_names: String = None):
    if metric_names is None:
        # The default output is the price/performance ratio of F1 and accuracy.
        metric_names = "Embedding"

    # print("\n Start model evaluation and cost-benefit analysis...\n")
    if metric_names == "Embedding":
        for name, model in llm_dict.items():
            predicted_labels=model.parse_output_to_context_labels()
            model.evaluate_with_embedding_similarity(contextual_components,predicted=predicted_labels, gold=true_labels,sim_threshold=0.75)
            model.get_embedding_cost_performance()

    if metric_names == "Substring":
        for name, model in llm_dict.items():
            predicted_labels=model.parse_output_to_context_labels()
            model.evaluate_with_substring_match(contextual_components,predicted=predicted_labels, gold=true_labels)
            model.get_substring_cost_performance()
            # print(Substring Match performance of f"\n{name}:")
            # print(model.substring_metrics)

    if metric_names == "Binary Metric":
        for name, model in llm_dict.items():
            predicted_labels=model.parse_output_to_context_labels()
            model.evaluate_binary_metrics_per_component(contextual_components,predicted=predicted_labels, gold=true_labels)
            model.get_binary_cost_performance()
            # print(f"\nBinary Metric performance of {name}:")
            # print(model.binary_metrics)
            # print(f"Binary Cost Performance: {model.cost_performance}\n")
            
            
def export_llm_infos_to_embedding_excel(llm_dict: dict, filename: str = "llm_metrics.xlsx", preview_output_len: int = 50):
    rows = []
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    for name, model in llm_dict.items():
        try:
            prompt_tokens = model.tokenizer_fn(LLMInfo.input_prompt)
            output_tokens = model.tokenizer_fn(model.output)
        except Exception as e:
            prompt_tokens = -1
            output_tokens = -1
            print(f"[Token Count Error] {model.name}: {e}")

        base_info = {
            "Model Name": model.name,
            "Input Cost / 1M": model.input_cost,
            "Output Cost / 1M": model.output_cost,
            "Prompt Token Count": prompt_tokens,
            "Output Token Count": output_tokens,
            "Total Cost (USD)": round(model.cost, 6),
            "Output Preview": model.output[:preview_output_len].replace("\n", " "),
        }

        component_keys = ["TIME", "PHYSICAL SETTING", "PRIOR BEHAVIOR", "OTHER PEOPLE", "INTERNAL STATE", "BEHAVIOR"]
        if model.embedding_metrics:
            acc_values = []
            for component in component_keys:
                value = model.embedding_metrics.get(component, "N/A")
                base_info[f"{component} Accuracy (Embedding-Based)"] = value
                if isinstance(value, (float, int)):
                    acc_values.append(value)
            mean_acc = round(sum(acc_values) / len(acc_values), 4) if acc_values else "N/A"
            base_info["Mean Accuracy (Embedding-Based)"] = mean_acc

            # Cost-effectiveness metric (based on average accuracy)
            if isinstance(mean_acc, (float, int)) and isinstance(model.cost, (float, int)) and model.cost > 0:
                base_info["Embedding Cost Performance (Mean Accuracy)"] = round(mean_acc / model.cost, 4)
            else:
                base_info["Embedding Cost Performance (Mean Accuracy)"] = "N/A"
        else:
            for component in component_keys:
                base_info[f"{component} Accuracy (Embedding-Based)"] = "N/A"
            base_info["Mean Accuracy (Embedding-Based)"] = "N/A"
            base_info["Embedding Cost Performance (Mean Accuracy)"] = "N/A"
        rows.append(base_info)

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    print(f"Export successful: {filename}")

def export_llm_infos_to_substring_excel(llm_dict: dict, filename: str = "llm_metrics.xlsx", preview_output_len: int = 50):
    """
    Export basic information and substring_metrics of all LLMInfo models to Excel files.
    """
    rows = []
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    for name, model in llm_dict.items():
        try:
            prompt_tokens = model.tokenizer_fn(LLMInfo.input_prompt)
            output_tokens = model.tokenizer_fn(model.output)
        except Exception as e:
            prompt_tokens = -1
            output_tokens = -1
            print(f"[Token Count Error] {model.name}: {e}")

        base_info = {
            "Model Name": model.name,
            "Input Cost / 1M": model.input_cost,
            "Output Cost / 1M": model.output_cost,
            "Prompt Token Count": prompt_tokens,
            "Output Token Count": output_tokens,
            "Total Cost (USD)": round(model.cost, 6),
            "Output Preview": model.output[:preview_output_len].replace("\n", " "),
        }

        component_keys = ["TIME", "PHYSICAL SETTING", "PRIOR BEHAVIOR", "OTHER PEOPLE", "INTERNAL STATE", "BEHAVIOR"]

        # Add the substring value of each component (if any)
        if model.substring_metrics:
            score_values = []
            for component in component_keys:
                value = model.substring_metrics.get(component, "N/A")
                base_info[f"{component} Substring Score"] = value
                if isinstance(value, (float, int)):
                    score_values.append(value)

            # Calculate the average score
            mean_score = round(sum(score_values) / len(score_values), 4) if score_values else "N/A"
            base_info["Mean Substring Score"] = mean_score

            # Adding cost-effectiveness based on averages
            if isinstance(mean_score, (float, int)) and isinstance(model.cost, (float, int)) and model.cost > 0:
                base_info["Substring Cost Performance (Mean Score)"] = round(mean_score / model.cost, 4)
            else:
                base_info["Substring Cost Performance (Mean Score)"] = "N/A"
        else:
            for component in component_keys:
                base_info[f"{component} Substring Score"] = "N/A"
            base_info["Mean Substring Score"] = "N/A"
            base_info["Substring Cost Performance (Mean Score)"] = "N/A"

        rows.append(base_info)

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    print(f"Export successful: {filename}")
    
def export_llm_infos_to_binary_metrics_excel(llm_dict: dict, filename: str = "llm_metrics.xlsx", preview_output_len: int = 50):
    """
    Export basic information and binary_metrics of all LLMInfo models to Excel files.
    """
    rows = []
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    metric_names = ["accuracy", "precision", "recall", "f1", "mcc", "kappa"]
    component_keys = ["TIME", "PHYSICAL SETTING", "PRIOR BEHAVIOR", "OTHER PEOPLE", "INTERNAL STATE", "BEHAVIOR"]

    for name, model in llm_dict.items():
        try:
            prompt_tokens = model.tokenizer_fn(LLMInfo.input_prompt)
            output_tokens = model.tokenizer_fn(model.output)
        except Exception as e:
            prompt_tokens = -1
            output_tokens = -1
            print(f"[Token Count Error] {model.name}: {e}")

        base_info = {
            "Model Name": model.name,
            "Input Cost / 1M": model.input_cost,
            "Output Cost / 1M": model.output_cost,
            "Prompt Token Count": prompt_tokens,
            "Output Token Count": output_tokens,
            "Total Cost (USD)": round(model.cost, 6),
            "Output Preview": model.output[:preview_output_len].replace("\n", " "),
        }

        # Collect the values ​​of each metric to calculate the average
        aggregated_metrics = {metric: [] for metric in metric_names}

        if model.binary_metrics:
            for component in component_keys:
                metrics = model.binary_metrics.get(component, {})
                for metric in metric_names:
                    val = metrics.get(metric, "N/A")
                    # base_info[f"{component} {metric.capitalize()} (Binary)"] = val
                    if isinstance(val, (float, int)):
                        aggregated_metrics[metric].append(val)
        # else:
        #     for component in component_keys:
        #         for metric in metric_names:
        #             base_info[f"{component} {metric.capitalize()} (Binary)"] = "N/A"
        # for metric in metric_names:
        #     values = aggregated_metrics[metric]
        #     if values:
        #         mean_val = round(sum(values) / len(values), 4)
        #         base_info[f"Mean {metric.capitalize()} (Binary)"] = mean_val

        #         if model.cost and isinstance(model.cost, (float, int)) and model.cost > 0:
        #             perf = round(mean_val / model.cost, 4)
        #             base_info[f"Cost Performance - Mean {metric.capitalize()} (Binary)"] = perf
        #         else:
        #             base_info[f"Cost Performance - Mean {metric.capitalize()} (Binary)"] = "N/A"
        #     else:
        #         base_info[f"Mean {metric.capitalize()} (Binary)"] = "N/A"
        #         base_info[f"Cost Performance - Mean {metric.capitalize()} (Binary)"] = "N/A"
        # if model.binary_metrics_cost_performance:
        #     for k, v in model.binary_metrics_cost_performance.items():
        #         base_info[f"Cost Performance - {k}"] = v
        # else:
        #     base_info["Cost Performance - {k}"] = "N/A"
        #     base_info["Cost Performance - {k}"] = "N/A"

        overall = model.binary_metrics.get("__overall__", {})
        for k in ["micro_f1", "macro_f1", "hamming_loss"]:
            val = overall.get(k, "N/A")
            base_info[f"{k}"] = round(val, 4) if isinstance(val, (float, int)) else "N/A"
            if k != "hamming_loss" and isinstance(val, (float, int)) and model.cost and model.cost > 0:
                perf = round(val / model.cost, 4)
                base_info[f"Cost Performance - {k}"] = perf
            elif k != "hamming_loss":
                base_info[f"Cost Performance - {k}"] = "N/A"
        rows.append(base_info)

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    print(f"Export successful: {filename}")


evaluate_and_report(llm_dict, true_labels,metric_names="Embedding")
export_llm_infos_to_embedding_excel(llm_dict, filename="Definition/Embedding_report.xlsx")


evaluate_and_report(llm_dict, true_labels,metric_names="Substring")
export_llm_infos_to_substring_excel(llm_dict, filename="Definition/Substring_report.xlsx")

evaluate_and_report(llm_dict, true_labels,metric_names="Binary Metric")
export_llm_infos_to_binary_metrics_excel(llm_dict, filename="Definition/Binary_Metrics_report.xlsx")