# weatheRESTua
Small REST API build on FastAPI (wanted to try something new) to obtain basic weather info for UA cities.

## How to run?
1. Create separate venv for project and install dependencies: `pip install -r requirements.txt`
2. Create `.env` file (use `sample.env` for reference)
3. [Obtain your OpenWeatherMapAPI token](https://openweathermap.org/price)
4. Paste it in required .env field
5. `uvicorn run:app` from the project directory - and that's it!
