import webapp2
import string
import re
import cgi

form_1 = """
	<form method="post">
		<h1>Signup</h1>
		<br>
		<label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Username
			<input type="text" name="username" value="%(username)s">
		</label><span style="color: red">%(error_username)s</span>
		<br>
"""
form_2 = """
		<label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Password
			<input type="password" name="password" value="%(password)s">
		</label><span style="color: red">%(error_password)s</span>
		<br>
"""
form_3 = """
		<label>Verify Password
			<input type="password" name="verify" value="%(verify)s">
		</label><span style="color: red">%(error_verify)s</span>
		<br>
"""
form_4 = """
		<label>Email (optional)
			<input type="text" name="email" value="%(email)s">
		</label><span style="color: red">%(error_email)s</span>
		<br>
		<input type="submit">
	</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form_1(self, username="", error_username=""):
		self.response.out.write(form_1 % {"username": username,
										"error_username": error_username})

	def write_form_2(self, password="", error_password=""):
		self.response.out.write(form_2 % {"password": password, "error_password": error_password})

	def write_form_3(self, verify="", error_verify=""):
		self.response.out.write(form_3 % {"verify": verify, "error_verify": error_verify})

	def write_form_4(self, email="", error_email=""):
		self.response.out.write(form_4 % {"email": email, "error_email": error_email})

	def write_form(self, username="", error_username="", password="", error_password="", verify="", error_verify="", email="", error_email=""):
		self.write_form_1(username, error_username)
		self.write_form_2(password, error_password)
		self.write_form_3(verify, error_verify)
		self.write_form_4(email, error_email)

	def get(self):
		self.write_form()

	def post(self):
		this_username = self.request.get("username")
		this_password = self.request.get("password")
		this_verify = self.request.get("verify")
		this_email = self.request.get("email")

		validated_username = valid_username(this_username)
		validated_password = valid_password(this_password)
		validated_email = valid_email(this_email)

		if (validated_username):
			self.write_form_1(username=this_username)
		elif (validated_username == None):
			self.write_form_1(username=this_username, error_username="That's not a valid username.")

		if (validated_password):
			self.write_form_2()
		elif (validated_password == None):
			self.write_form_2(error_password="That wasn't a valid password.")
		
		if (this_password == this_verify):
			self.write_form_3()
		else:
			self.write_form_3(error_verify="Your passwords didn't match.")

		if (validated_email):
			self.write_form_4(email=this_email)
		else:
			self.write_form_4(email=this_email, error_email="That's not a valid email.")

		if (validated_username and validated_password and (this_password == this_verify) and validated_email):
			self.redirect('/success')


class SuccessHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Success! Your account has been created.")


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

def escape_html(s):
	return cgi.escape(s, quote=True)

app = webapp2.WSGIApplication([('/', MainPage), ('/success', SuccessHandler)], debug=True)