from bed2idt.cli import cli
import pathlib
import sys
import xlsxwriter

"""
These are the correct values on the IDT website as of time of writing
Please check https://eu.idtdna.com/site/order/oligoentry to confirm
"""


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


def plate(primer_list, workbook, args):
    # Ensure primers are split by pool
    if args.splitby == "pool":
        # Make sure the pools are zero indexed
        all_pools = list({int(x[4]) - 1 for x in primer_list})
        all_pools.sort()

        # If only one pool complain
        if len(all_pools) <= 1:
            sys.exit("To few pools to split by. Please use -s none")

        # Ensure all pools are pos
        for pool in all_pools:
            if pool < 0:
                sys.exit("Please ensure all pools are 1-indexed")

        # If people do werid things with pools this should be pretty hardy
        plates = [[] for _ in range((max(all_pools) + 1))]
        for primer in primer_list:
            pool = int(primer[4]) - 1
            plates[pool].append(primer)

    # Don't Split plates by primers
    elif args.splitby == "none":
        plates = [primer_list]

    # Split primers by the ref genome
    elif args.splitby == "ref":
        all_refs = {x[0] for x in primer_list}
        ref_dict = {x: i for i, x in enumerate(all_refs)}

        # If only one pool complain
        if len(all_refs) <= 1:
            sys.exit("To few referances to split by. Please use -s none")

        plates = [[] for _ in all_refs]
        for primer in primer_list:
            plate = ref_dict[primer[0]]
            plates[plate].append(primer)

    # Split primers by INNER or OUTER name
    elif args.splitby == "nest":
        plates = [[], []]
        for primer in primer_list:
            if "INNER" in primer[3].upper():
                plates[0].append(primer)
            elif "OUTER" in primer[3].upper():
                plates[1].append(primer)
            else:
                sys.exit(f"Cannot find (INNER / OUTER) in {primer[3].upper()}")

    # make sure no pool are more than 96 primers
    plates = [chunks(x, 96) for x in plates]

    for index, plate in enumerate(plates):
        if plate:  # Plates can be empty so only write non-empty plates
            create_plate(
                plate,
                workbook,
                sheet_name=f"plate_{index +1}",
                by_rows=args.fillby == "rows",
            )

    workbook.close()


def tubes(primer_list, workbook, args):
    worksheet = workbook.add_worksheet()
    headings = ["Name", "Sequence", "Scale", "Purification"]

    # Write the headings
    for index, head in enumerate(headings):
        worksheet.write(0, index, head)
    row = 1

    # Generate the things to write
    content = [(x[3], x[6], args.scale, args.purification) for x in primer_list]

    # Write each line
    for primer in content:
        for col, data in enumerate(primer):
            worksheet.write(row, col, data)

        row += 1

    workbook.close()


def read_bedfile(bed_path: pathlib.Path) -> list:
    primer_list = []
    with open(bed_path, "r") as file:
        for line in file.readlines():
            primer_list.append(line.split())
    return primer_list


def main():
    args = cli()

    # Check the outpath
    if args.output.exists() and not args.force:
        sys.exit(
            f"Directory exists at {args.output.absolute()}, add --force to overwrite"
        )
    # Read in the primers
    primer_list = read_bedfile(args.bedfile)

    # Create the workbook
    workbook = xlsxwriter.Workbook(args.output)

    if args.command == "plate":
        plate(primer_list, workbook, args)
    elif args.command == "tube":
        tubes(primer_list, workbook, args)
    else:
        sys.exit("Give plates or tubes")


if __name__ == "__main__":
    main()
