# About

A command-line tool used to simulate popular techniques in the field of **Data Communication**.

# Usage

```
usage: dc-sim [-h] [-V] {crc,hamming,stopwait} ...

Simulate data communication techniques.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit

utilities:
  {crc,hamming,stopwait}
    crc                 Simulate the CRC error detection technique.
    hamming             Calculate the Hamming Distance between two codewords.
    stopwait            Simulate the Stop and Wait protocol.
```

# Examples

- Simulate CRC:

```
dc-sim crc --dataword 100100 --generator 1101 --bitinvert
```

- Calculate Hamming Distance:

```
dc-sim hamming --codeword 1001 1110
```

- Simulate Stop and Wait:

Start the **receiver**:

```
dc-sim stopwait --mode receiver
```

Then, start the **sender** in another terminal instance:

```
dc-sim stopwait --mode sender --packets 10
```
[![asciicast](https://asciinema.org/a/Io0AhcaaHkkZ9mCUNSsWIwLbr.png)](https://asciinema.org/a/Io0AhcaaHkkZ9mCUNSsWIwLbr)

# Dependencies

- Python >=3.7
- [argparse](https://pypi.org/project/argparse)

# Installation

> It is advised to install **git** and use the latest version of *pip* before installation, including the essential packages, *setuptools* and *wheel*.

To ensure these packages are up-to-date, run

```
python3 -m pip install --upgrade pip setuptools wheel
```

To install, run

```
python3 -m pip install --no-cache-dir git+https://github.com/hyPnOtICDo0g/dc-sim.git
```
