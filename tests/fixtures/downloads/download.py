import csv, sys
import requests

server = "https://rest.ensembl.org"
ext = "/variant_recoder/human/{hgvs_c}?"

def read_tsv(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            rows.append(row)
    return rows

def get_translation(hgvs_c):
    ext = "/variant_recoder/human/{}?fields=None&vcf_string=1".format(hgvs_c)
    timeout = 90

    response = requests.get(server+ext, headers={"Content-Type":"application/json"}, timeout=timeout)
    if not response.ok:
        return hgvs_c, False, None, None, None, None
    json = response.json()
    # Parse output json into its component values
    chrom, pos, ref, alt = json[0][list(json[0].keys())[0]]['vcf_string'][0].split("-")
    return hgvs_c, True, chrom, int(pos), ref, alt


if __name__ == "__main__":
    print("Running")
    if len(sys.argv) != 3:
        print("Usage: python download.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    print(f"Reading {input_file}")
    data = read_tsv(input_file)
    position=1
    total = len(data)
    print(f"Found {total} variants")
    
    hgvs_column_name = "hgvs_c"

    results = []
    # write file header, overwriting the existing file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["HGVS", "Success", "Chromosome", "Position", "Ref", "Alt"])

    # Lookup the ensembl API for each row and save the result in a matching file
    for row in data:
        hgvs_c = row.get(hgvs_column_name)
        
        print(f"Progress {position}/{total}")
        result = get_translation(hgvs_c)
        
        # write row, appending the existing file
        with open(output_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(result)

        position = position + 1
        
        
        
        




