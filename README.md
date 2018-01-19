# specimen-tools

`specimen-tools` contains code related to the iOS application 
[Specimen](https://itunes.apple.com/us/app/specimen-a-game-about-color/).
This can be used to: build a SQLite database of Specimen data, query it, and
includes additional utilities for simple things like plotting common
color-related data.

In order to avoid additional spamming of the original Specimen authors, 
for access to the underlying Specimen data, please reach out to 
Jose Cambronero (jcamsan@mit.edu). Access to the data is decided on a
case-by-case basis and there is no guarantee of approval. Applications
related to research or open-source experimentation are encouraged.

# Requirements
`specimen-tools` assumes you have access to:

* Python 2.*
* SQLite

Most *nix systems come with SQLite installed, and should satisfy this
requirement with no additional work. If this is not the case, please
see [SQlite](https://sqlite.org/) for the appropriate way to install 
on your system. On Linux, this should be as simple as
`sudo apt-get install sqlite3`. On Mac OSX, with homebrew,
the same command is `sudo brew install sqlite3`.

The necessary Python libraries are installed automatically.


# Installation and Basic Usage
Assuming you have satisfied the requirements above,
in order to install `specimen-tools`, you can use `pip`

```
sudo pip install specimen-tools
```

Or you can copy this repository and build locally

```
git clone https://github.com/josepablocam/specimen-tools.git
cd specimen-tools/
pip install -e .
```

This installs the `specimen` module. Note that this does not build
the database. In order to do so, you need to explicitly execute
`specimen-tools/scripts/build_db.py` (which is only included
in the repository). Additionally, you will need to have access
to the raw Specimen data to build the database. The database
built is a SQLite database, which means it is serverless and
consists of a single file.


## Acknowledgements
We thank Erica Gorochow, Salvatore Randazzo, and Charlie Whitney
for providing access to the Specimen dataset and for building
the Specimen application.
