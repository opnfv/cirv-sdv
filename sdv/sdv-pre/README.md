# Project Title

SDV - Pre deployment validation

### Prerequisites

Use Python Virtual Environment Manager
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```
Install the required packages from requirements.txt

```
pip install -r requirements.txt
```

### Getting Started

data/ Folder contains all dummy pdf, installer-mainfests and mapping files
To start the server run,
```
python server.py
```
Currently there exists two functionalities, extrapolation and validation.

To do a extrapolate POST request, use following command
```
curl --header "Content-Type: application/json"   --request POST   --data '{"pdf_fn":"<>", "store_at":"<>"}'   http://localhost:8888/extrapolate
```
To run this on commandline, use the following command
```
python extrapolation.py --pdf_fn="path/to/pdf_fn" --store-at="path/to/storage"
```
Sample pdf file is located in data directory.
The pdf_fn key expects absolute filepath to pdf.
the store_at key expects absolute filepath to which the new generated pdf should be stored at.

To do a validation POST request, use following command
```
curl --header "Content-Type: application/json"   --request POST   --data '{"pdf_file":"<>", "inst_dir":"<>", "inst_type":"<>", "gsw":"<>", "tsw":"<>"}'   http://localhost:8888/validate
```
To run this on commandline, use the following command.
```
python cli_validation.py --mani_dir=path/to/mani_dir --inst_type=type --pdf=path/to/pdf --gsw=path/to/gsw --tsw=/path/to/tsw
```
Sample pdf file(json), and installer file(yaml) is located in sdv-predep/data directory.
The pdf_file key expects absolute filepath to pdf.
The inst_dir key expects absolute filepath to installer directory.
The inst_type key expects installer type string ("airship", "tripleo", etc.)
The gsw key expects path to the global software directory.
The tsw key expects path to the type software directory.

Mapping files are found in sdv-predep/mapping directory. There exist mapping for 2 installers currently ( Airship & TripleO).
The validation files are found is sdv-predep/validation directory. And the extrapolation files in sdv-predep/extrapolation directory.

