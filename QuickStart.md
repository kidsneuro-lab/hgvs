```sh
./download_refGene.sh -hg38
docker build . -t hgvs
docker run -p 8000:8000 hgvs
or
docker compose up
```

- single translation
```sh
$ curl http://localhost:8000/translate?value=NM_000352.3:c.215A%3EG
["chr11",17496508,"T","C"]
```

- bulk translations
```sh
$ curl -H 'Content-Type: application/json' -X POST -d '["NM_000352.3:c.215A>G", "NM_000352.3:c.215A>T"]' localhost:8000/translate_bulk
[["NM_000352.3:c.215A>G","chr11",17496508,"T","C"],["NM_000352.3:c.215A>T","chr11",17496508,"T","A"]]
```
