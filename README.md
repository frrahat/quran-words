# Quran Words

Simple Web app to learn words used in the Quran.

Check it out here: https://quran-words.herokuapp.com

## Features

- Navigate to a specific verse and see the words, their meanings and parts of speech.
- Get all occurrences of a word root
- See frequency of words and list all occurrences, filter the verses by taraweeh night

## Navigations

### Using URL

`/app/verses/<suraNum>/<ayahNum>?word_index=<wordIndex>` Navigates to the \<ayahNum\> of sura: \<suraNum\> and shows word analysis for word at \<wordIndex\>

### Sura / Ayah Select Dropdown

Can be used to Select a sura from list of sura. Selection will navigate to the ayah 1 of that sura. Ayah can be selected from dropdown as well.

### Key Bindings

<kbd>&uarr;</kbd> <kbd>&darr;</kbd> To navigate between the prev / next ayah of a selected sura

<kbd>&larr;</kbd> <kbd>&rarr;</kbd> To navigate between
the words in a verse

### Get Word Root Occurrences

Click on the root from the Word information table to get all occurrences of that root in the Quran

## Stack

- FastAPI for Backend
- React for Frontend
- Sqlite for databases

## Setup and Run

Build the docker images and run the server and client containers

```
docker compose -f "docker-compose.yaml" up -d --build
```

browse http://localhost:3000/app

## Lint, Typecheck, Test

### Client

Exec into the client container for typecheck, lint and prettify code

- Typecheck and lint: `yarn build`
- Prettify code: `yarn prettify`

### Server

Exec into the shell of the server container for lint, typecheck and test

- Lint: `flake8 app/ --config flake8.cfg`
- Typecheck: `mypy --config-file=mypy.ini app/`
- Test: `pytest -vvv app/tests`

## Credits

- https://gtaf.org/apps/quran for the databases
- https://quran.com for cool css styles and sura name list
- https://app.memrise.com/course/199902/80-of-quranic-words-nouns-and-verbs/ for the collection of 80% quranic words
