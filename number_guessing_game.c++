#include <iostream>
#include <cstdlib>  
#include <ctime>    
#include <limits>  

using namespace std;

void displayWelcome() {
    cout << " WELCOME TO THE NUMBER THAT YOU WANT TO CHOOSE\n";
    cout << "I'm thinking of a number choosing from  1 and 70.\n";
    cout << "Can you guess what it is?\n\n";
}

int getUserGuess() {
    int guess;
    
    while (true) {
        cout << "Enter your guess: ";
        cin >> guess;
        
        if (cin.fail()) {
            cin.clear(); 
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
            cout << "Please enter a valid number between 1 and 70.\n";
            cout<<endl;
        } else if (guess < 1 || guess > 70) {
            cout << "Your guess must be between 1 and 70. Try again.\n";
            cout<<endl;
        } else {
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
            return guess;
        }
    }
}

void playGame() {
    srand(time(0)); 
    int secretNumber = rand() % 100 + 1;
    
    int guessCount = 0;
    int userGuess;
    bool hasGuessedCorrectly = false;
    
    cout << "I've picked a number. Let's begin!\n\n";
    cout<<endl;

    while (!hasGuessedCorrectly) {
        userGuess = getUserGuess();
        guessCount++;
        
        if (userGuess < secretNumber) {
            cout << "Too low! Try a higher number.\n";
            cout<<endl;
        } else if (userGuess > secretNumber) {
            cout << "Too high! Try a lower number.\n";
            cout<<endl;
        } else {
            hasGuessedCorrectly = true;
            cout << "CONGRATULATIONS ! YOU HAVE WON IT\n";
            cout<<endl;
            cout <<"You guessed the correct number in " << guessCount << " tries!\n";
            cout<<endl;
        }
    }
}

bool askToPlayAgain() {
    char choice;
    cout << "Would you like to play again? (yes/no): ";
    cin >> choice;
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
    
    return (choice == 'y' || choice == 'Y');
}

int main() {
    bool playAgain = true;
    
    displayWelcome();
    
    while (playAgain) {
        playGame();
        playAgain = askToPlayAgain();
        cout << endl;
    }
    
    cout << "\nThank You for playing !Have a good day! Goodbye!\n";
    return 0;
}
