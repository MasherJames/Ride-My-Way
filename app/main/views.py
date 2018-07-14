from . import main


@main.route('/')
def index():
    return "Ride my way carpooling application"
