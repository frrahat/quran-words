# Quran Words

Simple Web app to learn words used in the Quran.

## Features

Navigate to a specific verse and see the words, their meanings and parts of speech.

## Navigations

### Using URL
`/verses/<suraNum>/<ayahNum>?word_index=<wordIndex>` Navigates to the \<ayahNum\> of sura: \<suraNum\> and shows word analysis for word at \<wordIndex\>

### Sura Select Dropdown
Can be used to Select a sura from list of sura. Selection will navigate to the ayah 1 of that sura.

### Key Bindings
<kbd>&uarr;</kbd> <kbd>&darr;</kbd> To navigate between the prev / next ayah of a selected sura

<kbd>&larr;</kbd> <kbd>&rarr;</kbd> To navigate between
the words in a verse

## Stack
- FastAPI for Backend
- React for Frontend
- Sqlite for databases

## Setup and Run
Need to a create a virtual env first for python

To setup dependencies for both frontend and backend
```sh
make setup
````

To run frontend and backend parallelly
```sh
make start-all -j2
```

To Run server only
```sh
make server-start
```

To Run client only
```sh
make client-start
```

To Run lint
```sh
make lint
```

To Run typecheck on server
```sh
make typecheck
```

To Run test
```sh
make test
```

## Credits
- https://gtaf.org/apps/quran for the databases
- quran.com for cool css styles and sura name list
- https://app.memrise.com/course/199902/80-of-quranic-words-nouns-and-verbs/ for the collection of 80% quranic words
