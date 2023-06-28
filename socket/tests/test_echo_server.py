import pytest
import re
import requests


def test_response_format(host, port):
    r = requests.get(f'http://{host}:{port}')
    assert r.status_code == 200
    headers = r.text.split('\r\n')
    assert headers[0] == 'Request Method: GET'
    assert re.match(r"Request Source: \('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', \d+\)", headers[1]) is not None
    assert headers[2] == 'Response Status: 200 OK'


def test_default_headers(host, port):
    r = requests.get(f'http://{host}:{port}')
    for h in r.request.headers.items():
        assert f'{h[0]}: {h[1]}' in r.text


def test_custom_header(host, port):
    key, val = 'MyHeader', 'Agr'
    r = requests.get(f'http://{host}:{port}', headers={key: val})
    assert f'{key}: {val}' in r.text


@pytest.mark.parametrize('code, expected_code', [
    (200, 200),
    (201, 201),
    (404, 404),
    (503, 503),
    ('a', 200),
    ('', 200),
])
def test_status_code(host, port, code, expected_code):
    r = requests.get(f'http://{host}:{port}/?status={code}')
    assert r.status_code == expected_code


def test_status_second_parameter(host, port):
    r = requests.get(f'http://{host}:{port}/?a=1&status=500')
    assert r.status_code == 500


def test_post_method(host, port):
    r = requests.post(f'http://{host}:{port}')
    assert 'Request Method: POST' in r.text


def test_server_alive(host, port):
    for r in range(2):
        r = requests.get(f'http://{host}:{port}')
        assert r.status_code == 200
