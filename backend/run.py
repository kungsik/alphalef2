from bibleapi import app

if __name__ == '__main__':
	from bibleapi.app import create_app
	app = create_app()
	app.run(debug=False)
