```sh
./download_refGene.sh -hg38
docker build . -t hgvs
docker run -p 8002:8002 hgvs
or
docker compose up
```
- Examples

```sh
curl "http://localhost:8002/translate?value=NM_001110556.2:c.3396G>T"
["chrX",154360399,"C","A"]
```

```sh
curl "http://localhost:8002/translate?value=NM_000284.4:c.1172_*3del"
["chrX",19359651,"TAAGGG","T"]
```

- bulk translations
```sh
curl -H 'Content-Type: application/json' -X POST -d '["NM_001110556.2:c.3396G>T", "NM_000284.4:c.1172_*3del"]' localhost:8002/translate_bulk
[["NM_001110556.2:c.3396G>T","chrX",154360399,"C","A"],["NM_000284.4:c.1172_*3del","chrX",19359651,"TAAGGG","T"]]
```
