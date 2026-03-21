package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/duckdb/duckdb-go/v2"
)

func main() {
	db, err := sql.Open("duckdb", "data.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS crime AS
		SELECT * FROM read_csv('data/data.csv', header = true)
	`)
	if err != nil {
		log.Fatal(err)
	}

	var (
		id   int
		name string
	)

	// Query all rows
	rows, err := db.Query(`DESCRIBE crime`)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	for rows.Next() {
		err = rows.Scan(&id, &name)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("id: %d, date: %s\n", id, name)
	}
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
}
