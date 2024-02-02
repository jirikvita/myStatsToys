#include <iostream>
#include <functional>

void lambda2() {
    // Define a lambda function that generates a power function
    auto power_generator = [](int n) {
        return [n](int x) { return x * n; };
    };

    // Example usage
    auto doubler = power_generator(2);
    auto tripler = power_generator(3);
    auto quadrupler = power_generator(4);

    // Use the generated functions
    int value = 5;

    int doubled_value = doubler(value);
    int tripled_value = tripler(value);
    int quadrupled_value = quadrupler(value);

    std::cout << "Original value: " << value << std::endl;
    std::cout << "Doubled value: " << doubled_value << std::endl;
    std::cout << "Tripled value: " << tripled_value << std::endl;
    std::cout << "Quadrupled value: " << quadrupled_value << std::endl;

    return 0;
}
