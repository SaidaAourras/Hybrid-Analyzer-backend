from utils.markdown_to_json import text_markdown_json
from db.models.analysis_logs import AnalysisLogs
import os
import requests
from google import genai    
from dotenv import load_dotenv
from utils.markdown_to_json import text_markdown_json
from db.models.analysis_logs import AnalysisLogs
from utils.logger import get_logger


load_dotenv()

logger = get_logger(__name__)

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
    logger.info("HuggingFace request started")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload , timeout=30)
        response.raise_for_status()
        logger.info("HuggingFace request successful")
        return response.json()
    
    except requests.exceptions.RequestException:
        logger.error("HuggingFace request failed", exc_info=True)
        return {'erreur':'HuggingFace request failed'}


# remarque : l'output de cette fonction donne un tableau des objet classifier par score en ordre decroissant
def classifier_zero_shot(text):
    try:
        if not text.strip():
            logger.warning("Empty text received for classification")
            raise ValueError("Le texte ne peut pas être vide.")
        
        logger.info("Zero-shot classification started")
        
        
        output = query({
                "inputs": text,
                "parameters": {"candidate_labels": labels},
            })
        
        result = output[0]
        
        logger.info(
            "Classification completed",
            extra={"label": result["label"], "score": result["score"]}
        )
        return  result
    
    # si le text est vide
    except ValueError as ve:
        logger.warning(f"Invalid input: {ve}")
        return {'erreur':f'Invalid input: {ve}'}
    
    # erreur inattendue
    except Exception as e:
        logger.error("Unexpected error in zero-shot classification", exc_info=True)
        return {'erreur':f'Unexpected error in zero-shot classification {e}'}

# print(classifier_zero_shot('Le nouveau iPhone sort demain.'))

API_KEY_GEMINI = os.getenv('API_KEY_GEMINI')


# create prompt
def create_prompt(text):
    input_data = classifier_zero_shot(text)
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



# synthèse contextuelle Gemini
def analyse_with_gemini(prompt):
    logger.info("Gemini analysis started")
    
    try:
        client = genai.Client(api_key=API_KEY_GEMINI)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        logger.info("Gemini response received")
        
        text_json = text_markdown_json(response.text)
        return text_json
    except Exception as e:
        logger.error("Gemini analysis failed", exc_info=True)
        return {'erreur':f'Gemini analysis failed {e}'}
    
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


    
