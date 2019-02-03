<a href="https://imgur.com/v88ofuO"><img src="https://i.imgur.com/v88ofuO.png" title="source: imgur.com" /></a>

# COMPOSER: a deep QC aventure!

Base-calling, error-filtering read preprocessing designed by biologists

## Features

- Few dependencies (Python3 and R)
- Easy to learn
- Supports variable length barcodes and dual-indexing
- Trims buffer sequences and quality filters on a read-by-read basis
- Accepts project directory of multiple libraries
- Designed by biologists (please don't run away!)

## Installation

Clone or download the Git repository to your desired tool folder

```bash
$ git clone https://github.com/ryandkuster/Composer.git
```

## Usage

### Basic usage

Set up your project directory containing the following files:
- 1_R1.fastq
- 1_R2.fastq (optional)
- barcodes_1.txt
- index.txt

***

barcodes_1.txt (tab or space delimited)
```
	A	C	G	T
A	sample1	sample5	sample6	sample10
C	sample2	sample5	sample7	sample10
G	sample3	sample5	sample8	sample10
T	sample4	sample5	sample9	sample10
```

***

index.txt
```
1_R1.fastq  barcodes_1.txt
```

***

From command line, run composer with the specified directory of your project
```bash
$ python3 composer.py <path_to_directory>
```

## License

MIT

<a href="https://imgur.com/rTPylfm"><img src="https://i.imgur.com/rTPylfm.png" title="source: imgur.com" /></a>
