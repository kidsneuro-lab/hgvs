```sh
docker build . -t hgvs
docker run -p 8000:8000 hgvs
```

- single translation
```sh
curl http://localhost:8000/translate?value=NM_000352.3:c.215A%3EG
```

- multiple translation
```sh
curl -H 'Content-Type: application/json' -X POST -d '["NM_000352.3:c.215A>G", "NM_000352.3:c.215A>T"]' localhost:8000/translate_bulk
```
