# test.py
import requests

API_URL = "http://localhost:8000/segment/"

def test_habit(input_data):
    response = requests.post(API_URL, json=input_data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    # Test with an English sentence.
    test_data_en = {
        "donor_id": 1,
        "text": "In the morning after I wake up I go to the bathroom and brush my teeth.",
        "lang": "en",
        "source": "user"
    }
    print("Testing English Input:")
    test_habit(test_data_en)
    
    # Test with a German sentence.
    test_data_de = {
        "donor_id": 2,
        "text": "Am Morgen nachdem ich aufgewacht bin gehe ich ins Badezimmer und putze meine Zähne.",
        "lang": "de",
        "source": "user"
    }
    print("\nTesting German Input:")
    test_habit(test_data_de)