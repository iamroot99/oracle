from flask import Flask, session, redirect, url_for, request
import random
import os

app = Flask(__name__)
app.secret_key = "REDACTED_FOR_PRIVACY"

flag = "ICTF\{REDACTED_FOR_PRIVACY\}"

@app.route('/', methods = ['GET', 'POST'])
def index():
	if 'password' not in session:
		data = "You are not logged in. <br><a href = '/login'>" + "Click here to log in.</a>"
		return generate_page(data)

	if request.method == 'GET':
		data = '''
			<h1> <b>Welcome, adventurer!</b></h1>
			<p> "<b>The Oracle</b> has been expecting you," the voice says. You look to your friends and then up and see a giant crystall ball. <br/>
				"<b>The Oracle</b> is thinking of a number. Guess right and you live to hack another day. Guess wrong and you all
				shall suffer." </p>
			<p> You look again to your friends and realise that they are lost. <b>The Oracle</b> only speaks in your mind. </p>
			<form action = "" method = "post">
				<p> <input type = text name = guess /> </p>
				<p> <input type = submit value = Guess /> <p>
			</form>
		'''
		return generate_page(data)

	if request.method == 'POST':
		attempts_left = len(session['stuff'])
		if attempts_left == 0:
			session.pop('password')
			return redirect(url_for('index'))

		guess = request.form['guess']
		
		options = session['stuff']
		actual = options.pop()
		session['stuff'] = options

		if guess.isnumeric() and int(guess) == actual:
			data = f"""
				<h4> The earth shatters around you as <b>The Oracle</b> hisses and explodes into a bright light. You close your eyes until you feel the blinding light fade away. <b> The Oracle </b> has dissapeared and left a flag behind. </h4>
				<h4>
				{flag} </br> 
				<b>The Oracle</b> has been defeated! GG! </h4>"""
			return generate_page(data)
		else:
			data = f'''
				<h1> Welcome! The Oracle has been expecting you. </h1>
				<h3> The Oracle is thinking of a number. Can you guess it? </p>
				<form action = "" method = "post">
					<p> <input type = text name = guess /> </p>
					<p> <input type = submit value = Guess /> <p>
				</form>
				<p> Incorrect. <b>The Oracle</b> will remember this. You have {attempts_left - 1} tries.</p>
			'''
			return generate_page(data)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['password'] = request.form['password']
		# removed unsafe custom seed
		session['stuff'] = random.sample(range(10000, 1000000000), 10)

		return redirect(url_for('index'))

	data =  '''
		<form action = "" method = "post">
			<p> Password: </p>
			<p> <input type = password name = password /> </p>
			<p> <input type = submit value = Login /></p>
		</form>
		'''
	return generate_page(data)

def generate_page(data):
	return f"""
		<video autoplay muted loop id="oracle">
  			<!-- <source src="https://github.com/iamroot99/oracle/blob/main/static/oracle.mp4" type="video/mp4"> -->
  			<source src="./static/oracle.mp4" type="video/mp4">
		</video>

		<style>
			#oracle {{
  				position: fixed;
  				right: 0;
  				bottom: 0;
  				min-width: 100%;
  				min-height: 100%;
  				transform: translateX(calc((100% - 100vw) / 2));
			}}

			.content {{
  				position: fixed;
  				bottom: 0;
			 	background: rgba(0, 0, 0, 0.5);
				color: #f1f1f1;
  				width: 100%;
			  	padding: 20px;
			}}
		</style>

		<div class="content">
			{data}
		</div>
		"""

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
