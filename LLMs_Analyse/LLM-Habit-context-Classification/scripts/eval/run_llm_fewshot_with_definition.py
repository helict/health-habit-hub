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

Here are our 4 examples (few-shot examples) to illustrate the expected format and level of detail.:

Example 1:

Input: "Immer wenn ich müde bin, mache ich Atemübungen."

Output: 1,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)" 

Example 2:

Input: "Abends nach dem Abendbrot trinke ich ein Glas Wein."

Output: 1,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"

Example 3:

Input: "Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino."

Output: 1,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"

Example 4:

Input: "Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein."

Output: 1,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe",,,"trage ich sie in Notion ein (1.00)"

Now, please process the following list of sentences:


['Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.', 'Immer wenn ich müde bin, mache ich Atemübungen. ', 'Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen. ', 'Abends nach dem Abendbrot trinke ich ein Glas Wein. ', 'Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino. ', 'Nach dem Aufstehen mache ich Kraftsport', 'Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein. ', 'Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei. ', 'Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause. ', 'Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden. ', 'Morgens nach dem Aufstehen wasche ich mein Gesicht.', 'Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.', 'Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.', 'Morgens nach dem Gesicht-Eincremen füttere ich die Katze.', 'Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.', 'Morgens nach der Tierfütterung trinke ich einen Kaffee.', 'Nach dem Joggen trinke ich einen Proteinshake.', 'Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier', 'Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.', 'Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel', 'Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.', 'Nach dem Aufstehen mache ich mir ein Zitronenwasser.', 'Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.', 'wenn ich ins DM gehe, kaufe ich mir was Süßes.', 'nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout', 'nach dem Abendbrot wasche ich ab', 'Nach dem Aufstehen mache ich ein paar Sprachübungen', 'Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe', 'Ich nehme VItamin D tabletten ein', 'Samstags putze ich das Bad.', 'Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.', 'Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade', 'Nach dem Sport am Abend gehe ich oft erst spät ins Bett ']"""
    )

    llm_dict[
        "gpt4.1"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.97)",,,,"","trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,"ich ein negatives Gefühl stark fühle (0.95)","versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport",,"","Nach dem Aufstehen (0.97)",,,"mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.95)",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.80)","dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)",,"trete ich dem Meeting bei (0.98)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.85)",,,"noch niemand daheim erwartet (0.85)",,"spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.95)","in Dresden (0.90)",,,"mit mir allein (0.90)","verbringe ich einen Tag (0.98)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.97)",,,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.96)",,,"nach dem Gesichtwaschen (0.97)",,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.96)",,,"nach dem Zähneputzen (0.97)",,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.95)",,,"nach dem Gesicht-Eincremen (0.96)",,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.95)",,,"nach der Katzenfütterung (0.97)",,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.95)",,,"nach der Tierfütterung (0.97)",,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake",,,"Nach dem Joggen (0.97)",,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"ich Lust auf ein Bier/Wein habe (0.90)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.91)",,,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.91)",,,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,,"Nach dem Aufstehen (0.97)",,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","mich abends ins Bett lege (0.88)",,"Wenn ich mich abends ins Bett lege (0.92)",,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM gehe (0.93)","wenn ich ins DM gehe (0.95)",,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.93)",,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.98)",,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.97)",,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der  WOhnung gehe (0.93)",,"prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.98)",,"",,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.90)","den Apfelbaum (0.90)","Wenn es nicht regnet (0.85)",,"gieße ich den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","an einem stressigen Tag (0.92)",,,"Nach dem Abendbrot (0.98)",,"esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.85)",,,"Nach dem Sport (0.93)",,"gehe ich oft erst spät ins Bett (1.00)"
"""

    llm_dict[
        "gpt4.1 mini"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.97)",,,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,, "ich ein negatives Gefühl stark fühle (0.90)","versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport",,"", "Nach dem Aufstehen (0.95)",,, "mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.83)","dass sich ein Kollege im EvalGiGe Meeting befindet (0.82)",,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.80)",,,"noch niemand daheim erwartet (0.78)","nach Feierabend noch niemand daheim erwartet (0.80)","spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.93)","in Dresden (0.90)",,,"mit mir allein (0.90)","verbringe ich einen Tag (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.97)",,,"nach dem Aufstehen (0.90)",, "wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.92)",,,"nach dem Gesichtwaschen (0.98)",, "putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.92)",,,"nach dem Zähneputzen (0.98)",, "creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.96)",,,"nach dem Gesicht-Eincremen (0.97)",, "füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.93)",,,"nach der Katzenfütterung (0.97)",, "bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.92)",,,"nach der Tierfütterung (0.95)",, "trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,,"Nach dem Joggen (0.99)",,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,"Wenn ich Lust auf ein Bier/Wein habe (0.98)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.97)",,,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.97)",,,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.97)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,,"Nach dem Aufstehen (0.95)",,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.80)","ins Bett (0.84)","Wenn ich mich ins Bett lege (0.93)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM gehe (0.97)","wenn ich ins DM gehe (0.97)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.92)",,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.98)",,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.95)",,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der  WOhnung gehe (0.85)",,,"Ich prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"Ich nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.98)",,,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.83)",,"Wenn es nicht regnet (0.96)",,, "gieße ich den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.84)",,,"Nach dem Abendbrot an einem stressigen Tag (0.84)",, "esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.85)",,"Nach dem Sport (0.97)",,, "gehe ich oft erst spät ins Bett (1.00)"
