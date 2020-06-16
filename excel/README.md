# Excel models 1.x

This has the Excel models used with version 1.x

## Note on breaking bugs

The main issue with models are in the use of the `column` which in the latest
versions of Excel, called Microsoft 365 or Office 365 have a breaking bug
because a column returns an array, so `COLUMN()` is an array and you cannot use
to index into something with an OFFSET().

The fix is to collapse an the COLUMN with SUM(COLUMN()). this does not affect
Mac Excel v16 or google sheets, but the feature called a Dynamic Array causes
automatic arrays to get created when you don't need it.

The net is that you should never save a sheet with Microsoft 365, it produces
incompatible formulas when arrays are used.

We use them in a sumproduct and this is breaking.
