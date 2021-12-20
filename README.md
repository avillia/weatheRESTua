# weatheRESTua
Small RESTful API build on Flask to obtain basic weather info for UA cities.

## How to run?
1. Create separate venv for project and install dependencies: `pip install -r requirements.txt`
2. Create `.env` file (use `sample.env` for reference)
3. [Obtain your OpenWeatherMapAPI token](https://openweathermap.org/price)
4. Paste it in required .env field
5. `flask run` from the project directory if you want to do some tests manually...
6. ... or use `python request_samples.py` to test it automatically!
