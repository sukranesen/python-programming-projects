
def print_output(text):
    print(text)

def calculate_column_widths(columns, rows):
    widths = []
    for col in columns:
        widths.append(len(col))

    for row in rows:
        for i in range(len(row)):
            if len(row[i]) > widths[i]:
                widths[i] = len(row[i])

    return widths

def print_table_format(tables, table_name):
    table = tables[table_name]
    columns = table["columns"]
    rows = table["rows"]
    col_widths = calculate_column_widths(columns, rows)

    separator = "+".join(["-" * (width + 2) for width in col_widths])
    header = "|".join([f" {columns[i].ljust(col_widths[i])} " for i in range(len(columns))])

    print_output(f"Table: {table_name}")
    print_output(f"+{separator}+")
    print_output(f"|{header}|")
    print_output(f"+{separator}+")
    for row in rows:
        formatted_row = "|".join([f" {row[i].ljust(col_widths[i])} " for i in range(len(row))])
        print_output(f"|{formatted_row}|")
    print_output(f"+{separator}")

def parse_conditions(condition_str):
    condition_str = condition_str.strip("{}")
    conditions = {}
    for pair in condition_str.split(","):
        if ":" in pair:
            key, value = pair.split(":")
            conditions[key.strip().strip('"')] = value.strip().strip('"')
    return conditions

def create_table(tables, command):
    parts = command.split(maxsplit=2)
    table_name = parts[1]
    columns = parts[2].split(",")
    if table_name in tables:
        print_output(f"Table '{table_name}' already exists.")
        return
    tables[table_name] = {"columns": columns, "rows": []}
    print_output(f"###################### CREATE #########################")
    print_output(f"Table '{table_name}' created with columns: {columns}")
    print_output(f"#######################################################\n")

def insert(tables, command):
    parts = command.split(maxsplit=2)
    table_name = parts[1]
    values = parts[2].split(",")
    if table_name not in tables:
        print_output(f"###################### INSERT #########################")
        print_output(f"Table {table_name} not found")
        print_output(f"Inserted into '{table_name}': {tuple(values)}")
        print_output(f"#######################################################\n")
        return
    table = tables[table_name]
    if len(values) != len(table["columns"]):
        print_output(f"Column count does not match table schema in '{table_name}'.")
        return
    tables[table_name]["rows"].append(values)
    print_output(f"###################### INSERT #########################")
    print_output(f"Inserted into '{table_name}': {tuple(values)}\n")
    print_table_format(tables, table_name)
    print_output(f"#######################################################\n")

def select(tables, command):
    parts = command.split(maxsplit=3)
    table_name = parts[1]
    columns = parts[2].split(",")
    condition = parse_conditions(parts[3].split("WHERE ", 1)[1]) if "WHERE" in command else {}

    if table_name not in tables:
        print_output(f"###################### SELECT #########################")
        print_output(f"Table {table_name} not found")
        print_output(f"Condition: {condition}")
        print_output(f"Select result from '{table_name}': None")
        print_output(f"#######################################################\n")
        return

    table = tables[table_name]

    if any(col not in table["columns"] for col in columns):
        return

    for key in condition.keys():
        if key not in table["columns"]:
            print_output(f"###################### SELECT #########################")
            print_output(f"Column {key} does not exist")
            print_output(f"Condition: {condition}")
            print_output(f"Select result from '{table_name}': None")
            print_output(f"#######################################################\n")
            return

    rows = table["rows"]
    selected_rows = []
    for row in rows:
        match = all(str(row[table["columns"].index(k)]) == v for k, v in condition.items())
        if match:
            selected_rows.append(row)

    result = [[row[table["columns"].index(col)] for col in columns] for row in selected_rows]
    print_output(f"###################### SELECT #########################")
    print_output(f"Condition: {condition}")
    print_output(f"Select result from '{table_name}': {result}")
    print_output(f"#######################################################\n")

def update(tables, command):
    parts = command.split(" ", 3)
    table_name = parts[1]
    updates = parse_conditions(parts[2].strip())
    condition = parse_conditions(parts[3].split("WHERE ", 1)[1].strip())
    if table_name not in tables:
        print_output(f"###################### UPDATE #########################")
        print_output(f"Updated '{table_name}' with {updates} where {condition}")
        print_output(f"Table '{table_name}' not found")
        print_output(f"0 rows updated.")
        print_output(f"#######################################################\n")

        return
    table = tables[table_name]

    for key in updates.keys():
        if key not in table["columns"]:
            print_output(f"###################### UPDATE #########################")
            print_output(f"Updated '{table_name}' with {updates} where {condition}")
            print_output(f"Column {key} does not exist")
            print_output(f"0 rows updated.\n")
            print_table_format(tables, table_name)
            print_output(f"#######################################################\n")
            return

    for key in condition.keys():
        if key not in table["columns"]:
            print_output(f"###################### UPDATE #########################")
            print_output(f"Updated '{table_name}' with {updates} where {condition}")
            print_output(f"Column {key} does not exist")
            print_output(f"0 rows updated.\n")
            print_table_format(tables, table_name)
            print_output(f"#######################################################\n")
            return

    rows_updated = 0
    for row in table["rows"]:
        match = all(str(row[table["columns"].index(k)]) == v for k, v in condition.items())
        if match:
            for key, value in updates.items():
                col_index = table["columns"].index(key)
                row[col_index] = value
            rows_updated += 1
    print_output(f"###################### UPDATE #########################")
    print_output(f"Updated '{table_name}' with {updates} where {condition}")
    print_output(f"{rows_updated} rows updated.\n")
    print_table_format(tables, table_name)
    print_output(f"#######################################################\n")

