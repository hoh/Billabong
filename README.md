# Billabong

The *Billabong* project aims at providing a reliable and encrypted solution for
the storage and backup of large files that are not meant to be edited, such
as photos, videos and audio recordings.

Use *Billabong* to archive your files, and configure it to store multiple
copies of you file on different machines. Files are encrypted and their content
can be verified, so you can use untrusted computers as extra storage.

## Installation

Install *Billabong* and its main dependencies using PIP:

```
$ pip install billabong
```

No command line interface comes by default, but you can easily define one with
an alias:

```
$ alias bong="python3 -m billabong"
```



## Usage

```
Usage: bong COMMAND <options>

Available commands:
 add      Import one or several files and print resulting records.
 backup   Copy the inventory into a encrypted file on a remote system.
 blobs    List all blob ids from the first storage.
 check    Check the validity of all blobs and metadata.
 echo     Print blob content to standard output for the given record id.
 info     Print record content from one or several record ids.
 ls       List short records ids with filename from the inventory.
 mount    Mount data as a filesystem.
 pull     Pull blobs from sync storage.
 push     Push blobs to sync storage.
 records  List all records ids from the inventory.
 search   Search for the given term and return id of records matching the term.
 status   Print a global status of the inventory and storage.
 tags     List all tags from the inventory.
 version  Print software version.

Use 'bong <command> --help' for individual command help.
```

## Status

The format of the data storage is pretty reliable, and should stay compatible
with future versions.

Concerning the software itself, it is still under development. The core itself
is reaching a stable structure, and most efforts are now spent in improving the
interfaces, handling meta-data better and extending storage options.

## Data storage

*Billabong* makes a distinction between the content of the files (the *data*)
and the description of the files (the *meta-data*). When you add a file, a
random cryptographic key is generated and used to encrypt the content of the
file using AES-CTR. The key is then stored separately, together with other
meta-data such as the cryptographic hash of the original data, the hash of the
encrypted data, the file name and its size.

Here is an example of meta-data used when testing the software:
```json
{
  "datetime": "2015-08-24T21:23:18.397957",
  "timestamp": 1440444198.397957,
  "hash": "sha256-fc7d4f43945d94c874415e3bd9a6e181f8c84f8a36f586389405e391c01e48b2",
  "info": {
    "filename": "hello.txt",
    "type": "ASCII text",
    "tags": [],
    "path": "hello.txt",
    "mimetype": "text/plain"
  },
  "id": "b6a9fb49bcf54d43850d7b76182c9389",
  "blob": "87686a1e7d089c9cd63f52d90a3ea9745e587c310339b2b54329119e93a4e669",
  "key": "BT9dRpzUL+H39pFnVU2S8O1PyUEy6yq5zrYM2s2EvAE=",
  "size": 15
}
```

The meta-data is kept secure in the *inventory*, while the encrypted files
can be copied or moved freely to other computers.

![TravisCI build Status](https://api.travis-ci.org/hoh/Billabong.svg)
