from model.calendar import get_calendar_days, get_month_str
from model.events import GoogleCalendarEvents
from model.weather import OpenWeatherMapModel
from utils.config_generator import Configurations, load_or_create_config
from view.window import Window7in5

window = Window7in5('resources')


class Controller:
    def __init__(self, config: Configurations):
        self.window = Window7in5('resources')
        self.events = GoogleCalendarEvents(config.google_credential)
        for calendar_id in config.selected_calendars:
            self.events.select_calendar(calendar_id)
        self.weather = OpenWeatherMapModel(config.owm_token, config.city_id)
        self.weather.temperature_unit = config.units

    def update_calendar(self):
        self.window.calender.clear_selection()
        self.window.calender.set_month(get_month_str())
        days, selection = get_calendar_days()
        self.window.calender.set_dates(days)
        self.window.calender.set_select_date(selection[0], selection[1], True)

    def update_weather(self):
        weather_id, low, high, humidity = self.weather.get_current_weather()
        self.window.weather.set_weather(weather_id)
        self.window.weather.set_temp_range(low, high)
        self.window.weather.set_humidity(humidity)
        forecasts = self.weather.get_daily_forecast()
        forecasts = list(map(lambda forecast: forecast[:-1], forecasts))
        self.window.weather.set_forecast(forecasts)

    def update_events(self):
        events = self.events.get_sorted_events()
        self.window.events.set_events(events)

    def render(self):
        return self.window.render()


config = load_or_create_config()

controller = Controller(config)
controller.update_calendar()
controller.update_weather()
controller.update_events()

image = controller.render()

image.save("text.png")