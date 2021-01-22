# ICON Multi-Token Standard (IRC-31) Implementation

This is an reference implementation of the Multi-Token standard written in Python SCORE.
You can find standard interface at [IRC-31](https://github.com/icon-project/IIPs/blob/master/IIPS/iip-31.md).

## Requirements

- Python 3.7 or later.
- [Docker](https://docs.docker.com)

## Usage

### Installation

Clone this project first, and setup a virtual environment.

```
$ git clone git@github.com:sink772/multi-token-standard.git
$ cd multi-token-standard
$ virtualenv -p python3.7 .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

### Running T-Bears Docker Container for Local Testnet

In another terminal, run the following command to initiate the local testnet.

```
$ docker run -it -p 9000:9000 iconloop/tbears:mainnet
```

### Running Tests

Make sure you are in the virtual environment, and run the following command.

```
(.venv) $ make test
```

## License

This project is available under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
