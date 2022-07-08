import win10toast
import psutil


battery = psutil.sensors_battery()
battery = battery.percent

win10toast.ToastNotifier().show_toast(
    f"{battery}% of your battery remaining", duration=10
)

