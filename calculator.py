"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
def simplified(num_list, operator):
    sum = int(num_list[0])
    for i in range(1, len(num_list)):
        if operator == 'add':
            sum += int(num_list[i])
        if operator == 'subtract':
            sum -= int(num_list[i])
        if operator == 'multiply':
            sum *= int(num_list[i])
        if operator == 'divide':
            if num_list[i] == 0:
                raise ZeroDivisionError
            else:
                sum /= int(num_list[i])

    return str(int(sum))

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    return simplified(args, 'add')

# TODO: Add functions for handling more arithmetic operations.

def subtract(*args):
    """subtract subsequent arguments from the first, return a string of the sum"""
    return simplified(args, 'subtract')

def multiply(*args):
    """multiply the arguments together and return the total as a string"""
    return simplified(args, 'multiply')

def divide(*args):
    """divide the first argument by the following arguments, raise a ZeroDivisionError if dividing by zero"""
    return simplified(args, 'divide')

def main_page(*args):
    return """Welcome to the WSGI calculator,

            please choose from several functions to use,

            You can add, subtract, multiply, or divide!

            <p>Here are some examples:</p>

            <ul>"/add/2/3" Expect: 6</ul>

            <ul>"subtract/5/7" Expect: -2</ul>

            <ul>"multiply/2/2" Expect: 4</ul>

            <ul>"divide/24/6" Expect: 4</ul>

            <p>This calculator works only with integer numbers!!</p>

            """

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    args = path.strip("/").split('/')
    print(args)
    func_name = args.pop(0)
    func = {"add": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide,
            "": main_page}.get(func_name)

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Cannot Divide By Zero</h1>"
    #except Exception:
        #status = "500 Internal ServerError"
        #body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
