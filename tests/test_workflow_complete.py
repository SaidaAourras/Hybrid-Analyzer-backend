# from fastapi.testclient import TestClient
# from main import app
# def test_workflow_hf_gemini(mocker):
    
#     client = TestClient(app)
#     mocker.patch("api.v1.routes.analyse.verify_token", return_value={'email':'k@gmail.com', 'password':'123456'})
#     mocker.patch("api.v1.routes.analyse.create_prompt", return_value=("p", 0.23456819355487823, "éducation"))
#     mocker.patch("api.v1.routes.analyse.analyse_with_gemini", return_value={"ton": "neutre", "resume": "Le texte fourni est un mot unique ('test') et ne contient pas suffisamment d'informations pour être résumé."})
#     mocker.patch("api.v1.routes.analyse.verify_password", return_value=True)
#     mocker.patch("api.v1.routes.analyse.create_new_analysis_log", return_value={"ok": True})
    
#     response = client.post("/api/v1/analysis/analyse", json={"text": "test"})
    
#     assert response.status_code == 200