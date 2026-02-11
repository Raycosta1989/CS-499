#include <iostream>
#include <string>
#include <limits>

// =========================
// Configuration Constants
// =========================
namespace Config {
    const std::string MASKED_NAME = "[REDACTED]";
    const std::string MASKED_ACCOUNT = "****12345";
    const std::string MASKED_BALANCE = "$****";
    const std::string MASKED_LAST_TX = "[REDACTED]";
    const std::string MASKED_EMAIL = "[REDACTED]";
    const std::string MASKED_PHONE = "[REDACTED]";
}

// =========================
// Customer Information Class
// =========================
class CustomerInfo {
public:
    void display() const {
        std::cout << "\n--- Customer Information ---\n";
        std::cout << "Customer Name: " << Config::MASKED_NAME << "\n";
        std::cout << "Account Number: " << Config::MASKED_ACCOUNT << "\n";
        std::cout << "Status: Active\n";
        std::cout << "Balance: " << Config::MASKED_BALANCE << "\n";
        std::cout << "Last Transaction: " << Config::MASKED_LAST_TX << "\n";
        std::cout << "Email: " << Config::MASKED_EMAIL << "\n";
        std::cout << "Phone: " << Config::MASKED_PHONE << "\n";
        std::cout << "Preferred Contact: Email\n";
        std::cout << "Membership Tier: Gold\n";
        std::cout << "Notes: Verified identity; no outstanding issues.\n";
    }
};

// =========================
// Permission Manager
// =========================
class PermissionManager {
public:
    bool userIsAdmin;

    PermissionManager(bool isAdmin = false) : userIsAdmin(isAdmin) {}

    bool hasAccess() const {
        return userIsAdmin;
    }
};

// =========================
// Menu Controller Class
// =========================
class MenuController {
private:
    CustomerInfo customer;
    PermissionManager permissions;

public:
    MenuController(bool isAdmin = false) : permissions(isAdmin) {}

    void displayMenu() const {
        std::cout << "\n=== Client Management Menu ===\n"
                  << "1) Change Customer Choice\n"
                  << "2) Display Info\n"
                  << "3) Exit\n"
                  << "Select: ";
    }

    void changeCustomerChoice() {
        std::cout << "\nChange Customer Choice\nEnter a choice (1-5): ";

        int input = 0;
        if (!(std::cin >> input)) {
            handleInvalidInput();
            return;
        }

        if (input < 1 || input > 5) {
            std::cout << "Invalid choice.\n";
            return;
        }

        std::cout << "Customer choice updated to: " << input << "\n";
    }

    void handleInvalidInput() const {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Invalid input.\n";
    }

    void run() {
        while (true) {
            displayMenu();

            int choice = 0;
            if (!(std::cin >> choice)) {
                handleInvalidInput();
                continue;
            }

            switch (choice) {
                case 1:
                    changeCustomerChoice();
                    break;

                case 2:
                    if (permissions.hasAccess()) {
                        customer.display();
                    } else {
                        std::cout << "Permission denied.\n";
                    }
                    break;

                case 3:
                    std::cout << "Exiting program.\n";
                    return;

                default:
                    std::cout << "Unknown option.\n";
            }
        }
    }
};

// =========================
// Main Entry Point
// =========================
int main() {
    std::cout << "Created by Raymond Costa - Enhanced Version\n";

    MenuController controller(false); // false = non-admin user
    controller.run();

    return 0;
}
