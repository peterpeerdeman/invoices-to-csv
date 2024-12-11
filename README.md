# invoices-to-csv

I keep my invoices in folders per year, with a filename containing following metadata. This script turns the folder into a CSV that can be pasted into a spreadsheet

`YYYYMMDD-vendor-category-amountincents invoicesoftwareid.pdf`

e.g.

`20240102-amazon-backups-1076 20240429212749.pdf`

## usage

python3 invoices-to-csv.py -o output.csv ~/folder/with/files
