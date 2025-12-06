


def test_classifier_zero_shot(mocker):
    
    mock_post = mocker.patch("services.analyze_services.requests.post")
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{'label': 'technologie', 'score': 0.92}]
    
    
    mock_post.return_value = mock_response
    
    from services.analyze_services import classifier_zero_shot
    
    result = classifier_zero_shot("Le nouveau iPhone sort demain.")
    assert result["label"] == "technologie"
    assert result["score"] == 0.92
