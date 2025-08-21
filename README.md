# `bed2idt`

[![CI](https://github.com/ChrisgKent/bed2idt/actions/workflows/pytest.yml/badge.svg)](https://github.com/ChrisgKent/bed2idt/actions/workflows/pytest.yml)

## Installation


### Via pip
```console
$ pip install bed2idt 
```

# CLI

**Usage**:

```console
$ bed2idt [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `plates`
* `tubes`

## `bed2idt plates`

**Usage**:

```console
$ bed2idt plates [OPTIONS] BEDFILE
```

**Arguments**:

* `BEDFILE`: The path to the bed file  [required]

**Options**:

* `--output FILE`: The output location of the file. Defaults to output.xlsx  [default: output.xlsx]
* `--splitby [pool|ref|ref_pool|none]`: Should the primers be split across different plate  [default: pool]
* `--fillby [rows|cols]`: How should the plate be filled  [default: cols]
* `--plateprefix TEXT`: The prefix used in naming sheets in the excel file  [default: plate]
* `--force / --no-force`: Override the output directory
* `--randomise / --no-randomise`: Randomise the order of primers within a plate  [default: no-randomise]
* `--platesize [96|384]`: The size of the plate to use  [default: 96]
* `--help`: Show this message and exit.

## `bed2idt tubes`

**Usage**:

```console
$ bed2idt tubes [OPTIONS] BEDFILE
```

**Arguments**:

* `BEDFILE`: The path to the bed file  [required]

**Options**:

* `--output FILE`: The output location of the file. Defaults to output.xlsx  [default: output.xlsx]
* `--scale [25nm|100nm|250nm|1um|5um|10um]`: The concentration of the primers  [default: 25nm]
* `--purification [STD|PAGE|HPLC|IEHPLC|RNASE|DUALHPLC|PAGEHPLC]`: The purification of the primers  [default: STD]
* `--force / --no-force`: Override the output directory
* `--help`: Show this message and exit.

