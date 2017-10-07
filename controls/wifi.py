import subprocess as sh
import time


def connect(**kwargs):
    if kwargs.has_key("discon") and kwargs.has_key("ssid"):
        sh.check_output(["nmcli", "connection", "down", "id", kwargs["ssid"]])
    elif kwargs.has_key("ssid"):
        if kwargs["ssid"] in available_connections():
            t0 = time.time()
            sh.check_output(["nmcli", "connection", "up", "id", kwargs["ssid"]])
            print kwargs["ssid"], "connected in", round((time.time() - t0), 3), "s"
        else:
            print kwargs["ssid"], "not available, falling back to wifi"
            t0 = time.time()
            sh.check_output(["nmcli", "connection", "up", "id", "B704"])
            print "B704 connected in", round((time.time() - t0), 3), "s"
    else:
        print "ssid is mandatory, discon is optional - always True"


def active_connection():
    conn = sh.check_output(["nmcli", "connection", "show", "--active"])
    return conn.split()[4] if len(conn.split()) > 4 else "NA"


def available_connections():
    conn_list = sh.check_output(["nmcli", "-f", "SSID", "device", "wifi", "list"])
    return conn_list


def switch_net():
    if active_connection() != "NA":
        conn = active_connection()
        connect(ssid=conn, discon=True)
        print conn, "disconnected"
        time.sleep(5)
        if conn == "B704":
            connect(ssid="IPhone")
        else:
            connect(ssid="B704")
    else:
        connect(ssid="B704")


switch_net()
# switch_net()