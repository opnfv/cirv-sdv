=========
SDVConfig
=========
Welcome to the SDVConfig user Guide!

Who should use this guide?

If you are searching for a way to run the sdvconfig code and don't know how, this guide is for you.

Currently there exists two functionalities, extrapolation and validation.

To do a extrapolate POST request, use following command.

```
curl --header "Content-Type: application/json"   --request POST   --data '{"pdf_fn":"<>", "store_at":"<>"}'   http://localhost:8000/extrapolate
```

To run this on commandline, use the following command

```
python extrapolation.py --pdf_fn="path/to/pdf_fn" --store-at="path/to/storage"
```

The pdf_fn key expects absolute filepath to pdf.
the store_at key expects absolute filepath to which the new generated pdf should be stored at.

To do a validation POST request, use following command

```
curl --header "Content-Type: application/json"   --request POST   --data '{"pdf_file":"<>", "inst_dir":"<>", "inst_type":"<>", "sitename":"<>"}'   http://localhost:8000/validate
```

To run this on commandline, use the following command.

```
python cli_validation.py --mani_dir=path/to/mani_dir --inst_type=type --pdf=path/to/pdf --sitename=sitename
```

The pdf_file key expects absolute filepath to pdf.
The inst_dir key expects absolute filepath to installer directory.
The inst_type key expects installer type string ("airship", "tripleo", etc.)
sitename: intel-pod10, intel-pod15 etc.
