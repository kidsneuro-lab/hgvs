#!/bin/sh

# Check if a command line argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <-hg38|-hg38_sample>"
    exit 1
fi

# Store the parameter in a variable
parameter="$1"

# Download and index the genome based on the parameter
case "$parameter" in
    "-hg38")
        echo "Downloading Refseq (ncbiRefSeq)"
        mkdir -p reference
        docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 -it --rm mysql mysql -ugenome -hgenome-euro-mysql.soe.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "SELECT r.bin,
            r.name,
            r.chrom,
            r.strand,
            r.txStart,
            r.txEnd,
            r.cdsStart,
            r.cdsEnd,
            r.exonCount,
            CONVERT(r.exonStarts using utf8) AS exonStarts,
            CONVERT(r.exonEnds using utf8) AS exonEnds,
            r.score,
            r.name2,
            r.cdsStartStat,
            r.cdsEndStat,
            CONVERT(r.exonFrames using utf8) AS exonFrames
        FROM hg38.ncbiRefSeq r
        WHERE r.chrom IN ('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM')
        ;" > reference/genes.refGene
        
        echo "Downloading Refseq (refGene)"
        docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 -it --rm mysql mysql -ugenome -hgenome-euro-mysql.soe.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "WITH ncbi_names AS
        (
            SELECT DISTINCT REGEXP_REPLACE(name, '\.[0-9]+$', '') AS name 
            FROM hg38.ncbiRefSeq
        ), version_info AS (
            SELECT acc, version
            FROM hgFixed.gbCdnaInfo
            WHERE organism = 3218 -- Homo sapien
            AND type = 'mRNA'
            AND SUBSTR(acc, 1, 2) IN ('NM','NR','XM','XR')
        )
        SELECT r.bin,
            CONCAT(r.name, '.', g.version) AS name,
            r.chrom,
            r.strand,
            r.txStart,
            r.txEnd,
            r.cdsStart,
            r.cdsEnd,
            r.exonCount,
            CONVERT(r.exonStarts using utf8) AS exonStarts,
            CONVERT(r.exonEnds using utf8) AS exonEnds,
            r.score,
            r.name2,
            r.cdsStartStat,
            r.cdsEndStat,
            CONVERT(r.exonFrames using utf8) AS exonFrames
        FROM hg38.refGene r, version_info g
        WHERE r.chrom IN ('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM')
        AND r.name = g.acc
        AND r.name NOT IN (SELECT name FROM ncbi_names)
        ;" >> reference/genes.refGene

        echo Downloading LRG Refgene
        if [ ! -f reference/LRG_RefSeqGene ]; then
            mkdir -p reference
            wget -nv -c -O reference/LRG_RefSeqGene -nv -c https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene
        fi

        echo Downloading and indexing hg38
        if [ ! -f assemblies/hg38.fa.fai ]; then
            mkdir -p assemblies
            wget -nv -c -O assemblies/hg38.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/latest/hg38.fa.gz
            gunzip assemblies/hg38.fa.gz
            docker run -it --rm -v ./assemblies:/assemblies emihat/alpine-samtools:latest samtools faidx assemblies/hg38.fa
        fi
        ;;
    "-hg38_sample")
        echo "Downloading Refseq (ncbiRefSeq and refGene)"
        docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 -it --rm mysql mysql -ugenome -hgenome-mysql.cse.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "WITH ncbi AS
        (
            SELECT r.bin,
                r.name,
                r.chrom,
                r.strand,
                r.txStart,
                r.txEnd,
                r.cdsStart,
                r.cdsEnd,
                r.exonCount,
                CONVERT(r.exonStarts using utf8) AS exonStarts,
                CONVERT(r.exonEnds using utf8) AS exonEnds,
                r.score,
                r.name2,
                r.cdsStartStat,
                r.cdsEndStat,
                r.exonFrames
            FROM hg38.ncbiRefSeq r
           WHERE r.chrom = 'chrX'
        ), refGene AS (
            SELECT r.bin,
                CONCAT(r.name, '.', g.version) AS name,
                r.chrom,
                r.strand,
                r.txStart,
                r.txEnd,
                r.cdsStart,
                r.cdsEnd,
                r.exonCount,
                CONVERT(r.exonStarts using utf8) AS exonStarts,
                CONVERT(r.exonEnds using utf8) AS exonEnds,
                r.score,
                r.name2,
                r.cdsStartStat,
                r.cdsEndStat,
                r.exonFrames
            FROM hg38.refGene r, hgFixed.gbCdnaInfo g
            WHERE r.chrom = 'chrX'
            AND r.name = g.acc
        )
        SELECT *
        FROM ncbi
        UNION ALL
        SELECT *
        FROM refGene 
        WHERE REGEXP_REPLACE(name, '\.[0-9]+$', '') NOT IN (SELECT REGEXP_REPLACE(name, '\.[0-9]+$', '')
                                                            FROM ncbi)
        ;" > tests/fixtures/genes.refGene

        echo Downloading LRG Refgene
        if [ ! -f tests/fixtures/LRG_RefSeqGene ]; then
            wget -nv -c -O tests/fixtures/LRG_RefSeqGene -nv -c https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene
        fi

        echo Downloading and indexing hg38 \(chrX\)
        if [ ! -f tests/fixtures/chrX.fa.fai ]; then
            wget -nv -c -O tests/fixtures/chrX.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chrX.fa.gz
            gunzip tests/fixtures/chrX.fa.gz
            docker run -it --rm -v ./tests/fixtures:/assemblies emihat/alpine-samtools:latest samtools faidx assemblies/chrX.fa
        fi
        ;;
    *)
        echo "Unknown parameter: $parameter"
        exit 1
        ;;
esac

echo "Done"
