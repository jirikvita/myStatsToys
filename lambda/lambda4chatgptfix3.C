#include <iostream>
#include <cmath>
#include <functional>

void lambda4chatgptfix3() {
    // Define a lambda function that generates consecutive powers of a base value
    auto power_generator = [](int n) {
        return [n](int x, int count) {
            for (int i = 0; i < count; ++i) {
                std::cout << x << " to the power of " << i + 1 << " is: " << pow(x, i + 1) << std::endl;
            }
        };
    };

    // Example usage
    auto doubler = power_generator(2);
    auto tripler = power_generator(3);
    auto quadrupler = power_generator(4);

    // Use the generated functions
    int value = 2;  // Starting value
    int count = 5;  // Number of consecutive powers to print

    doubler(value, count);
    tripler(value, count);
    quadrupler(value, count);

    return 0;
}
