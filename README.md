# plantumlInliner

This is a small script that will help to merge all subsequent PlantUML-files that are included by the **!include**-directive.

Usually, I work with an oo-approach of define once and use everywhere for my PlantUML definition of components and sequences. So, sometimes a single file includes 5, 10 or 50 other files. However, sometimes I need a single file that I can share with someone or even use with the PlantUML Confluence plugin. This script does the job for me.

There are no frills and no guarantee. It worked for me with Python 3.8.2

## Usage

**python.exe inliner.py** **--path** _"c:/path/to/folder/"_ **--input** _firstFile.puml_ **--output** _output.puml_ 

## Example

There is a tiny example in the (manual) test folder.

### Given

4 files a.puml, b.iuml, c.iuml and common.iuml.
Common.iuml has information such as variables, functions or whatever needed in any other file.
a.puml includes common.iuml and b/b.iuml, which e.g. contains another compont and functions related to that component. The same goes for c.iuml.

```plantuml
file a.puml
folder "b"{
    file b.iuml
    folder "c" {
        file c.iuml
        }
         b.iuml -- c.iuml : 3rd include
}
file common.iuml
 a.puml -- common.iuml : 1st include
 a.puml -- b.iuml : 2nd include
```

### Result

1 file with all data from the 4 files above in hopefully the correct order, which is necessary for **!functions**, and only once included, which is important if you have defined a **!final function**.
```plantuml
file output.puml{
    note as content #LightYellow
    content of a.puml
    content of common.iuml
    content of b.iuml
    content of c.iuml
end note
}
```