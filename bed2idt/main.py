# Copyright (c) 2025, Chris Kent
# All rights reserved.
#
# This source code is licensed under the BSD-3-Clause license found in the
# LICENSE file in the root directory of this source tree.

import pathlib
import random
from importlib.metadata import version

import typer
import xlsxwriter
from primalbedtools.bedfiles import BedLine, group_by_chrom, group_by_pool
from primalbedtools.scheme import Scheme
from typing_extensions import Annotated

from bed2idt.config import (
    PlateFillBy,
    PlateSize,
    PlateSplitBy,
    TubePurification,
    TubeScale,
)


# Create the typer app
app = typer.Typer(
    name="bed2idt", no_args_is_help=True, pretty_exceptions_show_locals=False
)

SEED = 2025_08_20

plate_letters = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
]
plate_numbers = [*range(1, 25)]


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def create_plates(
    primer_list: list[list[BedLine]],
    workbook,
    sheet_name: str,
    by_rows: bool,
    size: PlateSize,
):
    for index, primer_sublist in enumerate(primer_list):
        # Create all the indexes in a generator
        if size == PlateSize.WELL96:
            letters = plate_letters[:8]
            numb = plate_numbers[:12]
        else:
            letters = plate_letters[:16]
            numb = plate_numbers[:24]

        # Ensure the plate is filled up correctly
        if by_rows:
            indexes = ((letter, str(number)) for letter in letters for number in numb)
        else:
            indexes = ((letter, str(number)) for number in numb for letter in letters)

        # Create the sheet
        worksheet = workbook.add_worksheet(f"{sheet_name}.{index}")

        headings = ["Well Position", "Name", "Sequence"]
        for index, head in enumerate(headings):
            worksheet.write(0, index, head)
        row = 1
        content = [
            ("".join(i), p.primername, p.sequence)
            for i, p in zip(indexes, primer_sublist)
        ]

        for primer in content:
            for col, data in enumerate(primer):
                worksheet.write(row, col, data)
            row += 1


def plates_go(
    scheme: Scheme,
    workbook,
    splitby: PlateSplitBy,
    fillby: PlateFillBy,
    plateprefix: str,
    randomise: bool,
    size: PlateSize,
):
    if randomise:
        random.Random(SEED).shuffle(scheme.bedlines)

    splits: dict[str, list[BedLine]] = dict()

    # Ensure primers are split by pool
    if splitby == PlateSplitBy.POOL:
        splits = {str(k): v for k, v in group_by_pool(scheme.bedlines).items()}

    # Don't Split plates by primers
    elif splitby == PlateSplitBy.NONE:
        splits = {"": scheme.bedlines}

    # Split primers by the ref genome
    elif splitby == PlateSplitBy.REF:
        splits = group_by_chrom(scheme.bedlines)

    elif splitby == PlateSplitBy.REF_POOL:
        ref_splits = group_by_chrom(scheme.bedlines)

        for ref, ref_bedlines in ref_splits.items():
            ref_pool_splits = {
                str(k): v for k, v in group_by_pool(ref_bedlines).items()
            }
            for pool, ref_pool_bedlines in ref_pool_splits.items():
                splits[f"{ref}_{pool}"] = ref_pool_bedlines

    else:
        raise typer.BadParameter("Please select a valid option for --splitby")

    # make sure no pool are more than 96 or 384 primers
    split_plates = {
        k: list(chunks(v, 96 if size == PlateSize.WELL96 else 384))
        for k, v in splits.items()
    }  # type: ignore

    for split, plates in split_plates.items():
        if plates:
            create_plates(
                plates,  # type: ignore
                workbook,
                sheet_name=f"{plateprefix}_{split}" if split else f"{plateprefix}",
                by_rows=fillby == PlateFillBy.ROWS,
                size=size,
            )

    workbook.close()


