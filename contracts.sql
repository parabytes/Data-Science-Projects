sqlite3 contracts.db;


CREATE TABLE "contractors" (
	"id" INTEGER PRIMARY KEY ,
	"global_vendor_name" VARCHAR
);

CREATE TABLE "actions" (
	"id" INTEGER PRIMARY KEY ,
	"department" VARCHAR,
	"number_of_actions"	INTEGER,
	"dollars_obligated"	INTEGER,
	"contractor_id"	INTEGER NOT NULL,
	FOREIGN KEY("contractor_id") REFERENCES "contractors"("id")
);

