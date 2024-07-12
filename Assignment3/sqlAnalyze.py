import sqlite3
import os
import re


# Function to create the database and tables
def create_database(db_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, db_name)

    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perf_header (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comm TEXT,
            pid INTEGER,
            timestamp REAL,
            event TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perf_stack (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            header_id INTEGER,
            address TEXT,
            symbol TEXT,
            offset TEXT,
            dso TEXT,
            FOREIGN KEY (header_id) REFERENCES perf_header (id)
        )
        ''')
        conn.commit()
        conn.close()
    return db_path


# Function to parse the header line of a perf data block
def parse_header_line(line):
    pattern = re.compile(r"(\S+)\s+(\d+)\s+([\d.]+):\s+(\S+)\s+cpu-clock:")
    match = pattern.match(line)
    if match:
        comm = match.group(1)
        pid = int(match.group(2))
        timestamp = float(match.group(3))
        event = match.group(4)
        return comm, pid, timestamp, event
    return None


# Function to parse a single line of the call stack
def parse_call_stack_line(line):
    pattern = re.compile(r"\s+(\S+)\s+(\S+)\+(\S+)\s+\((\S+)\)")
    match = pattern.match(line)
    if match:
        address = match.group(1)
        symbol = match.group(2)
        offset = match.group(3)
        dso = match.group(4)
        return address, symbol, offset, dso
    return None


# Function to parse the perf data file and insert into database
def parse_and_insert_data(file_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(file_path, 'r') as file:
        header_id = None
        for line in file:
            header = parse_header_line(line)
            if header:
                cursor.execute("""
                    INSERT INTO perf_header (comm, pid, timestamp, event)
                    VALUES (?, ?, ?, ?)
                """, header)
                header_id = cursor.lastrowid
            else:
                stack = parse_call_stack_line(line)
                if stack and header_id:
                    cursor.execute("""
                        INSERT INTO perf_stack (header_id, address, symbol, offset, dso)
                        VALUES (?, ?, ?, ?, ?)
                    """, (header_id, *stack))

    conn.commit()
    conn.close()


# Function to count the top functions
def count_top_functions(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # modify LIMIT to see more functions
    cursor.execute("""
        SELECT symbol, COUNT(*) as count
        FROM perf_stack
        GROUP BY symbol
        ORDER BY count DESC
        LIMIT 10;
    """)
    top_functions = cursor.fetchall()
    print("Top Functions by Count:")
    for func in top_functions:
        print(f"Function: {func[0]}, Count: {func[1]}")

    conn.close()


# Function to analyze function duration
def analyze_function_duration(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, AVG(timestamp) as avg_time, SUM(timestamp) as total_time
        FROM perf_stack
        JOIN perf_header ON perf_stack.header_id = perf_header.id
        GROUP BY symbol
        ORDER BY total_time DESC
        LIMIT 10;
    """)
    function_durations = cursor.fetchall()
    print("Function Duration Analysis:")
    for func in function_durations:
        print(f"Function: {func[0]}, Avg Time: {func[1]}, Total Time: {func[2]}")

    conn.close()


# Function to correlate events
def correlate_events(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.symbol, b.symbol, COUNT(*) as count
        FROM perf_stack a
        JOIN perf_stack b ON a.header_id = b.header_id AND a.id != b.id
        GROUP BY a.symbol, b.symbol
        ORDER BY count DESC
        LIMIT 10;
    """)
    event_correlations = cursor.fetchall()
    print("Event Correlations:")
    for corr in event_correlations:
        print(f"Function A: {corr[0]}, Function B: {corr[1]}, Count: {corr[2]}")

    conn.close()


if __name__ == "__main__":
    db_name = "perf_data.db"
    file_path = "perf_data.txt"
    db_path = create_database(db_name)
    # parse_and_insert_data(file_path, db_path)
    print("=============TOP FUNCTIONS==================")
    count_top_functions(db_path)
    print("\n\n\n=============DURATION===================")
    analyze_function_duration(db_path)
    print("\n\n\n=============CORRELATE EVENTS==================")
    correlate_events(db_path)
