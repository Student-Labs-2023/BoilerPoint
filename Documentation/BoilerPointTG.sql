CREATE TABLE "DataUsers" (
  "chat_id" int UNIQUE PRIMARY KEY,
  "full_name" varchar,
  "age" int,
  "gender" bool,
  "balance" int,
  "user_state" varchar,
  "tgusr" varchar
);

CREATE TABLE "Report" (
  "tgusr" varchar UNIQUE PRIMARY KEY,
  "description" varchar
);

CREATE TABLE "Promocode" (
  "promo" varchar UNIQUE PRIMARY KEY,
  "last" int,
  "cost" int
);

CREATE TABLE "UsedPromocode" (
  "id" int UNIQUE PRIMARY KEY,
  "promo" varchar,
  "chat_id" int
);

CREATE TABLE "Event" (
  "id" int PRIMARY KEY,
  "date_start" varchar,
  "date_end" varchar,
  "full_name" varchar
);

CREATE TABLE "TaskCollection" (
  "name" varchar UNIQUE PRIMARY KEY,
  "description" varchar,
  "photo" varchar,
  "counter" int,
  "url" varchar,
  "numberPoints" varchar,
  "rightAnswers" varchar
);

CREATE TABLE "Passd" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "chat_id" int
);

ALTER TABLE "DataUsers" ADD FOREIGN KEY ("chat_id") REFERENCES "UsedPromocode" ("chat_id");

ALTER TABLE "DataUsers" ADD FOREIGN KEY ("tgusr") REFERENCES "Report" ("tgusr");

ALTER TABLE "Promocode" ADD FOREIGN KEY ("promo") REFERENCES "UsedPromocode" ("promo");

ALTER TABLE "TaskCollection" ADD FOREIGN KEY ("name") REFERENCES "Passd" ("name");

ALTER TABLE "DataUsers" ADD FOREIGN KEY ("chat_id") REFERENCES "Passd" ("chat_id");
