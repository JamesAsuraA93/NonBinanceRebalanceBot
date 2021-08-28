from flask import Flask
from threading import Thread
import rebalance



app = Flask('')

@app.route('/')

def main():
  rebalance.running()
  return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()