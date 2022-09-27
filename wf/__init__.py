import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from dataclasses_json import dataclass_json
from latch import large_task, map_task, message, small_task, workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile


@dataclass_json
@dataclass
class Sample:
    read1: LatchFile
    read2: LatchFile
    sample_name: str


@dataclass_json
@dataclass
class KrakenSample:
    data: Sample
    database: LatchDir


@large_task
def create_kraken2_database() -> LatchDir:

    database_name = "standard_kraken_db"
    database_dir = Path(database_name).resolve()

    _krakenbuild_cmd = ["kraken2-build", "--standard", "--db", str(database_dir)]

    subprocess.run(_krakenbuild_cmd, check=True)

    return LatchDir(str(database_dir), "latch:///kraken2/standard_kraken_db")


@small_task
def create_kraken2_inputs(
    samples: List[Sample], database: LatchDir
) -> List[KrakenSample]:
    return [KrakenSample(data=sample, database=database) for sample in samples]


@large_task
def run_kraken2(
    sample: KrakenSample,
) -> LatchDir:
    """Classify metagenomic reads with Kraken2

    Returns a tuple, first being the kraken2 file and second being the kraken report
    """
    # A reference to our output.
    output_dir_name = f"{sample.data.sample_name}_results/"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_name = f"{output_dir_name}{sample.data.sample_name}.kraken2"
    kraken_out = Path(output_name).resolve()

    report_outname = f"{output_dir_name}{sample.data.sample_name}.tsv"
    report_out = Path(report_outname).resolve()

    _kraken2_cmd = [
        "kraken2",
        "-db",
        sample.database.local_path,
        "--paired",
        sample.data.read1.local_path,
        sample.data.read2.local_path,
        "--report",
        str(report_out),
    ]

    with open(kraken_out, "w") as f:
        subprocess.call(_kraken2_cmd, stdout=f)

    return (LatchDir(str(output_dir), f"latch:///kraken2/{output_dir_name}"),)


@workflow
def kraken2(samples: List[Sample]) -> List[LatchDir]:
    """Taxonomic sequence classification with Kraken2

    Kraken2
    ----

    Kraken 2[^1] is the newest version of Kraken, a taxonomic
    classification system using exact k-mer matches to achieve
    high accuracy and fast classification speeds. This classifier
    matches each k-mer within a query sequence to the lowest common ancestor (LCA)
    of all genomes containing the given k-mer. The k-mer assignments inform
    the classification algorithm.

    [^1]: Wood, D.E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2.
    Genome Biol 20, 257 (2019). https://doi.org/10.1186/s13059-019-1891-0
    """
    kraken_database = create_kraken2_database()

    kraken_inputs = create_kraken2_inputs(samples=samples, database=kraken_database)

    return map_task(run_kraken2)(sample=kraken_inputs)


LaunchPlan(
    kraken2,
    "Shotgun metagenomics data",
    {
        "samples": [
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
    },
)
