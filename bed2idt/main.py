import pathlib
from random import shuffle

import typer
import xlsxwriter
from typing_extensions import Annotated

from bed2idt.__init__ import __version__
from bed2idt.config import PlateFillBy, PlateSplitBy, TubePurification, TubeScale

# Create the typer app
app = typer.Typer(name="bed2idt", no_args_is_help=True)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def create_plate(primer_list: list[list], workbook, sheet_name: str, by_rows: bool):
    for index, primer_sublist in enumerate(primer_list):
        # Create all the indexes in a generator
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        numb = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

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
        content = [("".join(i), p[3], p[6]) for i, p in zip(indexes, primer_sublist)]

        for primer in content:
            for col, data in enumerate(primer):
                worksheet.write(row, col, data)
            row += 1


def plates_go(
    primer_list,
    workbook,
    splitby: PlateSplitBy,
    fillby: PlateFillBy,
    plateprefix: str,
    randomise: bool,
):
    if randomise:
        shuffle(primer_list)

    # Ensure primers are split by pool
    if splitby == PlateSplitBy.POOL:
        # Make sure the pools are zero indexed
        all_pools = list({int(x[4]) - 1 for x in primer_list})
        all_pools.sort()

        # If only one pool complain
        if len(all_pools) <= 1:
            raise typer.BadParameter(
                "To few pools to split by. Please use other --splitby option"
            )

        # Ensure all pools are pos
        for pool in all_pools:
            if pool < 0:
                raise typer.BadParameter("Please ensure all pools are 1-indexed")

        # If people do werid things with pools this should be pretty hardy
        plates = [[] for _ in range(max(all_pools) + 1)]
        for primer in primer_list:
            pool = int(primer[4]) - 1
            plates[pool].append(primer)

    # Don't Split plates by primers
    elif splitby == PlateSplitBy.NONE:
        plates = [primer_list]

    # Split primers by the ref genome
    elif splitby == PlateSplitBy.REF:
        all_refs = {x[0] for x in primer_list}
        ref_dict = {x: i for i, x in enumerate(all_refs)}

        # If only one pool complain
        if len(all_refs) <= 1:
            raise typer.BadParameter(
                "To few references to split by. Please use other --splitby option"
            )

        plates = [[] for _ in all_refs]
        for primer in primer_list:
            plate = ref_dict[primer[0]]
            plates[plate].append(primer)

    else:
        raise typer.BadParameter("Please select a valid option for --splitby")

    # make sure no pool are more than 96 primers
    plates = [list(chunks(x, 96)) for x in plates]  # type: ignore

    for index, plate in enumerate(plates):
        if plate:  # Plates can be empty so only write non-empty plates
            create_plate(
                plate,  # type: ignore
                workbook,
                sheet_name=f"{plateprefix}_{index +1}",
                by_rows=fillby == PlateFillBy.ROWS,
            )

    workbook.close()


def tubes_go(primer_list, workbook, scale: TubeScale, purification: TubePurification):
    worksheet = workbook.add_worksheet()
    headings = ["Name", "Sequence", "Scale", "Purification"]

    # Write the headings
    for index, head in enumerate(headings):
        worksheet.write(0, index, head)
    row = 1

    # Generate the things to write
    content = [(x[3], x[6], scale.value, purification.value) for x in primer_list]

    # Write each line
    for primer in content:
        for col, data in enumerate(primer):
            worksheet.write(row, col, data)

        row += 1

    workbook.close()


def read_bedfile(bed_path: pathlib.Path) -> tuple[list[str], list[list[str]]]:
    """
    Read a BED file and return the header and primer list.

    Args:
        bed_path (pathlib.Path): The path to the BED file.

    Returns:
        tuple[list, list]: A tuple containing the header list and primer list.
    """
    primer_list = []
    header_list = []
    with open(bed_path) as file:
        for line in file.readlines():
            line = line.strip()
            # Handle the header
            if line.startswith("#"):
                header_list.append(line)
                continue
            primer_list.append(line.split())
    return header_list, primer_list


def append_xlsx(path: pathlib.Path):
    """
    Append to an xlsx file path
    """
    if path.suffix != ".xlsx":
        return path.with_suffix(".xlsx")
    return path


def typer_callback_version(value: bool):
    if value:
        typer.echo(f"bed2idt version: {__version__}")
        raise typer.Exit()


@app.callback()
def common(
    value: Annotated[bool, typer.Option] = typer.Option(
        False, "--version", callback=typer_callback_version
    ),
):
    pass


@app.command()
def plates(
    bedfile: Annotated[
        pathlib.Path,
        typer.Argument(help="The path to the bed file", readable=True),
    ],
    output: Annotated[
        pathlib.Path,
        typer.Option(
            help="The output location of the file. Defaults to output.xlsx",
            writable=True,
            callback=append_xlsx,
        ),
    ] = pathlib.Path("output.xlsx"),
    splitby: Annotated[
        PlateSplitBy,
        typer.Option(help="Should the primers be split across different plate"),
    ] = PlateSplitBy.POOL.value,  # type: ignore
    fillby: Annotated[
        PlateFillBy, typer.Option(help="How should the plate be filled")
    ] = PlateFillBy.COLS.value,  # type: ignore
    plateprefix: Annotated[
        str, typer.Option(help="The prefix used in naming sheets in the excel file")
    ] = "plate",
    force: Annotated[
        bool, typer.Option(help="Override the output directory", show_default=False)
    ] = False,
    randomise: Annotated[
        bool,
        typer.Option(
            help="Randomise the order of primers within a plate", show_default=False
        ),
    ] = False,
):
    # Check the outpath
    if output.exists() and not force:
        raise typer.BadParameter(
            f"File exists at {output.absolute()}, add --force to overwrite"
        )
    # Read in the primers
    header, primer_list = read_bedfile(bedfile)

    # Create the workbook
    workbook = xlsxwriter.Workbook(output)

    # Create the plates
    plates_go(primer_list, workbook, splitby, fillby, plateprefix, randomise)


@app.command()
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
    header, primer_list = read_bedfile(bedfile)

    # Create the workbook
    workbook = xlsxwriter.Workbook(output)

    # Create the tubes
    tubes_go(primer_list, workbook, scale, purification)


if __name__ == "__main__":
    app()
