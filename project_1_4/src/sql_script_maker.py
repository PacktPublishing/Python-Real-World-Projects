"""
    Python Real-World Projects
    Project 1.4: Local SQL Database
"""

def write_insert(series: int, sequence: int, x: str, y: str) -> str:
    print(
        f"INSERT INTO SSAMPLES(SERIES, SEQUENCE, X, Y)"
        f"VALUES({series}, {sequence}, '{x}', '{y}')"
    )

if __name__ == "__main__":
    write_insert(1, 2, '3.0', '4.0')
    write_insert(1, 2, "'); DROP TABLE USERS;", "'); ROLLBACK;")