def tubes_go(
    scheme: Scheme, workbook, scale: TubeScale, purification: TubePurification
):
    worksheet = workbook.add_worksheet()
    headings = ["Name", "Sequence", "Scale", "Purification"]

    # Write the headings
    for index, head in enumerate(headings):
        worksheet.write(0, index, head)
    row = 1

    # Generate the things to write
    content = [
        (x.primername, x.sequence, scale.value, purification.value)
        for x in scheme.bedlines
    ]

    # Write each line
    for primer in content:
        for col, data in enumerate(primer):
            worksheet.write(row, col, data)

        row += 1

    workbook.close()


def append_xlsx(path: pathlib.Path):
    """
    Append to an xlsx file path
    """
    if path.suffix != ".xlsx":
        return path.with_suffix(".xlsx")
    return path


def typer_callback_version(value: bool):
    if value:
        typer.echo(f"bed2idt version: {version('bed2idt')}")
        raise typer.Exit()


@app.callback()
def common(
    value: Annotated[bool, typer.Option] = typer.Option(
        False, "--version", callback=typer_callback_version
    ),
):
    pass


@app.command(no_args_is_help=True)
def plates(
    bedfile: Annotated[
        pathlib.Path,
        typer.Argument(help="The path to the bed file", readable=True),
    ],
    plateprefix: Annotated[
        str,
        typer.Option(
            help="The prefix used in naming sheets in the excel file",
            show_default=False,
        ),
    ],
    output: Annotated[
        pathlib.Path,
        typer.Option(
            help="The output location of the file. Defaults to output.xlsx",
            writable=True,
            callback=append_xlsx,
            dir_okay=False,
        ),
    ] = pathlib.Path("output.xlsx"),
    splitby: Annotated[
        PlateSplitBy,
        typer.Option(help="Should the primers be split across different plate"),
    ] = PlateSplitBy.POOL.value,  # type: ignore
    fillby: Annotated[
        PlateFillBy, typer.Option(help="How should the plate be filled")
    ] = PlateFillBy.COLS.value,  # type: ignore
    force: Annotated[
        bool, typer.Option(help="Override the output directory", show_default=False)
    ] = False,
    randomise: Annotated[
        bool,
        typer.Option(help="Randomise the order of primers within a plate"),
    ] = False,
    platesize: Annotated[
        PlateSize,
        typer.Option(help="The size of the plate to use"),
    ] = PlateSize.WELL96.value,  # type: ignore
):
    # Check the outpath
    if output.exists() and not force:
        raise typer.BadParameter(
            f"File exists at {output.absolute()}, add --force to overwrite"
        )
    # Read in the primers
    scheme = Scheme.from_file(str(bedfile))

    # Create the workbook
    workbook = xlsxwriter.Workbook(output)

    # Create the plates
    plates_go(scheme, workbook, splitby, fillby, plateprefix, randomise, platesize)


@app.command(no_args_is_help=True)
def tubes(
    bedfile: Annotated[
        pathlib.Path, typer.Argument(help="The path to the bed file", readable=True)
    ],
    output: Annotated[
        pathlib.Path,
        typer.Option(
            help="The output location of the file. Defaults to output.xlsx",
            writable=True,
            callback=append_xlsx,
            dir_okay=False,
        ),
    ] = pathlib.Path("output.xlsx"),
    scale: Annotated[
        TubeScale, typer.Option(help="The concentration of the primers")
    ] = TubeScale.NM25.value,  # type: ignore
    purification: Annotated[
        TubePurification, typer.Option(help="The purification of the primers")
    ] = TubePurification.STD.value,  # type: ignore
    force: Annotated[
        bool, typer.Option(help="Override the output directory", show_default=False)
    ] = False,
):
    # Check the outpath
    if output.exists() and not force:
        raise typer.BadParameter(
            f"File exists at {output.absolute()}, add --force to overwrite"
        )

    # Read in the primers
    scheme = Scheme.from_file(str(bedfile))
    # Create the workbook
    workbook = xlsxwriter.Workbook(output)

    # Create the tubes
    tubes_go(scheme, workbook, scale, purification)


if __name__ == "__main__":
    app()
