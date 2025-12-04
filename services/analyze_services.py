import os
import requests
from dotenv import load_dotenv

load_dotenv()


labels = [
  "politique",
  "économie",
  "technologie",
  "science",
  "santé",
  "écologie",
  "éducation",
  "sport",
  "culture",
  "faits divers",
  "international",
  "société"
]


API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
}
    
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()



def classifier_zero_shot(text , labels):
    try:
        if not text.strip():
            raise ValueError("Le texte ne peut pas être vide.")
        
        output = query({
                "inputs": text,
                "parameters": {"candidate_labels": labels},
            })
        
        return output
    
    # si le text est vide
    except ValueError as ve:
        return f'erreur de donnees : {ve}'
    
    # erreur de connexion
    except ConnectionError:
        return 'erreur de connexion'
    
    # erreur inattendue
    except Exception as e :
        return f'erreur {e}'
    