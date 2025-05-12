#include <iostream>
#include <cmath>
#include <iomanip>
#include <limits>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

struct PaymentDetail {
    int month;
    double emi;
    double principal;
    double interest;
    double remaining;
};

double calculateEMI(double principal, double annualRate, int years);
vector<PaymentDetail> generatePaymentSchedule(double principal, double annualRate, int years, double emi);
void displayMainResults(double principal, double annualRate, int years, double emi);
void displayPaymentSchedule(const vector<PaymentDetail>& schedule, int totalMonths);
void displayCorrectChart(const vector<PaymentDetail>& schedule);
float getValidatedInput(const string& prompt, float min, float max);
int getValidatedIntegerInput(const string& prompt, int min, int max);
char getYesNoInput(const string& prompt);

int main() {
    cout << "LOAN EMI CALCULATOR REQUIREMENTS:-\n";
    cout<<endl;
   
    double principal = getValidatedInput("Enter principal amount: ", 100, 100000000);// Annual principal value i.e, Rs.
    double annualRate = getValidatedInput("Enter rate of interest: ", 1, 70);// Annual Rate i.e, %
    int years = getValidatedIntegerInput("Enter total loan tenure : ", 1, 40);// Annual time i.e, years

    double emi = calculateEMI(principal, annualRate, years);
    vector<PaymentDetail> paymentSchedule = generatePaymentSchedule(principal, annualRate, years, emi);

    displayMainResults(principal, annualRate, years, emi);

    char choice = getYesNoInput("Would you like to see the payment schedule? (yes/no): ");
    if (tolower(choice) == 'y') {
        displayPaymentSchedule(paymentSchedule, years * 12);
    }

    choice = getYesNoInput("Would you like to see an Correctchart? (yes/no): ");
    if (tolower(choice) == 'y') {
        displayCorrectChart(paymentSchedule);
    }

    cout << "Thank you for using the EMI Calculator!\n";
    return 0;
}

double calculateEMI(double principal, double  annualRate, int years) {
    if (principal <= 0 || years <= 0) return 0;

    double monthlyRate = annualRate / 12 / 100;
    int months = years * 12;

   if (monthlyRate == 0) {
        return principal / months;
    }

   if (monthlyRate < 0.0001) {
        double temp = monthlyRate * months;
        return principal * (monthlyRate + temp / months + (temp * temp) / (2 * months * months));
    }

    return (principal * monthlyRate * pow(1 + monthlyRate, months)) / 
           (pow(1 + monthlyRate, months) - 1);
}

vector<PaymentDetail> generatePaymentSchedule(double  principal, double annualRate, int years, double emi) {
    vector<PaymentDetail> schedule;
    double monthlyRate = annualRate / 12 / 100;
    int months = years * 12;
    double remaining = principal;

    for (int month = 1; month <= months; month++) {
        double interest = remaining * monthlyRate;
        double principalPaid = emi - interest;
        remaining -= principalPaid;

      if (month == months || remaining < 1) {
            principalPaid += remaining;
            remaining = 0;
        }

        PaymentDetail detail;
        detail.month = month;
        detail.emi = emi;
        detail.principal = principalPaid;
        detail.interest = interest;
        detail.remaining = remaining >= 0 ? remaining : 0;

        schedule.push_back(detail);
    }

    return schedule;
}

void displayMainResults(double  principal, double annualRate, int years, double emi) {
    int months = years * 12;
    double totalPayment = emi * months;
    double totalInterest = totalPayment - principal;
    double interestPercentage = (totalInterest / principal) * 100;

    cout << fixed << setprecision(2);
    cout << " LOAN DETAILS:-\n";
    cout<<endl;
    cout << left << setw(25) << "Principal Amount:" << right << setw(15) << principal << "\n";
    cout << left << setw(25) << "Annual Interest Rate:" << right << setw(14) << annualRate << "%\n";
    cout << left << setw(25) << "Loan Tenure:" << right << setw(12) << years << " years (" << months << " months)\n";
    cout << endl;
    cout << left << setw(25) << "Monthly EMI:" << right << setw(15) << emi << "\n";
    cout << left << setw(25) << "Total Payment:" << right << setw(15) << totalPayment << "\n";
    cout << left << setw(25) << "Total Interest:" << right << setw(15) << totalInterest << "\n";
    cout << left << setw(25) << "Interest Percentage:" << right << setw(14) << interestPercentage << "%\n";
    cout << endl;
}

