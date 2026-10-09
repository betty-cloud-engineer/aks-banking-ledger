from flask import Flask, jsonify
import time

app = Flask(__name__)

# In-memory ledger data
ledger_balances = {
    "ACC-7732": 150000.00,
    "ACC-9011": 42500.50
}

@app.route("/api/ledger", methods=["GET"])
def get_ledger():
    return jsonify({
        "status": "SECURE",
        "timestamp": int(time.time()),
        "system": "AKS-Banking-Ledger-Core",
        "data": ledger_balances
    })

if __name__ == "__main__":
    # Python starts up on port 8080
    app.run(host="0.0.0.0", port=8080)
