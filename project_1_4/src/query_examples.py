"""
    Python Real-World Projects
    Project 1.4: Local SQL Database
"""
import sqlite3
from textwrap import dedent

count_join_query = dedent("""\
    SELECT s.name, COUNT(*)
      FROM series s JOIN series_sample sv
        ON s.series_id = sv.series_id
      GROUP BY s.series_id
    """)

detail_join_query = dedent("""\
    SELECT s.name, sv.x, sv.y
      FROM series s JOIN series_sample sv ON s.series_id = sv.series_id
    """)

series_query = dedent("""\
    SELECT s.name, s.series_id
      FROM series s
    """)

detail_query = dedent("""\
    SELECT sv.x, sv.y
      FROM series_sample sv
      WHERE sv.series_id = :series_id
      ORDER BY sv.sequence
    """)

def main():
    with sqlite3.connect("file:../example.db", uri=True) as connection:
        cursor = connection.execute(count_join_query)
        for row in cursor:
            print(row)
        cursor = connection.execute(detail_join_query)
        for row in cursor:
            print(row)

        outer = connection.execute(series_query)
        for series in outer:
            print(series)
            inner = connection.execute(detail_query, {"series_id": series[1]})
            for row in inner:
                print(row)
if __name__ == "__main__":
    main()