void displayPaymentSchedule(const vector<PaymentDetail>& schedule, int totalMonths) {
    const int entriesPerPage = 12;
    int currentPage = 0;
    int totalPages = (totalMonths + entriesPerPage - 1) / entriesPerPage;
    char choice;

    do {
        cout << "PAYMENT SCHEDULE (Page " << currentPage + 1 << " of " << totalPages << ")\n";
        cout << "Month\tEMI\t\tPrincipal\tInterest\tRemaining\n";

        int start = currentPage * entriesPerPage;
        int end = min(start + entriesPerPage, totalMonths);

        for (int i = start; i < end; i++) {
            const PaymentDetail& detail = schedule[i];
            cout << detail.month << "\t" << detail.emi << "\t" << detail.principal 
                 << "\t\t" << detail.interest << "\t\t" << detail.remaining << "\n";
        }

        if (totalPages > 1) {
            cout << "Press 'n' for next page, 'p' for previous page, or 'q' to quit:\n ";
            cin >> choice;
            choice = tolower(choice);

            if (choice == 'n' && currentPage < totalPages - 1) {
                currentPage++;
            } else if (choice == 'p' && currentPage > 0) {
                currentPage--;
            } else if (choice != 'q') {
                cout << "Invalid choice. Please try again.\n";
            }
        } else {
            break;
        }
    } while (choice != 'q');
}

void displayCorrectChart(const vector<PaymentDetail>& schedule) {
    const int chartWidth = 50;
    double maxPrincipal = max_element(schedule.begin(), schedule.end(), 
        [](const PaymentDetail& a, const PaymentDetail& b) {
            return a.principal < b.principal;
        })->principal;

    double maxInterest = max_element(schedule.begin(), schedule.end(), 
        [](const PaymentDetail& a, const PaymentDetail& b) {
            return a.interest < b.interest;
        })->interest;

    cout << "CORRECT CHART \n";//Resulting final output  of principal through interest
    cout << "Month\t Principal \t Interest \t Chart\n";

    for (const auto& detail : schedule) {
        if (detail.month % 12 == 1 || detail.month == (int)schedule.size() || detail.month <= 3) {
            int principalWidth = (detail.principal / maxPrincipal) * chartWidth;
            int interestWidth = (detail.interest / maxInterest) * chartWidth;

            cout << detail.month << "\t" << fixed << setprecision(2) << detail.principal 
                 << "\t\t" << detail.interest << "\t\t";

           cout << "[";
            for (int i = 0; i < principalWidth; i++) cout << "P";
            
           cout << "|";
            for (int i = 0; i < interestWidth; i++) cout << "I";
            cout << "]\n";
        }
    }
}

float  getValidatedInput(const string& prompt, float min, float max) {
    double value;
    while (true) {
        cout << prompt;
        cin >> value;

        if (cin.fail() || value < min || value > max) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input. Please enter a value between " << min << " and " << max << ".\n";
        } else {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return value;
        }
    }
}

int getValidatedIntegerInput(const string& prompt, int min, int max) {
    int value;
    while (true) {
        cout << prompt;
        cin >> value;

        if (cin.fail() || value < min || value > max) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input. Please enter an integer between " << min << " and " << max << ".\n";
        } else {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return value;
        }
    }
}

char getYesNoInput(const string& prompt) {
    char choice;
    while (true) {
        cout << prompt;
        cin >> choice;
        choice = tolower(choice);

        if (choice == 'y' || choice == 'n') {
            return choice;
        } else {
            cin.clear();
            cout << "Please enter 'y' for yes or 'n' for no.\n";
        }
    }
}
