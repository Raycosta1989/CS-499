#include <iostream>
#include <string>
#include <limits>

// Vulnerability: Global mutable state variable can be insecure in larger systems.
// FIX: For demonstration, we keep it but note that encapsulation in a class or local scope is preferred.
static int state = 0;

// --- Helper routines inferred from LEA + CALL patterns ---
void SetupA() { /* initialize buffers/resources */ }
void SetupB() { /* print banner or intro text */ }
void SetupC() { /* load defaults */ }

// DisplayInfo: linear chain of output-like calls
void DisplayInfo() {
    std::cout << "\n--- Customer Information ---" << std::endl;

    // Vulnerability: Hardcoded sensitive data (PII).
    // FIX: Replace with masked or placeholder values.
    std::cout << "Customer Name: [REDACTED]" << std::endl;
    std::cout << "Account Number: ****12345" << std::endl;
    std::cout << "Status: Active" << std::endl;
    std::cout << "Balance: $****" << std::endl;
    std::cout << "Last Transaction: [REDACTED]" << std::endl;
    std::cout << "Email: [REDACTED]" << std::endl;
    std::cout << "Phone: [REDACTED]" << std::endl;
    std::cout << "Preferred Contact: Email" << std::endl;
    std::cout << "Membership Tier: Gold" << std::endl;
    std::cout << "Notes: Verified identity; no outstanding issues." << std::endl;
}

// ChangeCustomerChoice: prompts and confirms choices 1..5
void ChangeCustomerChoice() {
    std::cout << "\nChange Customer Choice" << std::endl;
    std::cout << "Enter a choice (1-5): ";

    int input = 0;
    if (!(std::cin >> input)) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Invalid input." << std::endl;
        return;
    }

    // Vulnerability: No bounds check for input.
    // FIX: Add explicit range validation.
    if (input >= 1 && input <= 5) {
        state = input;
    } else {
        std::cout << "Invalid choice." << std::endl;
    }
}

// CheckUserPermissionAccess: returns 1 (granted) or 2 (denied)
int CheckUserPermissionAccess() {
    // Vulnerability: Always grants access (logic flaw).
    // FIX: Implement placeholder role check.
    bool userIsAdmin = false; // Example: replace with real validation
    if (userIsAdmin) {
        return 1; // granted
    } else {
        return 2; // denied
    }
}

// Simple menu display
void DisplayMenu() {
    std::cout << "\n=== Client Management Menu ===\n"
              << "1) Change Customer Choice\n"
              << "2) Display Info\n"
              << "3) Exit\n"
              << "Select: ";
}

int main() {
    std::cout << "Created by Raymond Costa - Reverse Engineering Proficiency Test" << std::endl;

    SetupA();
    SetupB();
    SetupC();

    while (true) {
        DisplayMenu();

        int choice;
        // Vulnerability: Direct assignment to global state without validation.
        // FIX: Validate input before assigning.
        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Invalid input." << std::endl;
            continue;
        }

        if (choice < 1 || choice > 3) {
            std::cout << "Unknown option. Try again." << std::endl;
            continue;
        }

        state = choice;

        // cmp $0x1 → handler for option 1
        if (state == 1) {
            ChangeCustomerChoice();
        }
        // cmp $0x2 → handler for option 2
        else if (state == 2) {
            int perm = CheckUserPermissionAccess();
            if (perm == 1) {
                DisplayInfo();
            } else {
                std::cout << "Permission denied to display info." << std::endl;
            }
        }
        // cmp $0x3 → exit
        else if (state == 3) {
            break;
        }
    }

    return 0;
}