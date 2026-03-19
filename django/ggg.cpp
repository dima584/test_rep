#include <iostream>
#include <string>
#include <Windows.h>

using namespace std;

class Buyer {
private:
    string surname, name, patronymic, address, phone, creditCard, bankAccount;

public:

    Buyer() {}

    void Login() {
        cout << "Введення даних покупця" << endl;
        cout << "Прізвище: "; cin >> surname;
        cout << "Ім'я: "; cin >> name;
        cout << "По батькові: "; cin >> patronymic;
        cout << "Адреса: "; cin.ignore(); getline(cin, address);
        cout << "Телефон: "; cin >> phone;
        cout << "Номер кредитної карти: "; cin >> creditCard;
        cout << "Банківська карта: "; cin >> bankAccount;
    }

    void setSurname(string s) { surname = s; }
    void setName(string n) { name = n; }
    void setAddress(string addr) { address = addr; }
    void setPhone(string ph) { phone = ph; }


    void Present() {
        cout << "\nПоточна картка покупця" << endl;
        cout << "ПІБ: " << surname << " " << name << " " << patronymic << endl;
        cout << "Адреса: " << address << "  Тел: " << phone << endl;
        cout << "кредитна карта: " << creditCard << " | Банківська карта: " << bankAccount << endl;
    }
};

int main() {
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);

    Buyer player_1;

    player_1.Login();
    player_1.Present();

    cout << "\nЗмінюємо прізвище та телефон." << endl;

    string newSurname, newPhone;
    cout << "Введіть НОВЕ прізвище: "; cin >> newSurname;
    player_1.setSurname(newSurname);

    cout << "Введіть НОВИЙ телефон: "; cin >> newPhone;
    player_1.setPhone(newPhone);   

    player_1.Present();

    return 0;
}