def delete(tables, command):
    parts = command.split(" ", 3)
    table_name = parts[1]

    if len(parts) > 3 and "WHERE" in parts[3]:
        condition = parse_conditions(parts[3].split("WHERE ", 1)[1].strip())
    else:
        condition = {}

    if table_name not in tables:
        print_output("###################### DELETE #########################")
        print_output("Deleted from '" + table_name + "' where " + str(condition))
        print_output("Table " + table_name + " not found.")
        print_output("0 rows deleted.")
        print_output("#######################################################\n")
        return

    table = tables[table_name]

    for key in condition.keys():
        if key not in table["columns"]:
            print_output("###################### DELETE #########################")
            print_output("Deleted from '" + table_name + "' where " + str(condition))
            print_output("Column " + key + " does not exist")
            print_output("0 rows deleted.")
            print_table_format(tables, table_name)  # Tabloyu yazdırıyoruz
            print_output("#######################################################\n")
            return

    initial_count = len(table["rows"])
    filtered_rows = []
    for row in table["rows"]:
        match = True
        for k, v in condition.items():
            col_index = table["columns"].index(k)
            if str(row[col_index]) != v:
                match = False
                break
        if match:
            filtered_rows.append(row)

    table["rows"] = filtered_rows
    deleted_count = initial_count - len(table["rows"])  # Kaç satır silindi?

    print_output("###################### DELETE #########################")
    print_output("Deleted from '" + table_name + "' where " + str(condition))
    print_output(str(deleted_count) + " rows deleted.\n")
    print_table_format(tables, table_name)
    print_output("#######################################################\n")


def join_tables(tables, command):

    parts = command.split(" ", 2)

    table_part, condition_part = parts[1], parts[2]
    table_names = table_part.split(",")
    table1_name, table2_name = table_names

    if table1_name not in tables or table2_name not in tables:
        print_output("####################### JOIN ##########################")
        print_output("Join tables " + table1_name + " and " + table2_name)
        print_output("Table does not exist")
        print_output("#######################################################\n")
        return

    condition = condition_part.split("ON", 1)[1].strip()

    table1 = tables[table1_name]
    table2 = tables[table2_name]

    if condition not in table1["columns"] or condition not in table2["columns"]:
        print_output("####################### JOIN ##########################")
        print_output("Join tables " + table1_name + " and " + table2_name)
        print_output("Column " + condition + " does not exist")
        print_output("#######################################################\n")
        return

    col_index1 = table1["columns"].index(condition)
    col_index2 = table2["columns"].index(condition)

    joined_rows = []
    for row1 in table1["rows"]:
        for row2 in table2["rows"]:
            if row1[col_index1] == row2[col_index2]:
                filtered_row2 = [val for idx, val in enumerate(row2) if idx != col_index2]
                joined_rows.append(row1 + filtered_row2)

    joined_columns = table1["columns"] + [col for idx, col in enumerate(table2["columns"]) if idx != col_index2]

    if not joined_rows:
        print_output("####################### JOIN ##########################")
        print_output("Join tables " + table1_name + " and " + table2_name)
        print_output("No rows matched the join condition.\n")
        print_output("#######################################################\n")
        return

    print_output("####################### JOIN ##########################")
    print_output("Join tables " + table1_name + " and " + table2_name)
    print_output("Join result (" + str(len(joined_rows)) + " rows):\n")

    joined_table = {"columns": joined_columns, "rows": joined_rows}
    print_table_format({"Joined Table": joined_table}, "Joined Table")
    print_output("#######################################################\n")

def count(tables, command):
    parts = command.split(" ", 3)
    table_name = parts[1]

    if "WHERE" in parts[3]:
        condition = parse_conditions(parts[3].split("WHERE ", 1)[1].strip())
    else:
        condition = {}

    if table_name not in tables:
        print_output("###################### COUNT #########################")
        print_output("Table " + table_name + " not found")
        print_output("Total number of entries in '" + table_name + "' is 0")
        print_output("#######################################################\n")
        return

    table = tables[table_name]
    for key in condition.keys():
        if key not in table["columns"]:
            print_output("###################### COUNT #########################")
            print_output("Column " + key + " does not exist")
            print_output("Total number of entries in '" + table_name + "' is 0")
            print_output("#######################################################\n")
            return

    rows = table["rows"]
    count_result = 0
    for row in rows:
        match = True
        for k, v in condition.items():
            col_index = table["columns"].index(k)
            if str(row[col_index]) != v:
                match = False
                break
        if match:
            count_result += 1

    print_output("###################### COUNT #########################")
    print_output("Count: " + str(condition))
    print_output("Total number of entries in '" + table_name + "' is " + str(count_result))
    print_output("#######################################################\n")

import sys

def main():

    input_file = sys.argv[1]
    tables = {}

    try:
        with open(input_file, 'r') as f:
            for line in f:
                command = line.strip()
                if command:
                    if command.startswith("CREATE"):
                        create_table(tables, command)
                    elif command.startswith("INSERT"):
                        insert(tables, command)
                    elif command.startswith("SELECT"):
                        select(tables, command)
                    elif command.startswith("UPDATE"):
                        update(tables, command)
                    elif command.startswith("DELETE"):
                        delete(tables, command)
                    elif command.startswith("JOIN"):
                        join_tables(tables, command)
                    elif command.startswith("COUNT"):
                        count(tables, command)
                    else:
                        print_output("Unknown command.")

    except Exception as e:
        print_output("An unexpected error!")

if __name__ == "__main__":
    main()
