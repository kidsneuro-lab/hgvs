To ensure that we are accurately translating HGVS notation, we are using the ensembl rest api to translate a large batch of variants from HGVS to 
genomic co-ordinates. We can then use these as a base line to test the relative accuracy of this services.
Having them pre-translated means we can run out tests quickly locally, and just periodically update this file.

- To execute it, just point it at a source of hgvs id's and supply an output file.

```shell
python download.py ../hgvs_vcf_valid.tsv output_ensemble.csv output_variant_validator.csv
```

- Runtime is estimated at a couple of hours. While it is possible to reduce this with parallel requests its best not to as the ensembl service is unreliable.

```shell
curl -X "POST" "https://rest.ensembl.org/variant_recoder/homo_sapiens?fields=None&vcf_string=1" \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     -d $'{
  "ids": [
    "NM_172245.4:c.780+135G>A"
  ]
}'
```

```json
[{"A":{"vcf_string":["Y-1294596-G-A","LRG_186-30797-G-A","X-1294596-G-A"],"input":"NM_172245.4:c.780+135G>A"}}]
````