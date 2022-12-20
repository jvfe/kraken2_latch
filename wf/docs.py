from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    Params,
    Section,
    Text,
)

PARAMS = {
    "samples": LatchParameter(
        display_name="Kraken2 samples",
        description="Paired-end FastQ files",
        batch_table_column=True,
        section_title="Data",
    ),
    "kraken_database": LatchParameter(
        display_name="Kraken2 database",
        description=(
            "A database created with the kraken-build command. "
            "Must also contain Bracken database-kmer files"
        ),
    ),
    "read_length": LatchParameter(
        display_name="Read length", description="Ideal length of reads in your sample"
    ),
    "classification_level": LatchParameter(
        display_name="Taxonomic rank",
    ),
    "threshold": LatchParameter(display_name="Minimum read threshold"),
}

FLOW = [
    Section("Samples", Params("samples")),
    Section("Kraken2 options", Params("kraken_database")),
    Section(
        "Bracken options",
        Text(
            "Bracken uses the taxonomy labels assigned by Kraken "
            "to estimate the number of reads originating from each species present "
            "in a sample"
        ),
        Params("read_length"),
        Text(
            "Specifies the taxonomic rank to analyze. "
            "Each classification at this specified rank will receive "
            "an estimated number of reads belonging to that rank after abundance estimation."
        ),
        Params("classification_level"),
        Text(
            "Specifies the minimum number of reads required for a classification "
            "at the specified rank. Any classifications with less than the specified threshold "
            "will not receive additional reads from higher taxonomy levels when distributing reads "
            "for abundance estimation."
        ),
        Params("threshold"),
    ),
]

metadata = LatchMetadata(
    display_name="Kraken2",
    documentation="https://github.com/jvfe/kraken2_latch/blob/main/README.md",
    author=LatchAuthor(
        name="jvfe",
        github="https://github.com/jvfe",
    ),
    repository="https://github.com/jvfe/kraken2_latch",
    license="MIT",
    tags=["NGS", "taxonomy", "metagenomics"],
    parameters=PARAMS,
    flow=FLOW,
)
