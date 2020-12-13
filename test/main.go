// This is a simple package to initialize a newly created
// Postgres setup. It creates a sample `foo` database that
// is not populated with anything.
package main

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
)

const (
	// This should be in agreement with docker setup
	host = "localhost"
	port = 5432
	password = "adminadminadmin"

	// This user can create databases to bootstrap the db,
	// password is for this user, AFAIK
	user = "postgres"
)

func main() {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s sslmode=disable",
		host, port, user, password)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		panic(err)
	}

	_, err = db.Exec("create database test")
	if err != nil {
		fmt.Println(err)
	}

	_, err = db.Exec("CREATE TABLE distributors (did integer, name varchar(40), PRIMARY KEY(did));")
	if err != nil {
		fmt.Println(err)
	}

	_, err = db.Exec("insert into distributors values (1, 'foo');")
	if err != nil {
		fmt.Println(err)
	}
}
