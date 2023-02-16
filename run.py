from AnandaInvestor import create_app
from AnandaInvestor.config import ConfigDefault

# The Config is always ConfigDefault

app = create_app()  # Prod
# app = create_app(ConfigUAT)  # UAT
# app = create_app(ConfigTest)  # Test

if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/