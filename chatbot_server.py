from flask import Flask, redirect, url_for, request, render_template
from web import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)