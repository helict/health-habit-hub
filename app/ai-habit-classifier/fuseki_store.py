# fuseki_store.py
import requests

# Update the endpoint to match your Fuseki configuration.
FUSEKI_UPDATE_URL = "http://localhost:3030/hhh/update"

def store_donation_fuseki(donor_id: int, language: str, source: str, sentence: str, parts: list):
    """
    Stores a donation in Fuseki as an instance of hhh:Donor with associated parts.
    Each part is mapped to a class based on its domain and linked using:
      - hhh:hasBehavior (for Habit parts)
      - hhh:hasContext (for all other parts)
    """
    # Mapping from classifier domain to RDF class from your schema.
    domain_mapping = {
        "Habit": "hhh:Behavior",
        "Time": "hhh:TimeReference",
        "Prior Behavior": "hhh:RelatedBehavior",
        "Inner State": "hhh:InternalState",
        "People": "hhh:People",
        "Location": "hhh:PhysicalSetting",
        "Other": "hhh:Context"
    }
    
    triples = f"""
    PREFIX hhh: <http://example.com/hhh#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    INSERT DATA {{
      hhh:Donor{donor_id} rdf:type hhh:Donor ;
         hhh:language "{language}" ;
         hhh:source "{source}" ;
         hhh:sentence "{sentence}" .
    """
    for idx, part in enumerate(parts):
        part_resource = f"hhh:Part{donor_id}_{idx}"
        part_class = domain_mapping.get(part["domain"], "hhh:Context")
        relation = "hhh:hasBehavior" if part["domain"] == "Habit" else "hhh:hasContext"
        triples += f"""
         hhh:Donor{donor_id} {relation} {part_resource} .
         {part_resource} rdf:type {part_class} ;
                      hhh:value "{part['phrase']}" .
        """
    triples += "\n}"
    response = requests.post(FUSEKI_UPDATE_URL, data={"update": triples})
    return response.status_code

if __name__ == "__main__":
    # Test the Fuseki insertion with sample data.
    donor_id = 12345
    language = "en"
    source = "user"
    sentence = "In the morning after I wake up I go to the bathroom and brush my teeth."
    parts = [
        {"phrase": "In the morning", "domain": "Time"},
        {"phrase": "after I wake up", "domain": "Prior Behavior"},
        {"phrase": "I go to the bathroom and brush my teeth", "domain": "Habit"}
    ]
    status = store_donation_fuseki(donor_id, language, source, sentence, parts)
    print("Fuseki update status:", status)