from utils.markdown_to_json import text_markdown_json
from db.models.analysis_logs import AnalysisLogs
import os
import requests
from google import genai    
from dotenv import load_dotenv
from utils.markdown_to_json import text_markdown_json
from db.models.analysis_logs import AnalysisLogs


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


# remarque : l'output de cette fonction donne un tableau des objet classifier par score en ordre decroissant
def classifier_zero_shot(text):
    try:
        if not text.strip():
            raise ValueError("Le texte ne peut pas être vide.")
        
        output = query({
                "inputs": text,
                "parameters": {"candidate_labels": labels},
            })
        
        return output[0] 
    
    # si le text est vide
    except ValueError as ve:
        return f'erreur de donnees : {ve}'
    
    # erreur de connexion
    except ConnectionError:
        return 'erreur de connexion'
    
    # erreur inattendue
    except Exception as e :
        return f'erreur {e}'

print(classifier_zero_shot('Le nouveau iPhone sort demain.'))

API_KEY_GEMINI = os.getenv('API_KEY_GEMINI')


# create prompt
def create_prompt(text):
    input_data = classifier_zero_shot(text)
    print(input_data)
    score = input_data['score']
    label = input_data['label']
    
    prompt = f"""
                Tu es un modèle NLP spécialisé dans l'analyse et le résumé de textes.
                Le texte fourni appartient à la catégorie : {label}.
                
                Tâches :
                1. Produire un résumé clair, neutre et concis(1 ligne).
                2. Identifier le ton général du texte (positif / neutre / négatif).
                3. Retourner la réponse sous forme de JSON valide avec deux champs : "resume" et "ton".

                Texte à analyser :
                {text}

                Réponds uniquement en JSON.
                """
    return prompt ,score , label


# text = "La ville a inauguré aujourd’hui une nouvelle ligne de tramway destinée à améliorer les déplacements des habitants.Le projet, commencé il y a trois ans, a coûté près de 400 millions d’euros et fait partie d’un plan plus large visant à développer les transports publics et réduire l’usage des voitures."
# prompt , score = create_prompt(text)



# synthèse contextuelle Gemini
def analyse_with_gemini(prompt):
    try:
        client = genai.Client(api_key=API_KEY_GEMINI)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        text_json = text_markdown_json(response.text)
        return text_json
    except Exception as e:
        return f'erreur : {e}'
    
# print(analyse_with_gemini(prompt))



# create a new log
def create_new_analysis_log(log , user , db):
    new_log = AnalysisLogs(
        text = log["text"],
        score = log["score"] ,
        category = log["category"],
        ton = log["ton"],
        resume = log["resume"],
        user_id = user.id
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return new_log


    
