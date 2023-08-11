#!/bin/sh

echo Downloading Refseq

docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 -it --rm mysql mysql -ugenome -hgenome-mysql.cse.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "SELECT r.bin,
       CONCAT(r.name, '.', g.version) AS name,
       REPLACE(r.chrom, 'chr', '') as chrom,
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
FROM hg38.refGene r, hgFixed.gbCdnaInfo g
WHERE r.name = g.acc;" > genes.refGene

echo Downloading LRG Refgene

wget https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene

mv genes.refGene pyhgvs/data
mv LRG_RefSeqGene pyhgvs/data
