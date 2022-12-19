from latch.types import LatchDir, LatchFile

from wf import Sample, kraken2

kraken2(
    samples=[
        Sample(
            sample_name="SRR579291",
            read1=LatchFile("s3://latch-public/test-data/4318/SRR579291_1.fastq"),
            read2=LatchFile("s3://latch-public/test-data/4318/SRR579291_2.fastq"),
        ),
        Sample(
            sample_name="SRR579292",
            read1=LatchFile("s3://latch-public/test-data/4318/SRR579292_1.fastq"),
            read2=LatchFile("s3://latch-public/test-data/4318/SRR579292_2.fastq"),
        ),
    ],
    kraken_database=LatchDir("s3://latch-public/test-data/4318/standard_kraken_db/"),
)
