
def test_analyse_with_gemini(mocker):
    
    mock_client_class = mocker.patch('services.analyze_services.genai.Client')
    
    mock_client = mocker.Mock()
    mock_client_class.return_value = mock_client
    
    mock_response = mocker.Mock()
    mock_response.text = '{"resume": "ok", "ton": "neutre"}'
    
    mock_client.models.generate_content.return_value = mock_response
    
    from services.analyze_services import analyse_with_gemini
    
    result = analyse_with_gemini('prompt test')
    
    assert result["resume"] == "ok"
    assert result["ton"] ==  "neutre"
    
    
    
    
    
    