# perflogger

A performance tracking package for Python devs

## Quick start

##### Use pip

Install the `akashic-perflogger` package with pip:
```bash
pip install akashic-perflogger
```

##### Build from sources

```bash
# Download sources
git clone https://github.com/ewigael/perflogger
# Move to sources directory
cd perflogger
# Install from sources with pip
pip install .
```

## Features

### PerfLogger

The `PerfLogger` class allows you to simply record time deltas between operations.
You can then access that data directly from the class instance as the most recent value, or an average over a custom time step.
You may also record all that data to a file to be analyzed later.

## Coming soon:

- ```PerfCounter``` class, to count how many times something happens
- ```PerfAnalyzer```, a co-project to vizualise and compare recorded data
