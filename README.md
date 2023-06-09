# bed2idt 

This command-line interface (CLI) generates IDT input files from a 7-column primer bed file.

## Description

The IDT Input File Generator CLI allows you to convert a primer bed file into IDT input files. IDT (Integrated DNA Technologies) is a company that provides custom DNA synthesis services. This tool automates the process of generating input files for ordering primers from IDT.

## Usage

To use the CLI, run the following command:

    python bed2idt/main.py [options] [command] [command-options]

## Options

The CLI supports the following options:

-   `-b, --bedfile`: Path to the primer bed file (required).
-   `-o, --output`: The output location for the generated IDT input file(s) (default: `output.xlsx`).
-   `plate` command:
    -   `-s, --splitby`: Specifies whether the primers should be split across more than one plate. Valid options are `pool`, `ref`, or `none` (default: `pool`).
-   `tube` command:
    -   `-s, --scale`: The concentration of the primers. Valid options are `25nm`, `100nm`, `250nm`, `1um`, `2um`, `5um`, `10um`, `4nmU`, `20nmU`, `PU`, or `25nmS` (default: `25nm`).
    -   `-p, --purification`: The purification method for the primers. Valid options are `STD`, `PAGE`, `HPLC`, `IEHPLC`, `RNASE`, `DUALHPLC`, or `PAGEHPLC` (default: `STD`).
-   `--force`: Overrides the output directory if it already exists.

## Examples

1.  Generate 96-well plate IDT input files for a primer bed file named `primers.bed` and save/overide the output as `output.xlsx`, split by pools:

    ```python bed2idt/main.py -b primers.bed --force plate --splitby pools```

2.  Generate tube IDT input files for a primer bed file named `primers.bed`, save the output as `custom_output.xlsx`, and specify a purification method:

    ```python bed2idt/main.py -b primers.bed -o custom_output.xlsx tube --purification PAGE```

3.  Generate IDT input files for a primer bed file named `primers.bed` without splitting the primers across multiple plates:

    ```python bed2idt/main.py -b primers.bed plate --splitby none```

Note: Make sure to replace `python` with the appropriate command for running Python on your system.

## 
