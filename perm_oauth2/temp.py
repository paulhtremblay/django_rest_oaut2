def my_decorator(some_function):

    def wrapper(*args, **kwargs):
        num = args[1]
        if num == 10:
            print("Yes!")
        else:
            print("No!")
            return

        some_function(*args, **kwargs)

        print("Something is happening after some_function() is called.")

    return wrapper


class Foo:

    @my_decorator
    def method(self, num, foo = 'f'):
        print("num is {num}".format(num= num))

if __name__ == "__main__":
    foo = Foo()
    foo.method(10, 'f')
    foo.method(11, 'f')

