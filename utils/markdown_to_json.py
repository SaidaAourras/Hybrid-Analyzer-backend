import json

def text_markdown_json(text_md):
    
    clean = text_md.replace("```json", "").replace("```", "").strip()
    
    data = json.loads(clean)
    
    return data

# text = "```json { \"resume\": \"Une ville a inauguré une nouvelle ligne de tramway, un projet de 400 millions d'euros ayant duré trois ans. Cette initiative vise à améliorer les déplacements des habitants et s'inscrit dans un plan plus large de développement des transports publics et de réduction de l\'utilisation des véhicules privés.\", \"ton\": \"neutre\"}```"

# print(text_markdown_json(text))