docker build . -t hgvs
docker run -p 8000:8000 hgvs
curl localhost:8000/translate?value=NM_000352.3:c.215A>G
