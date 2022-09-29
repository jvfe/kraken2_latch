from latch.types import LatchAuthor, LatchMetadata, LatchParameter

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
)

metadata.parameters = {
    "samples": LatchParameter(
        display_name="Kraken2 samples",
        description="Paired-end FastQ files",
        batch_table_column=True,
        section_title="Data",
    ),
    "kraken_database": LatchParameter(
        display_name="Kraken2 database",
        description="A database created with the kraken-build command",
    )
}
