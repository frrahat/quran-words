FROM node:20.11.1-alpine3.19

WORKDIR /code
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
