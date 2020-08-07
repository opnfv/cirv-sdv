## Program Settings handler

Settings will be loaded from several ```.yaml``` or ```.yml``` files and any user provided settings files.

So, that user can use these settings values across program.



This utility loads settings from yaml files in form of key and value where key is always ```string``` while value can be of type python:

* ```int``` e.g. 5, 45, 1234
* ```str``` e.g. hello, world
* ```float``` e.g. 34.56, 12.7
* ```list``` e.g. [ 'month' , 'is', 45 ]
* ```dict``` e.g. {'program': 'sdv', 'language': 'python'}
* ```bool``` e.g. True, False



#### keys are case-insensitive

The utility is case-insensitive to keys used as it automatically converts all keys to lower case.

E.g. ```Program : sdv```, ```program : sdv```, ```PrOgRam : sdv``` all are same.



* ```settings.load_from_file(path/to/file)```
* ```settings.load_from_env()```
* ```settings.load_from_dir(directory/to/search/yamls)```

```settings.load_from_dir()``` reads all yaml files in given directory and all it's sub-directory recursively in ascending order, hence if a configuration item exists in more than one file, then the setting in the file that occurs in the last read file will have high precedence and overwrite previous values. .



