# plantumlInliner

This is a small script that will help to merge all subsequent PlantUML-files that are included by the **!include**-directive.

There are no bells and whistles and no guarantee.

## Usage

**python.exe inliner.py** **--path** _"c:/path/to/folder/"_ **--input** _firstFile.puml_ **--output** _output.puml_ 

## Example

There is a tiny example in the (manual) test folder.

### Given

4 files a.puml, b.iuml, c.iuml and common.iuml.
Common.iuml has information such as variables, functions or whatever needed in any other file.
a.puml includes common.iuml and b/b.iuml, which e.g. contains another compont and functions related to that component. The same goes for c.iuml.

### Result

1 file with all data from the 4 files above in hopefully the correct order, which is necessary for **!functions**, and only once included, which is important if you have defined a **!final function**.