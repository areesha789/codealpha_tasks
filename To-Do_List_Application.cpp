#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct Task {
    string description;
    bool completed;

    Task(string desc) {
        description = desc;
        completed = false;
    }
};

void displayMenu() {
    cout << "\n==== TO-DO LIST MENU ====\n";
    cout << "1. Add Task\n";
    cout << "2. View Tasks\n";
    cout << "3. Mark Task as Completed\n";
    cout << "4. Exit\n";
    cout << "Choose an option: ";
}

void addTask(vector<Task> &tasks) {
    cout << "Enter task description: ";
    cin.ignore(); // clear input buffer
    string desc;
    getline(cin, desc);
    tasks.push_back(Task(desc));
    cout << "Task added successfully.\n";
}

void viewTasks(const vector<Task> &tasks) {
    if (tasks.empty()) {
        cout << "No tasks available.\n";
        return;
    }

    cout << "\n---- CURRENT TASKS ----\n";
    for (size_t i = 0; i < tasks.size(); ++i) {
        cout << i + 1 << ". [" << (tasks[i].completed ? "X" : " ") << "] " << tasks[i].description << "\n";
    }
}

void markTaskCompleted(vector<Task> &tasks) {
    if (tasks.empty()) {
        cout << "No tasks to mark as completed.\n";
        return;
    }

    viewTasks(tasks);
    cout << "Enter task number to mark as completed: ";
    int num;
    cin >> num;

    if (num < 1 || num > static_cast<int>(tasks.size())) {
        cout << "Invalid task number.\n";
        return;
    }

    tasks[num - 1].completed = true;
    cout << "Task marked as completed.\n";
}

int main() {
    vector<Task> tasks;
    int choice;

    do {
        displayMenu();
        cin >> choice;

        switch (choice) {
            case 1: addTask(tasks); break;
            case 2: viewTasks(tasks); break;
            case 3: markTaskCompleted(tasks); break;
            case 4: cout << "Exiting... Goodbye!\n"; break;
            default: cout << "Invalid choice. Try again.\n";
        }

    } while (choice != 4);

    return 0;
}
