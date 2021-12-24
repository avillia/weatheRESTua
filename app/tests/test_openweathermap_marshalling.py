from datetime import date

from assertpy import assert_that
from pytest_mock import MockerFixture

from app.src.services.weather_fetcher import obtain_weather_for_city


def test_correct_response_from_obtain_weather(mocker: MockerFixture):
    geodirect_data = [{"lat": 40, "lon": 40}]

    onecall_data = {
        "daily": [
            {
                "dt": 1639659212,
                "temp": {"day": 280, "night": 270, "max": 296, "min": 269},
                "pressure": 1000,
                "humidity": 69,
                "wind_speed": 4.0,
                "clouds": 69,
                "rain": 4.0,
            }
        ]
    }

    mocked_geodirect = mocker.MagicMock()
    mocked_geodirect.attach_mock(mocker.MagicMock(return_value=geodirect_data), "json")
    mocked_onecall = mocker.MagicMock()
    mocked_onecall.attach_mock(mocker.MagicMock(return_value=onecall_data), "json")
    mocked_get = mocker.MagicMock()
    mocked_get.side_effect = [mocked_geodirect, mocked_onecall]

    mocker.patch("requests.get", mocked_get)

    desired_response = {
        "date": date(2021, 12, 16),
        "temp": 275,
        "pcp": 4.0,
        "clouds": 69,
        "pressure": 1000,
        "humidity": 69,
        "wind_speed": 4.0,
    }

    result = obtain_weather_for_city("SomeCity")

    assert_that(result).is_type_of(list).is_not_empty()
    assert_that(result[0].dict()).is_equal_to(desired_response)
