import os
import sys
from fastapi import Path
import pytest
import logging
from fastapi.testclient import TestClient

current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder_path = os.path.join(current_dir, "..")
sys.path.append(target_folder_path)

logger = logging.getLogger(__name__)

class TestHealth:
    
    @pytest.fixture
    def client(self):
        from pyhgvs.api import app
        yield TestClient(app)

    def test_home_returns_success(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_api_is_alive(self, client):
        response = client.get("/health/alive")
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}

    def test_api_is_ready(self, client):
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}
        
    def test_api_translates_variant_with_asterix(self,client):
        variant='NM_000284.4:c.1172_*3del'
        response = client.post(f"/translate", json={"value": variant})
        assert response.status_code == 200
        assert response.json() == ['X', 19359651, 'TAAGGG', 'T']
        
    def test_api_translates_variant_with_greater_then(self,client):
        variant='NM_001110556.2:c.3396G>T'
        response = client.post(f"/translate", json={"value": variant})
        assert response.status_code == 200
        assert response.json() == ['X', 154360399, 'C', 'A']
    
    def test_api_translates_variant_with_plus(self,client):
        variant='NM_004006.3:c.8547+18C>T'
        response = client.post(f"/translate", json={"value": variant})
        assert response.status_code == 200
        assert response.json() == ['X', 31496770, 'G', 'A']
        