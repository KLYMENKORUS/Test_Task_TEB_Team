<h1>Django Application</h1>
	<p>This is a Django application for registering users using a Telegram bot.</p>
  <h2>Installation</h2>
<ol>
	<li>Clone the repository:</li>
</ol>
<pre><code>git clone https://github.com/KLYMENKORUS/Test_Task_TEB_Team.git</code></pre>

<ol start="2">
	<li>Create a virtual environment and activate it:</li>
</ol>
<pre><code>python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate  # Windows</code></pre>

<ol start="3">
	<li>Install the requirements:</li>
</ol>
<pre><code>pip install -r requirements.txt</code></pre>

<ol start="4">
	<li>Create a <code>.env</code> file and set the following environment variables:</li>
</ol>
<pre><code>TELEGRAM_BOT_TOKEN=&lt;your-telegram-bot-token&gt;
SECRET_KEY=&lt;your-django-secret-key&gt;</code></pre>

<ol start="5">
	<li>Run the database migrations:</li>
</ol>
<pre><code>python manage.py migrate</code></pre>

<ol start="6">
	<li>Start the Django development server:</li>
</ol>
<pre><code>python manage.py runserver</code></pre>

<ol start="7">
	<li>Start your Telegram bot and chat with it to register new users.</li>
</ol>

