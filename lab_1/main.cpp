#include <iostream>
#include <string.h>
#include <stdio.h>
#include <fstream>

using namespace std;

#define TRUE 1
#define FALSE 0
#define SIZE 100

int check_number()
{
    int res = TRUE;

    FILE *number_pipe, *number_key;
    // system_profiler - планировщик системы
    // SPHardwareDataType - информация о железе
    // UUID - стандарт идентификации, используемый в создании программного обеспечения
    // awk - нструмент для обработки и фильтрации текста
    number_pipe = popen("system_profiler SPHardwareDataType | awk '/UUID/ { print $3; }'", "r");
    number_key = fopen("license.key", "r");

    if (number_pipe == NULL || number_key == NULL) {
        return FALSE;
    }

    char buf[SIZE], file[SIZE];
    
    memset(&buf[0], 0, sizeof(buf));
    memset(&file[0], 0, sizeof(file));

    fgets(buf, sizeof(buf), number_pipe);
    fgets(file, sizeof(file), number_key);

    for (int i = 0; i < SIZE; i++) {
        if (file[i] != buf[i]) {
            res = FALSE;
        }
    }

    return res;

}

void bubbleSort(int *num, int size)
{
    for (int i = 0; i < size - 1; i++)
    {
        for (int j = (size - 1); j > i; j--)
        {
            if (num[j - 1] > num[j])
            {
                int temp = num[j - 1];
                num[j - 1] = num[j];
                num[j] = temp;
            }
        }
    }
}


int main()
{
    int res;
    res = check_number();

    if (res == TRUE) {
        int a[10];
        for (int i = 0; i < 10; i++)
        {
            printf("a[%d] = ", i);
            scanf("%d", &a[i]);
        }

        bubbleSort(a, 10);

        for (int i = 0; i<10; i++)
            printf("%d ", a[i]);
        getchar(); getchar();
    }
    else
    {
        cout << "Please, activate the program!" << endl;
    }

    return 0;
}
