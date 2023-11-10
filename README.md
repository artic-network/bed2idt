# bed2idt 

This command-line interface (CLI) generates IDT input files from a 7-column primer bed file.

## Description

The IDT Input File Generator CLI allows you to convert a primer bed file into IDT input files. IDT (Integrated DNA Technologies) is a company that provides custom DNA synthesis services. This tool automates the process of generating input files for ordering primers from IDT.

## Installation

#### From pip

```pip instal bed2idt```

#### From Poetry / source

```git clone https://github.com/ChrisgKent/bed2idt```

```poetry install && poetry build```

## Usage

To use the CLI, run the following command:

    bed2idt [options] [command] [command-options]


## Options

The CLI supports the following options:

-   `-b, --bedfile`: Path to the primer bed file (required).
-   `-o, --output`: The output location for the generated IDT input file(s) (default: `output.xlsx`).
-   `plate` command:
    -   `-s, --splitby`: Specifies whether the primers should be split across more than one plate. Valid options are `pool`, `ref`, `none`, ~~`next`~~ (default: `pool`).
    -   `-f, --fillby`: Specifies how the plates should be filled. Valid options are `rows` or `cols` (default: `rows`).
-   `tube` command:
    -   `-s, --scale`: The concentration of the primers. Valid options are `25nm`, `100nm`, `250nm`, `1um`, `2um`, `5um`, `10um`, `4nmU`, `20nmU`, `PU`, or `25nmS` (default: `25nm`).
    -   `-p, --purification`: The purification method for the primers. Valid options are `STD`, `PAGE`, `HPLC`, `IEHPLC`, `RNASE`, `DUALHPLC`, or `PAGEHPLC` (default: `STD`).
-   `--force`: Overrides the output directory if it already exists.

## Examples

1.  Generate 96-well plate IDT input files for a primer bed file named `primer.bed` and save/overide the output as `output.xlsx`, split by pools:

    ```bed2idt -b primer.bed --force plate --splitby pools```

2.  Generate tube IDT input files for a primer bed file named `primer.bed`, save the output as `custom_output.xlsx`, and specify a purification method:

    ```bed2idt -b primer.bed -o custom_output.xlsx tube --purification PAGE```

3.  Generate IDT input files for a primer bed file named `primer.bed` without splitting the primers across multiple plates:

    ```bed2idt -b primer.bed plate --splitby none```

4.  Generate IDT input files `primer.xlsx` for a primer.bed file named `primer.bed`, splitting the plate by pool, and filling plates by col:

    ```bed2idt -b primer.bed -o primer.xlsx plate  --splitby pools --filllby cols```

Note: Make sure to replace `python` with the appropriate command for running Python on your system.

## 
