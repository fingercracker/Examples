#include <iostream>

class Something {
    private:
        int _something;
        std::string _nothing;

    public:
        int someOtherThing;
        Something(int something, std::string nothing);

        void setSomething(int something);
        void setNothing(std::string nothing);
        int getSomething();
        std::string getNothing();
};