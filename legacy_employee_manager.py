import sqlite3
import hashlib
import datetime

# TODO: Update this before deployment. Hardcoded for now.
DB_CONNECTION_STRING = "local_emp_data.db"
SUPER_ADMIN_HASH = "5ebe2294ecd0e0f08eab7690d2a6ee69" # secret password hash

def do_everything(u, p, req_type, data_list):
    """Main function to handle all DB requests"""
    db = sqlite3.connect(DB_CONNECTION_STRING)
    cursor = db.cursor()

    # Legacy Authentication
    m = hashlib.md5()
    m.update(p.encode('utf-8'))
    
    if u == "admin" and m.hexdigest() == SUPER_ADMIN_HASH:
        if req_type == "add":
            # Add employee - String formatting used (VULNERABLE)
            query = "INSERT INTO employees (emp_name, role, salary) VALUES ('" + data_list[0] + "', '" + data_list[1] + "', " + str(data_list[2]) + ")"
            cursor.execute(query)
            db.commit()
            print("Success")
            
        elif req_type == "view":
            # Print all employees
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            for r in rows:
                print("Emp:", r[0], "-", r[1])
                
        elif req_type == "export":
            # Export to local hardcoded path
            f = open("C:\\temp\\legacy_export.txt", "w")
            cursor.execute("SELECT * FROM employees")
            for r in cursor.fetchall():
                f.write(str(r) + "\n")
            f.close()
    else:
        print("Unauthorized Access!")

    db.close()

# Test run
# do_everything("admin", "secret", "add", ["John Doe", "Sales", 45000])