"""

    llm_dict[
        "o3"
    ].output = """Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.98)",,,,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,"ich ein negatives Gefühl stark fühle (0.91)","versuche ich es auszufühlen (0.98)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)",,,,,"mache ich Kraftsport (0.99)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.93)",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,,"dass sich ein Kollege im EvalGiGe Meeting befindet (0.94)","mir in Teams angezeigt wird (0.88)","trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.95)","","","","noch niemand daheim erwartet (0.89)","spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.95)","in Dresden (0.91)",,,,"verbringe ich einen Tag mit mir allein (0.93)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.98)",,,,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.95)",,,,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.94)",,,,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.92)",,,,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.91)",,,,,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.91)",,,,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.90)",,,,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"ich Lust auf ein Bier/Wein habe (0.91)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.90)",,,,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.93)",,,,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.98)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)",,,,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","ich mich abends ins Bett lege (0.93)",,,,"","scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,,"wenn ich ins DM gehe (0.91)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen trinken und Medikamenteinnahme (0.89)",,,,,"mach ich ein kurzes HIT Workout (0.99)"
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.97)",,,,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)",,,,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der  WOhnung gehe (0.93)",,,"Ich prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"Ich nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.95)",,,,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.93)","den Apfelbaum (0.85)",,,,"gieße ich den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot (0.91)",,,"an einem stressigen Tag (0.84)",,"esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.94)",,,,,"gehe ich oft erst spät ins Bett (0.99)"
"""

    llm_dict[
        "o4 mini (High Effort)"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.96)",,,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,"ich ein negatives Gefühl stark fühle (0.93)","versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport",,"", "Nach dem Aufstehen (0.97)",,,, "mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.98)",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,,"dass sich ein Kollege im EvalGiGe Meeting befindet (0.94)",,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.92)","","noch niemand daheim erwartet (0.92)",,"spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.98)","in Dresden (0.96)",,,"mit mir allein (0.94)","verbringe ich einen Tag (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.96)",,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.94)",,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.94)",,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.93)",,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.93)",,,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.93)",,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,"","Nach dem Joggen (0.96)",,, "trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"ich Lust auf ein Bier/Wein habe (0.92)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.97)",,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","ich mich abends ins Bett lege (0.90)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,,"wenn ich ins DM gehe (0.92)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.93)",,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.96)",,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen.","Nach dem Aufstehen (0.97)",,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der Wohnung gehe (0.97)",,,"prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (1.00)",,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.90)","den Apfelbaum (0.80)",,"es nicht regnet (0.90)",,"gieße ich den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.92)",,,,"an einem stressigen Tag (0.95)","esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.95)",,,"gehe ich oft erst spät ins Bett (1.00)"
"""

    llm_dict[
        "o3 mini (High Effort)"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.97)",,,,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,, "ich ein negatives Gefühl stark fühle (0.95)","versuche ich es auszufühlen (0.98)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.93)",,,,,"mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.95)",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)","Kollege im EvalGiGe Meeting (0.88)",,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.87)",,"noch niemand daheim erwartet (0.80)",,"","spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.94)","in Dresden (0.90)",,,"mit mir allein (0.70)","verbringe ich einen Tag (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.97)",,,,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.92)",,,,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.92)",,,,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.93)",,,,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.93)",,,,,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.93)",,,,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,"","Nach dem Joggen (0.96)",,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"ich Lust auf ein Bier/Wein habe (0.90)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.92)",,,,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.92)",,,,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (0.98)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.93)",,,,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.80)","ins Bett (0.88)","Wenn ich mich abends ins Bett lege (0.90)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM gehe (0.85)","wenn ich ins DM gehe (0.95)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,"","nach dem Aufstehen trinken und Medikamenteinnahme (0.89)",,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab",,"","nach dem Abendbrot (0.97)",,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.93)",,,,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der  WOhnung gehe (0.93)",,,"prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.98)",,,,"","putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.80)","","Wenn es nicht regnet (0.87)",,,"gieße ich den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.90)",,,"","an einem stressigen Tag (0.87)","esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.85)",, "Nach dem Sport (0.90)",,,"gehe ich oft erst spät ins Bett (0.98)"
