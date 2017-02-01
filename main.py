import webapp2
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/'
        (the root of our site)
    """

    def get(self):

        password_header = "<h1>Signup</h1>"

        # form that takes user username
        username_form = """
        <form action="/username" method="post">

            <label>
                Username&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <input type="text" name = "username"/>
            </label>
            <br>
            <label>
                Password&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <input type="password" name = "password" value= ""/>
            </label>
            <br>
            <label>
                Verify Password
                <input type="password" name = "password_check" value= ""/>
            </label>
            <br>
            <label>
                Email(optional)&nbsp;
                <input type="text" name = "email"/>
            </label>
            <br>
            <input type="submit" value="Submit"/>
        </form>
        """

        # if we have an error, make a <p> to disply error
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        # combine all the pieces to build the content of our response
        content = password_header + username_form + error_element + page_header + page_footer
        self.response.write(content)


class ValidateUser(webapp2.RequestHandler):
    """ Handles requests coming in to '/username'
    """

    def post(self):
        # look inside the username request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        password_check = self.request.get("password_check")
        email = self.request.get("email")

        #if user types nothing, remind them to enter valid input
        if username == "" or len(username) < 3:
            error = "Please enter a valid username"
            error_escaped = cgi.escape(error, quote=True)
            self.response.write(error_escaped)
            #redirect to homepage, and include error
            self.redirect("/?error=" + error_escaped)

        # if user types nothing, remind them to enter a password
        elif password == "":
            error = "Please enter a valid password"
            password_error_escaped = cgi.escape(error, quote=True)
            self.response.write(password_error_escaped)
            #redirect to homepage, ands include error
            self.redirect("/?error=" + password_error_escaped)

        elif password_check == "":
            error = "Please verify your password"
            password_error_escaped = cgi.escape(error, quote=True)
            self.response.write(password_error_escaped)
            #redirect to homepage, ands include error
            self.redirect("/?error=" + password_error_escaped)

        elif password != password_check:
            error = "Passwords do not match"
            password_error_escaped = cgi.escape(error, quote=True)
            self.response.write(password_error_escaped)
            #redirect to homepage, ands include error
            self.redirect("/?error=" + password_error_escaped)

        elif email == "":
            confirmation = "Welcome " + username
            self.response.write(confirmation)

        elif '@' not in email:
            error = "Please enter a valid email"
            password_error_escaped = cgi.escape(error, quote=True)
            self.response.write(password_error_escaped)

            #redirect to homepage, and include error
            self.redirect("/?error=" + password_error_escaped)

        else:
            confirmation = "Welcome " + username
            self.response.write(confirmation)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/username', ValidateUser)
], debug=True)
