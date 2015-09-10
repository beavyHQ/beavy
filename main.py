from beavy.app import app

@app.route("/")
def hello():
    return """<html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Hello World</h1>
        <script type="text/javascript" src="/assets/main.js"></script>
    </body>
"""
