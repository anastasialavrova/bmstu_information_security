#include <iostream>
#include <string.h>
#include <stdio.h>

using namespace std;

#define TRUE 1
#define FALSE 0

int write_key()
{
    int check;
    int res;
    // system_profiler - планировщик системы
    // SPHardwareDataType - информация о железе
    // UUID - стандарт идентификации, используемый в создании программного обеспечения
    // awk - инструмент для обработки и фильтрации текста

    check = system("system_profiler SPHardwareDataType | awk '/UUID/ { print $3; }' > license.key");

    if (check == 0)
        res = TRUE;
    else
        res = FALSE;

    return res;
}

int main()
{
    int res;
    res = write_key();

    if (res == TRUE)
    {
        cout << "Activation is succeed!" << endl;
    }
    else
        cout << "Activation is failed!" << endl;

    return 0;
}
