def test_workflow_hf_gemini(mocker):
    
    from services.analyze_services import create_prompt
    
    # hf + create prompt
    
    mock_post = mocker.patch("services.analyze_services.requests.post")
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{'label': 'technologie', 'score': 0.92}]
    
    mock_post.return_value = mock_response
    
    prompt ,score , label = create_prompt("Le nouveau iPhone sort demain.")

    assert score == 0.92
    assert label == "technologie"
    
    
    # analyse with gemini
    
    mock_client_class = mocker.patch('services.analyze_services.genai.Client')
    
    mock_client = mocker.Mock()
    mock_client_class.return_value = mock_client
    
    mock_gemini_response = mocker.Mock()
    mock_gemini_response.text = '{"resume": "ok", "ton": "neutre"}'
    
    mock_client.models.generate_content.return_value = mock_gemini_response
    
    from services.analyze_services import analyse_with_gemini
    
    result = analyse_with_gemini(prompt)
    
    assert result["resume"] == "ok"
    assert result["ton"] ==  "neutre"