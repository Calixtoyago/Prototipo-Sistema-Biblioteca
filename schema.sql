DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "books";
DROP TABLE IF EXISTS "user_books";
DROP TABLE IF EXISTS "authors";
DROP TABLE IF EXISTS "genres";

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
    "author_id" INTEGER DEFAULT 'Unindentified',
    "genre_id" INTEGER,
    "pages" INTEGER NOT NULL,
    "year" INTEGER DEFAULT NULL,
    "ISBN" TEXT NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("author_id") REFERENCES "authors"("id") ON DELETE SET DEFAULT,
    FOREIGN KEY ("genre_id") REFERENCES "genres"("id") ON DELETE RESTRICT
);

CREATE TABLE "user_books" (
    "user_id" INTEGER,
    "book_id" INTEGER,
    "datetime" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("user_id", "book_id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
    FOREIGN KEY ("book_id") REFERENCES "books"("id") ON DELETE CASCADE
);

CREATE TABLE "authors" (
    "id" INTEGER,
    "name" TEXT UNIQUE NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE "genres" (
    "id" INTEGER,
    "genre" TEXT UNIQUE NOT NULL,
    PRIMARY KEY ("id")
);
