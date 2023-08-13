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
        echo Downloading Refseq
        mkdir -p reference
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
            WHERE r.name = g.acc
        )
        SELECT *
        FROM ncbi
        UNION ALL
        SELECT *
        FROM refGene 
        WHERE REGEXP_REPLACE(name, '\.[0-9]+$', '') NOT IN (SELECT REGEXP_REPLACE(name, '\.[0-9]+$', '')
                                                            FROM ncbi)
        ;" > reference/genes.refGene

        echo Downloading LRG Refgene
        mkdir -p reference
        wget -nv -c -O reference/LRG_RefSeqGene -nv -c https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene

        echo Downloading and indexing hg38
        mkdir -p assemblies
        wget -nv -c -O assemblies/hg38.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/latest/hg38.fa.gz
        gunzip assemblies/hg38.fa.gz
        docker run -it --rm -v ./assemblies:/assemblies emihat/alpine-samtools:latest samtools faidx assemblies/hg38.fa
        ;;
    "-hg38_sample")
        echo Downloading Refseq
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
