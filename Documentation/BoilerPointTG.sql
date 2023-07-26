CREATE TABLE "DataUsers" (
  "chat_id" int UNIQUE PRIMARY KEY,
  "full_name" varchar,
  "age" int,
  "gender" bool,
  "balance" int,
  "user_state" varchar,
  "tgusr" varchar
);

CREATE TABLE "Pointer" (
  "chat_id" int UNIQUE PRIMARY KEY,
  "counter" int
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

CREATE TABLE "AdminTasks" (
  "counter" int PRIMARY KEY,
  "name" varchar,
  "description" varchar
);

ALTER TABLE "DataUsers" ADD FOREIGN KEY ("chat_id") REFERENCES "Pointer" ("chat_id");

ALTER TABLE "DataUsers" ADD FOREIGN KEY ("chat_id") REFERENCES "UsedPromocode" ("chat_id");

ALTER TABLE "Promocode" ADD FOREIGN KEY ("promo") REFERENCES "UsedPromocode" ("promo");

ALTER TABLE "AdminTasks" ADD FOREIGN KEY ("counter") REFERENCES "Pointer" ("counter");
