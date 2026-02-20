#include <iostream>
#include <string>
#include "sqlite3.h"

using namespace std;

sqlite3 *db;

// Execute SQL
bool executeSQL(const string &sql) {

    char *errMsg = nullptr;

    int rc = sqlite3_exec(db, sql.c_str(), 0, 0, &errMsg);

    if (rc != SQLITE_OK) {

        cout << "ERROR: " << errMsg << endl;
        sqlite3_free(errMsg);
        return false;
    }

    return true;
}


// Initialize database
void initDB() {

    int rc = sqlite3_open("bank.db", &db);

    if (rc) {

        cout << "ERROR: Cannot open database\n";
        exit(1);
    }

    string createAccounts =
        "CREATE TABLE IF NOT EXISTS accounts ("
        "accNo INTEGER PRIMARY KEY,"
        "name TEXT,"
        "pin INTEGER,"
        "balance REAL DEFAULT 0);";

    string createTransactions =
        "CREATE TABLE IF NOT EXISTS transactions ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "accNo INTEGER,"
        "type TEXT,"
        "amount REAL,"
        "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);";

    executeSQL(createAccounts);
    executeSQL(createTransactions);
}


// Authenticate user
bool authenticate(int accNo, int pin) {

    string sql =
        "SELECT accNo FROM accounts WHERE accNo=" +
        to_string(accNo) +
        " AND pin=" +
        to_string(pin) +
        ";";

    bool found = false;

    auto callback = [](void *data, int argc, char **argv, char **colName) {

        bool *found = (bool *)data;
        *found = true;
        return 0;
    };

    sqlite3_exec(db, sql.c_str(), callback, &found, nullptr);

    return found;
}


// Get balance
double getBalance(int accNo) {

    string sql =
        "SELECT balance FROM accounts WHERE accNo=" +
        to_string(accNo);

    double balance = 0;

    auto callback = [](void *data, int argc, char **argv, char **colName) {

        double *balance = (double *)data;

        if (argv[0])
            *balance = atof(argv[0]);

        return 0;
    };

    sqlite3_exec(db, sql.c_str(), callback, &balance, nullptr);

    return balance;
}


// MAIN
int main(int argc, char *argv[]) {

    initDB();

    if (argc < 2) {

        cout << "ERROR: Invalid command\n";
        return 0;
    }

    string command = argv[1];


    // CREATE ACCOUNT
    if (command == "create") {

        int accNo = stoi(argv[2]);
        string name = argv[3];
        int pin = stoi(argv[4]);

        string check =
            "SELECT accNo FROM accounts WHERE accNo=" +
            to_string(accNo);

        bool exists = false;

        auto callback = [](void *data, int argc, char **argv, char **colName) {

            bool *exists = (bool *)data;
            *exists = true;
            return 0;
        };

        sqlite3_exec(db, check.c_str(), callback, &exists, nullptr);

        if (exists) {

            cout << "ERROR: Account already exists\n";
            return 0;
        }

        string sql =
            "INSERT INTO accounts (accNo,name,pin,balance) VALUES (" +
            to_string(accNo) +
            ",'" +
            name +
            "'," +
            to_string(pin) +
            ",0);";

        executeSQL(sql);

        cout << "SUCCESS: Account created\n";
    }


    // BALANCE
    else if (command == "balance") {

        int accNo = stoi(argv[2]);
        int pin = stoi(argv[3]);

        if (!authenticate(accNo, pin)) {

            cout << "ERROR: Invalid credentials\n";
            return 0;
        }

        double balance = getBalance(accNo);

        cout << "Balance: " << balance << endl;
    }


    // DEPOSIT
    else if (command == "deposit") {

        int accNo = stoi(argv[2]);
        int pin = stoi(argv[3]);
        double amount = stod(argv[4]);

        if (!authenticate(accNo, pin)) {

            cout << "ERROR: Invalid credentials\n";
            return 0;
        }

        string update =
            "UPDATE accounts SET balance = balance + " +
            to_string(amount) +
            " WHERE accNo=" +
            to_string(accNo);

        executeSQL(update);

        string trans =
            "INSERT INTO transactions (accNo,type,amount,timestamp) VALUES (" +
            to_string(accNo) +
            ",'Deposited'," +
            to_string(amount) +
            ",datetime('now','localtime'));";

        executeSQL(trans);

        cout << "SUCCESS: Deposit complete\n";
    }


    // WITHDRAW
    else if (command == "withdraw") {

        int accNo = stoi(argv[2]);
        int pin = stoi(argv[3]);
        double amount = stod(argv[4]);

        if (!authenticate(accNo, pin)) {

            cout << "ERROR: Invalid credentials\n";
            return 0;
        }

        double balance = getBalance(accNo);

        if (amount > balance) {

            cout << "ERROR: Insufficient balance\n";
            return 0;
        }

        string update =
            "UPDATE accounts SET balance = balance - " +
            to_string(amount) +
            " WHERE accNo=" +
            to_string(accNo);

        executeSQL(update);

        string trans =
            "INSERT INTO transactions (accNo,type,amount,timestamp) VALUES (" +
            to_string(accNo) +
            ",'Withdrawn'," +
            to_string(amount) +
            ",datetime('now','localtime'));";

        executeSQL(trans);

        cout << "SUCCESS: Withdraw complete\n";
    }


    // HISTORY
    else if (command == "history") {

        int accNo = stoi(argv[2]);
        int pin = stoi(argv[3]);

        if (!authenticate(accNo, pin)) {

            cout << "ERROR: Invalid credentials\n";
            return 0;
        }

        string sql =
            "SELECT type, amount, timestamp FROM transactions "
            "WHERE accNo=" +
            to_string(accNo) +
            " ORDER BY timestamp DESC;";

        auto callback = [](void *data, int argc, char **argv, char **colName) {

            cout << argv[0]
                 << ": "
                 << argv[1]
                 << " at "
                 << argv[2]
                 << endl;

            return 0;
        };

        sqlite3_exec(db, sql.c_str(), callback, nullptr, nullptr);
    }


    else {

        cout << "ERROR: Unknown command\n";
    }

    sqlite3_close(db);

    return 0;
}
