#include "example.hpp"

Something::Something(int something, std::string nothing) {
    setSomething(something);
    setNothing(nothing);
}

void Something::setSomething(int something) {
    _something = something;
}

void Something::setNothing(std::string nothing) {
    _nothing = nothing;
}

int Something::getSomething() {
    return _something;
}

std::string Something::getNothing() {
    return _nothing;
}

int main() {
    Something s{1, "nothing"};
    std::cout << "s.nothing is " << s.getNothing() << "." << std::endl;
    std::cout << "s.something is " << s.getSomething() << "." << std::endl;
}