"""

    llm_dict[
        "GPT-4o mini"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.98)",,,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,, "ein negatives Gefühl stark fühle (0.95)","versuche ich es auszufühlen (0.95)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport",,"", "Nach dem Aufstehen (0.97)",,,"mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe (0.95)",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)","dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)",,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.85)","nach Hause (0.70)",, "noch niemand daheim erwartet (0.85)",,"spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.90)","in Dresden (0.95)",,,"mit mir allein (0.90)","verbringe ich einen Tag (0.95)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.97)",,,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.93)",,,"nach dem Gesichtwaschen (0.97)",,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.93)",,,"nach dem Zähneputzen (0.97)",,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.93)",,,"nach dem Gesicht-Eincremen (0.97)",,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.93)",,,"nach der Katzenfütterung (0.97)",,,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.93)",,,"nach der Tierfütterung (0.97)",,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,,"Nach dem Joggen (0.97)",,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,"Lust auf ein Bier/Wein habe (0.92)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.97)",,,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.97)",,,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.95)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.",,,"Nach dem Aufstehen (0.97)",,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.80)","ins Bett (0.80)","Wenn ich mich abends ins Bett lege (0.90)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM gehe (0.90)","wenn ich ins DM gehe (0.95)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,,"nach dem Aufstehen trinken und Medikamenteinnahme (0.96)",,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab",,,"nach dem Abendbrot (0.97)",,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,,"Nach dem Aufstehen (0.97)",,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  Wohnung gehe",,,"wenn ich aus der  Wohnung gehe (0.95)",,,"Ich prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"Ich nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (1.00)",,,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.",,"im Sommer (0.89)","Wenn es nicht regnet (0.91)",,,"gieße ich jeden Tag den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.94)",,,"Nach dem Abendbrot an einem stressigen Tag (0.96)",,,"esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.85)",,"Nach dem Sport (0.97)",,,"gehe ich oft erst spät ins Bett (1.00)"
"""

    llm_dict[
        "GPT-4o"
    ].output = """Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.97)",,,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.",,,,,"ich ein negatives Gefühl stark fühle (0.92)","versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport",,"nach dem Aufstehen (0.95)",,,,,"mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.",,,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.87)","dass sich ein Kollege im EvalGiGe Meeting befindet (0.85)",,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","nach Feierabend (0.94)","zu Hause (0.80)",,,"noch niemand daheim erwartet (0.80)","spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.98)","in Dresden (0.93)",,,"mit mir allein (0.90)","verbringe ich einen Tag (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.97)",,,"nach dem Aufstehen (0.95)",,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.95)",,,"nach dem Gesichtwaschen (1.00)",,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.95)",,,"nach dem Zähneputzen (1.00)",,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.94)",,,"nach dem Gesicht-Eincremen (0.97)",,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.90)",,,"nach der Katzenfütterung (0.97)","der Hund (0.85)",,"bekommt der Hund eine Kaustange (0.95)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.93)",,,"nach der Tierfütterung (0.96)",,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.",,"nach dem Joggen (1.00)",,,,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier",,,,,"ich Lust auf ein Bier/Wein habe (0.92)","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.89)",,,,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.90)",,,,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.",,,,,"ich gestresst bin (0.97)","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser",,"nach dem Aufstehen (0.95)",,,,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","abends (0.76)","im Bett (0.80)","Wenn ich mich...ins Bett lege (0.82)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.",,"ins DM gehe (0.90)",,,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout",,"nach dem Aufstehen trinken und Medikamenteinnahme (0.85)",,,,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab",,"nach dem Abendbrot (0.95)",,,,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen",,"nach dem Aufstehen (0.95)",,,,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der  WOhnung gehe",,,"wenn ich aus der  WOhnung gehe (0.84)",,,,"prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein",,,,,,"nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.99)",,,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","im Sommer jeden Tag (0.92)","den Apfelbaum (0.75)","Wenn es nicht regnet (0.97)",,,"gieße ich...den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.87)",,,"Nach dem Abendbrot (0.92)",,"an einem stressigen Tag (0.88)","esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","am Abend (0.85)",,"Nach dem Sport (0.95)",,,"gehe ich oft erst spät ins Bett (1.00)"
"""

    llm_dict[
        "DeepSeek-Coder-V2-Lite-Instruct"
    ].output = """ ```csv
Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)",,"trinke ich direkt einen Kafffe (1.00)",,,
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","Wenn ich ein negatives Gefühl (0.90)",,,"versuche ich es auszufühlen (1.00)",,
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,"trinke ich ein Glas Wein (1.00)",,
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)",,"zum Bäcker gehe, mache ich einen Abstecher (0.85)",,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)",,,"mache ich Kraftsport (1.00)",,
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.",,,"Sobald ich eine Aufgabe sehe",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","Wenn mir in Teams (0.85)",,"dass sich ein Kollege im EvalGiGe Meeting befindet",,"trete ich dem Meeting bei (1.00)",
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","Wenn mich nach Feierabend (0.85)",,,"spaziere ich nach Hause (1.00)",,
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.80)",,"verbringe ich einen Tag mit mir allein in Dresden (1.00)",,
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)",,"wasche ich mein Gesicht (1.00)",,
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.95)",,"putze ich meine Zähne (1.00)",,
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.95)",,"creme ich mein Gesicht ein (1.00)",,
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.90)",,"füttere ich die Katze (1.00)",,
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.90)",,"bekommt der Hund eine Kaustange (1.00)",,
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.90)",,,"trinke ich einen Kaffee (1.00)",,
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.90)",,,"trinke ich einen Proteinshake (1.00)",,
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","Wenn ich Lust auf ein Bier/Wein (0.85)",,,"trinke ich ein Malzbier (1.00)",,
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.90)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)",,
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen (0.90)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)",,
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","Wenn ich gestresst bin (0.90)",,"gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)",,
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)",,,"mache ich mir ein Zitronenwasser (1.00)",,
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","Wenn ich mich abends ins Bett lege (0.95)",,,"scrolle ich sinnlos durch social media (1.00)",,
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","wenn ich ins DM gehe (0.85)",,,"kaufe ich mir was Süßes (1.00)",,
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen (0.95)",,"trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout (1.00)",,
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.95)",,,"wasche ich ab (1.00)",,
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)",,,"mache ich ein paar Sprachübungen (1.00)",,
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe","Ich prüfe ob ich meinen Schlüssel dabeihabe (0.85)",,,"aus der WOhnung gehe (1.00)",,
29,"Ich nehme VItamin D tabletten ein","Ich nehme VItamin D tabletten ein (0.90)",,,"nehme VItamin D tabletten ein (1.00)",,
30,"Samstags putze ich das Bad.","Samstags (0.85)",,,"putze ich das Bad (1.00)",,
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","Wenn es nicht regnet (0.85)",,,"gieße ich im Sommer jeden Tag den Apfelbaum (1.00)",,
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot (0.95)",,"an einem stressigen Tag esse ich gern ein Stück Schokolade (1.00)",,
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.90)",,,"gehe ich oft erst spät ins Bett (1.00)",,
```
"""
    llm_dict[
        "DeepSeek-R1"
    ].output = """ ```csv
Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)",,"","","trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","","","Immer wenn ich müde bin",,,"mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","Wenn ich ein negatives Gefühl stark fühle",,,"","versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,"","","trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)",,"zum Bäcker gehe, mache ich einen Abstecher (0.85)",,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)",,"","","mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","Sobald ich eine Aufgabe sehe",,,"","trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","Wenn mir in Teams angezeigt wird",,"dass sich ein Kollege im EvalGiGe Meeting befindet",,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","Wenn mich nach Feierabend noch niemand daheim erwartet",,,"","spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat",,"","","verbringe ich einen Tag mit mir allein in Dresden (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)",,"","","wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.90)",,"","","putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.90)",,"","","creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.90)",,"","","füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.90)",,"","","bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.90)",,"","","trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.95)",,"","","trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","Wenn ich Lust auf ein Bier/Wein habe (0.90)",,"","","trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)",,"","","mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)",,"","","nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","Wenn ich gestresst bin",,"","","gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)",,"","","mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","Wenn ich mich abends ins Bett lege (0.95)",,"","","scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","wenn ich ins DM gehe (0.90)",,"","","kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen (0.95)",,"","","trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.97)",,"","","wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)",,"","","mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe","Ich prüfe ob ich meinen Schlüssel dabeihabe",,"wenn ich aus der WOhnung gehe",,"(1.00)"
29,"Ich nehme VItamin D tabletten ein","Ich nehme VItamin D tabletten ein (0.95)",,"","","(1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.95)",,"","","putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","Wenn es nicht regnet",,"","","gieße ich im Sommer jeden Tag den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.95)",,"","","esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.95)",,"","","gehe ich oft erst spät ins Bett (1.00)"
```
"""

    llm_dict[
        "Llama-3.3-70B-Instruct"
    ].output = """ ```csv
Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)",,"trinke ich direkt einen Kafffe (1.00)",,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","Wenn ich ein negatives Gefühl stark fühle (0.90)",,,"versuche ich es auszufühlen (1.00)",,
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,"trinke ich ein Glas Wein (1.00)",,
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)",,,"mache ich Kraftsport (1.00)",,
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","Sobald ich eine Aufgabe sehe",,,"trage ich sie in Notion ein (1.00)",,
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.80)",,,"dann trete ich dem Meeting bei (1.00)",,
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","Wenn mich nach Feierabend noch niemand daheim erwartet (0.85)",,,"dann spaziere ich nach Hause (1.00)",,
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.90)",,"verbringe ich einen Tag mit mir allein in Dresden (1.00)",,,"verbringe ich einen Tag mit mir allein in Dresden (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)",,,"wasche ich mein Gesicht (1.00)",,
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.95)",,,"putze ich meine Zähne (1.00)",,
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.95)",,,"creme ich mein Gesicht ein (1.00)",,
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.95)",,,"füttere ich die Katze (1.00)",,
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.95)",,,"bekommt der Hund eine Kaustange (1.00)",,
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.95)",,,"trinke ich einen Kaffee (1.00)",,
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.95)",,,"trinke ich einen Proteinshake (1.00)",,
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","Wenn ich Lust auf ein Bier/Wein habe (0.90)",,,"trinke ich ein Malzbier (1.00)",,
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)",,
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)",,
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","Wenn ich gestresst bin (0.90)",,,"gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)",,
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)",,,"mache ich mir ein Zitronenwasser (1.00)",,
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","Wenn ich mich abends ins Bett lege (0.95)",,,"scrolle ich sinnlos durch social media (1.00)",,
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","wenn ich ins DM gehe (0.90)",,,"kaufe ich mir was Süßes (1.00)",,
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen trinken und Medikamenteinnahme (0.95)",,,"mach ich ein kurzes HIT Workout (1.00)",,
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.95)",,,"wasche ich ab (1.00)",,
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)",,,"mache ich ein paar Sprachübungen (1.00)",,
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe","Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe (0.85)",,,"prüfe ob ich meinen Schlüssel dabeihabe (1.00)",,
29,"Ich nehme VItamin D tabletten ein","Ich nehme VItamin D tabletten ein (0.95)",,,"nehme VItamin D tabletten ein (1.00)",,
30,"Samstags putze ich das Bad.","Samstags (0.90)",,,"putze ich das Bad (1.00)",,
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum (0.85)",,,"gieße ich im Sommer jeden Tag den Apfelbaum (1.00)",,
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.90)",,,"esse ich gern ein Stück Schokolade (1.00)",,
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.95)",,,"gehe ich oft erst spät ins Bett (1.00)",,
```
"""


    llm_dict[
        "gpt-oss-120b"
    ].output = """ ```csv
Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)",,"trinke ich direkt einen Kafffe (1.00)",,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.",,,,,"ich müde bin (0.95)","mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","Wenn ich ein negatives Gefühl stark fühle (0.90)",,,"versuche ich es auszufühlen (1.00)",,
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,,"trinke ich ein Glas Wein (1.00)",,
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe, mache ich einen Abstecher (0.85)",,,"trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)",,,"mache ich Kraftsport (1.00)",,
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","Sobald ich eine Aufgabe sehe",,,"trage ich sie in Notion ein (1.00)",,
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)",,,"dann trete ich dem Meeting bei (1.00)",,
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","Wenn mich nach Feierabend noch niemand daheim erwartet (0.90)",,,"dann spaziere ich nach Hause (1.00)",,
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.90)",,"verbringe ich einen Tag mit mir allein in Dresden (1.00)",,,"verbringe ich einen Tag mit mir allein in Dresden (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)",,"wasche ich mein Gesicht (1.00)",,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.95)",,,"putze ich meine Zähne (1.00)",,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.95)",,,"creme ich mein Gesicht ein (1.00)",,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.95)",,,"füttere ich die Katze (1.00)",,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.95)",,,"bekommt der Hund eine Kaustange (1.00)",,,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.95)",,,"trinke ich einen Kaffee (1.00)",,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.95)",,,"trinke ich einen Proteinshake (1.00)",,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","Wenn ich Lust auf ein Bier/Wein habe (0.90)",,,"trinke ich ein Malzbier (1.00)",,,"trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","Wenn ich gestresst bin (0.90)",,"gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)",,,"gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)",,,"mache ich mir ein Zitronenwasser (1.00)",,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","Wenn ich mich abends ins Bett lege (0.95)",,,"scrolle ich sinnlos durch social media (1.00)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","wenn ich ins DM gehe (0.90)",,,"kaufe ich mir was Süßes (1.00)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen trinken und Medikamenteinnahme (0.90)",,,"mach ich ein kurzes HIT Workout (1.00)",,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.95)",,,"wasche ich ab (1.00)",,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)",,,"mache ich ein paar Sprachübungen (1.00)",,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe","Ich prüfe ob ich meinen Schlüssel dabeihabe (0.90)",,,"wenn ich aus der WOhnung gehe (1.00)",,,"Ich prüfe ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein","Ich nehme VItamin D tabletten ein (0.95)",,,"nehme VItamin D tabletten ein (1.00)",,,"nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.90)",,,"putze ich das Bad (1.00)",,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","Wenn es nicht regnet (0.90)",,,"gieße ich im Sommer jeden Tag den Apfelbaum (1.00)",,,"gieße ich im Sommer jeden Tag den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.90)",,,"esse ich gern ein Stück Schokolade (1.00)",,,"esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.95)",,,"gehe ich oft erst spät ins Bett (1.00)",,,"gehe ich oft erst spät ins Bett (1.00)"
```
"""

    llm_dict[
        "Llama-4-Scout-17B-16E-Instruct"
    ].output = """ ```csv
Number,"Original Sentence","TIME (conf.)","PHYSICAL SETTING (conf.)","PRIOR BEHAVIOR (conf.)","OTHER PEOPLE (conf.)","INTERNAL STATE (conf.)","BEHAVIOR (conf.)"
1,"Morgens nach dem Aufstehen trinke ich direkt einen Kafffe.","Morgens nach dem Aufstehen (0.95)",,"trinke ich direkt einen Kafffe (1.00)",,,"trinke ich direkt einen Kafffe (1.00)"
2,"Immer wenn ich müde bin, mache ich Atemübungen.","Immer wenn ich müde bin (0.95)",,,"müde bin (0.95)",,"mache ich Atemübungen (1.00)"
3,"Wenn ich ein negatives Gefühl stark fühle, versuche ich es auszufühlen.","Wenn ich ein negatives Gefühl stark fühle (0.95)",,,"ein negatives Gefühl stark fühle (0.95)",,"versuche ich es auszufühlen (1.00)"
4,"Abends nach dem Abendbrot trinke ich ein Glas Wein.","Abends nach dem Abendbrot (0.97)",,"trinke ich ein Glas Wein (1.00)",,,"trinke ich ein Glas Wein (1.00)"
5,"Wenn ich am Wochenende zum Bäcker gehe, mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino.","Wenn ich am Wochenende zum Bäcker gehe (0.90)","in mein Lieblingscafe (0.85)","zum Bäcker gehe (0.85)",,,"mache ich einen Abstecher in mein Lieblingscafe und trinke einen Cappucino (1.00)"
6,"Nach dem Aufstehen mache ich Kraftsport","Nach dem Aufstehen (0.95)",,"mache ich Kraftsport (1.00)",,,"mache ich Kraftsport (1.00)"
7,"Sobald ich eine Aufgabe sehe, trage ich sie in Notion ein.","Sobald ich eine Aufgabe sehe (0.95)",,,"eine Aufgabe sehe (0.95)",,,"trage ich sie in Notion ein (1.00)"
8,"Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet, dann trete ich dem Meeting bei.","Wenn mir in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)",,,"in Teams angezeigt wird, dass sich ein Kollege im EvalGiGe Meeting befindet (0.90)",,,"trete ich dem Meeting bei (1.00)"
9,"Wenn mich nach Feierabend noch niemand daheim erwartet, dann spaziere ich nach Hause.","Wenn mich nach Feierabend noch niemand daheim erwartet (0.90)",,,"nach Feierabend noch niemand daheim erwartet (0.90)",,,"spaziere ich nach Hause (1.00)"
10,"Einmal im Monat verbringe ich einen Tag mit mir allein in Dresden.","Einmal im Monat (0.90)",,"verbringe ich einen Tag mit mir allein in Dresden (1.00)",,,"verbringe ich einen Tag mit mir allein in Dresden (1.00)"
11,"Morgens nach dem Aufstehen wasche ich mein Gesicht.","Morgens nach dem Aufstehen (0.95)",,"wasche ich mein Gesicht (1.00)",,,"wasche ich mein Gesicht (1.00)"
12,"Morgens/Abends nach dem Gesichtwaschen putze ich meine Zähne.","Morgens/Abends nach dem Gesichtwaschen (0.95)",,"putze ich meine Zähne (1.00)",,,"putze ich meine Zähne (1.00)"
13,"Morgens/Abends nach dem Zähneputzen creme ich mein Gesicht ein.","Morgens/Abends nach dem Zähneputzen (0.95)",,"creme ich mein Gesicht ein (1.00)",,,"creme ich mein Gesicht ein (1.00)"
14,"Morgens nach dem Gesicht-Eincremen füttere ich die Katze.","Morgens nach dem Gesicht-Eincremen (0.95)",,"füttere ich die Katze (1.00)",,,"füttere ich die Katze (1.00)"
15,"Morgens nach der Katzenfütterung bekommt der Hund eine Kaustange.","Morgens nach der Katzenfütterung (0.95)",,"bekommt der Hund eine Kaustange (1.00)",,,"bekommt der Hund eine Kaustange (1.00)"
16,"Morgens nach der Tierfütterung trinke ich einen Kaffee.","Morgens nach der Tierfütterung (0.95)",,"trinke ich einen Kaffee (1.00)",,,"trinke ich einen Kaffee (1.00)"
17,"Nach dem Joggen trinke ich einen Proteinshake.","Nach dem Joggen (0.95)",,,"trinke ich einen Proteinshake (1.00)",,,"trinke ich einen Proteinshake (1.00)"
18,"Wenn ich Lust auf ein Bier/Wein habe trinke ich ein Malzbier","Wenn ich Lust auf ein Bier/Wein habe (0.95)",,,"Lust auf ein Bier/Wein habe (0.95)",,,"trinke ich ein Malzbier (1.00)"
19,"Bevor ich schlafe mache ich meine Ohrstöpsel ins Ohr.","Bevor ich schlafe (0.95)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)",,,"mache ich meine Ohrstöpsel ins Ohr (1.00)"
20,"Bevor ich schlafen gehe nehme ich meine Nahrungsergänzungsmittel","Bevor ich schlafen gehe (0.95)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)",,,"nehme ich meine Nahrungsergänzungsmittel (1.00)"
21,"Wenn ich gestresst bin, gehe ich zum Kühlschrank und nehme mir etwas zu essen.","Wenn ich gestresst bin (0.95)",,,"gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)",,,"gehe ich zum Kühlschrank und nehme mir etwas zu essen (1.00)"
22,"Nach dem Aufstehen mache ich mir ein Zitronenwasser.","Nach dem Aufstehen (0.95)",,,"mache ich mir ein Zitronenwasser (1.00)",,,"mache ich mir ein Zitronenwasser (1.00)"
23,"Wenn ich mich abends ins Bett lege, scrolle ich sinnlos durch social media.","Wenn ich mich abends ins Bett lege (0.95)",,,"scrolle ich sinnlos durch social media (1.00)",,,"scrolle ich sinnlos durch social media (1.00)"
24,"wenn ich ins DM gehe, kaufe ich mir was Süßes.","wenn ich ins DM gehe (0.95)",,,"kaufe ich mir was Süßes (1.00)",,,"kaufe ich mir was Süßes (1.00)"
25,"nach dem Aufstehen trinken und Medikamenteinnahme mach ich ein kurzes HIT Workout","nach dem Aufstehen trinken und Medikamenteinnahme (0.95)",,,"mach ich ein kurzes HIT Workout (1.00)",,,"mach ich ein kurzes HIT Workout (1.00)"
26,"nach dem Abendbrot wasche ich ab","nach dem Abendbrot (0.97)",,,"wasche ich ab (1.00)",,,"wasche ich ab (1.00)"
27,"Nach dem Aufstehen mache ich ein paar Sprachübungen","Nach dem Aufstehen (0.95)",,,"mache ich ein paar Sprachübungen (1.00)",,,"mache ich ein paar Sprachübungen (1.00)"
28,"Ich prüfe ob ich meinen Schlüssel dabeihabe, wenn ich aus der WOhnung gehe","Ich prüfe ob ich meinen Schlüssel dabeihabe (0.95)",,,"aus der WOhnung gehe (0.95)",,,"prüfe ich ob ich meinen Schlüssel dabeihabe (1.00)"
29,"Ich nehme VItamin D tabletten ein","Ich nehme VItamin D tabletten ein (0.95)",,,"nehme VItamin D tabletten ein (0.95)",,,"nehme VItamin D tabletten ein (1.00)"
30,"Samstags putze ich das Bad.","Samstags (0.90)",,,"putze ich das Bad (1.00)",,,"putze ich das Bad (1.00)"
31,"Wenn es nicht regnet, gieße ich im Sommer jeden Tag den Apfelbaum.","Wenn es nicht regnet (0.95)",,,"gieße ich im Sommer jeden Tag den Apfelbaum (1.00)",,,"gieße ich im Sommer jeden Tag den Apfelbaum (1.00)"
32,"Nach dem Abendbrot an einem stressigen Tag esse ich gern ein Stück Schokolade","Nach dem Abendbrot an einem stressigen Tag (0.95)",,,"esse ich gern ein Stück Schokolade (1.00)",,,"esse ich gern ein Stück Schokolade (1.00)"
33,"Nach dem Sport am Abend gehe ich oft erst spät ins Bett","Nach dem Sport am Abend (0.95)",,,"gehe ich oft erst spät ins Bett (1.00)",,,"gehe ich oft erst spät ins Bett (1.00)"
```
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
export_llm_infos_to_embedding_excel(llm_dict, filename="FewshotwithDefinition/Embedding_report.xlsx")


evaluate_and_report(llm_dict, true_labels,metric_names="Substring")
export_llm_infos_to_substring_excel(llm_dict, filename="FewshotwithDefinition/Substring_report.xlsx")

evaluate_and_report(llm_dict, true_labels,metric_names="Binary Metric")
export_llm_infos_to_binary_metrics_excel(llm_dict, filename="FewshotwithDefinition/Binary_Metrics_report.xlsx")