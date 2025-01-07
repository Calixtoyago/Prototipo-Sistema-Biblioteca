DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "books";
DROP TABLE IF EXISTS "user_books";
DROP TABLE IF EXISTS "authors";

CREATE TABLE "users" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "email" TEXT NOT NULL UNIQUE,
    "number" TEXT NOT NULL UNIQUE,
    "type" TEXT CHECK("type" = 'admin' OR "type" = 'normal'),
    PRIMARY KEY ("id")
);

CREATE TABLE "books" (
    "id" INTEGER,
    "title" TEXT NOT NULL UNIQUE,
    "author_id" INTEGER,
    "pages" INTEGER NOT NULL,
    "year" INTEGER DEFAULT NULL,
    "ISBN" TEXT NOT NULL,
    "genre"TEXT NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("author_id") REFERENCES "authors"("id")
);

CREATE TABLE "user_books" (
    "user_id" INTEGER,
    "book_id" INTEGER,
    "datetime" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    FOREIGN KEY ("book_id") REFERENCES "books"("id")
);

CREATE TABLE "authors" (
    "id" INTEGER,
    "name" TEXT UNIQUE NOT NULL,
    PRIMARY KEY ("id")
)
