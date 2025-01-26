import httpx as http

from yattag import Doc

from unittest.mock import patch, Mock

from torbot.modules.api import get_ip

def generate_mock_troproject_page(header: str, body: str) -> str:
    doc, tag, text = Doc().tagtext()
    with tag("html"):
        with tag("div", klass="content"):
            with tag("h1"):
                text(header)
            with tag("p"):
                text(body)    
    return doc.getvalue()

@patch.object(http.Client, "get")
def test_get_ip(mock_get: Mock) -> None:
    # Gerar o html 
    mock_header = "Tor Project Page"
    mock_bpdy = "Voce esta conectado no Tor. IP 17.0.0.1"
    mock_html_page = generate_mock_troproject_page(mock_header, mock_bpdy)

    # Definir o mock 
    mock_responde = Mock()
    mock_get.return_value = mock_responde
    mock_responde.text.return_value = mock_html_page

    # Attempt teste
    with http.Client() as client:
        resp = get_ip(client)
        assert resp["header"] == mock_header
        assert resp["body"] == mock_bpdy
        
