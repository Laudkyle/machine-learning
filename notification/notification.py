from plyer import notification

title = "My First Notification"
message = "This is the first notification I am displaying"
app_name = "Joe"
timeout = 10
toast = "Here is a simpler message"
ticker = "Notification"

notification.notify(title=title, message=message, app_name=app_name, timeout=timeout)