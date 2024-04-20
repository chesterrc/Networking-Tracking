import datetime as dt
import os
import time

import dearpygui.dearpygui as dpg

import network_monitoring_examples as nm

dpg.create_context()

start_time = time.time()

#Status of Servers
dns_queries = [
    ('quad9.net', 'A'),
    ('quad9.net', 'AAAA')
]

servers = ["https://stackoverflow.com", "http://allura.apache.org", "youtube.com",
        "129.6.15.28", ["9.9.9.9", "quad9.net",dns_queries], ["google.com", 80], ["206.200.127.128", 26477]]


def serviceCheck(timing):
    #https
    timing = str(timing)
    if timing[-1] == "0":
        dpg.set_value("https_time_last", dt.datetime.now())
        https_check = nm.check_server_https(servers[0])
        dpg.set_value("https_status_tag", "UP" if https_check[0] is True else "Down")
        if https_check[0] is True:
            dpg.set_value("https_service_tag", "Status code:" + str(https_check[1])+ "|" + https_check[2])
        else:
            dpg.set_value("https_service_tag", "Server is down")
    #http
    if timing[-1] == "2":
        dpg.set_value("http_time_last", dt.datetime.now())
        http_check = nm.check_server_http(servers[1])
        dpg.set_value("http_status_tag", "UP" if http_check[0] is True else "Down")
        if http_check[0] is True:
            dpg.set_value("http_service_tag", "Status code:" + str(http_check[1]))
        else:
            dpg.set_value("http_service_tag", "Server is down")
    #ICMP (ping)
    if timing[-1] == "3":
        dpg.set_value("ICMP_time_last", dt.datetime.now())
        pinging = nm.ping(servers[2])
        dpg.set_value("ICMP_status_tag", "UP" if pinging[1] != None else "Down")
        if pinging[1] != None:
            dpg.set_value("ICMP_service_tag", f"Server:{pinging[0]} Time:{round(pinging[1], 3)} ms")
        else:
            dpg.set_value("ICMP_service_tag", "Server is down")
    #NTP
    if timing[-1] == "4":
        dpg.set_value("NTP_time_last", dt.datetime.now())
        ntp_check = nm.check_ntp_server(servers[3])
        dpg.set_value("NTP_status_tag", "UP" if ntp_check[1] != False else "Down")
        if ntp_check[1] != None:
            dpg.set_value("NTP_service_tag", f"date: {ntp_check[1]}")
        else:
            dpg.set_value("NTP_service_tag", f"Server is down")
    #DNS A
    if timing[-1] == "5":
        dpg.set_value("DNS_time_last", dt.datetime.now())
        dns_check = nm.check_dns_server_status(servers[4][0], servers[4][1], "A")

        dpg.set_value("DNS_status_tag_A", "UP" if dns_check[0] is True else "Down")
        if dns_check[0] is True:
            dpg.set_value("DNS_service_tag_A", f"Query Results:{dns_check[1]}")
        else:
            dpg.set_value("DNS_service_tag_A", "Server is down")
    #TCP
    if timing[-1] == "6":
        dpg.set_value("TCP_time_last", dt.datetime.now())
        tcp_check = nm.check_tcp_port(servers[5][0], servers[5][1])

        dpg.set_value("TCP_status_tag", "UP" if tcp_check[0] is True else "Down")
        if tcp_check[0] is True:
            dpg.set_value("TCP_service_tag", f"{tcp_check[1]}")
        else:
            dpg.set_value("TCP_service_tag", "Server is down")
    #UDP
    if timing[-1] == "7":
        dpg.set_value("UDP_time_last", dt.datetime.now())
        udp_check = nm.check_udp_port(servers[6][0], servers[6][1])
        dpg.set_value("UDP_status_tag", "UP" if udp_check[0] is True else "Down")
        if udp_check[0] is True:
            dpg.set_value("UDP_service_tag", udp_check[1])
        else:
            dpg.set_value("UDP_service_tag", "Server is down")
    #DNS AAAA
    if timing[-1] == "5":
        dpg.set_value("DNS_time_last_AAAA", dt.datetime.now())
        dns_check = nm.check_dns_server_status(servers[4][0], servers[4][1], "AAAA")

        dpg.set_value("DNS_status_tag_AAAA", "UP" if dns_check[0] is True else "Down")
        if dns_check[0] is True:
            dpg.set_value("DNS_service_tag_AAAA", f"Query Results:{dns_check[1]}")
        else:
            dpg.set_value("DNS_service_tag_AAAA", "Server is down")
    #TCP echo
    if timing[-1] == "1":
        dpg.set_value("ECHO_time_last", dt.datetime.now())
        echo_check = nm.tcp_echo_client_check("message")
        dpg.set_value("ECHO_status_tag", "UP" if echo_check[0] == "UP" else "Down")
        if echo_check[0] == "UP":
            dpg.set_value("ECHO_service_tag", "Address: " + echo_check[1] + " Port: " + echo_check[2] )
        else:
            dpg.set_value("ECHO_service_tag", "Server is down")


with dpg.window(tag="Primary Window",label="Network Monitoring Service"):
    with dpg.table(header_row=True):
        
        # use add_table_column to add columns to the table,
        # table columns use child slot 0
        dpg.add_table_column(label="Hostname/IP address")
        dpg.add_table_column(label="Time since last change")
        dpg.add_table_column(label="Status")
        dpg.add_table_column(label="Protocol")
        dpg.add_table_column(label="Description")

        # add_table_next_column will jump to the next row
        # once it reaches the end of the columns
        # table next column use slot 1
        for i in range(len(servers)+2):
            with dpg.table_row():
                for j in range(5):
                    #https
                    if i == 0:
                        if j == 0:
                            dpg.add_text(servers[i])
                        if j == 1:
                            dpg.add_text(tag="https_time_last")
                        if j == 2:
                            dpg.add_text(tag="https_status_tag")
                        if j == 3:
                            dpg.add_text("HTTPS")
                        if j == 4:
                            dpg.add_text(tag="https_service_tag")
                    #http
                    if i == 1:
                        if j == 0:
                            dpg.add_text(servers[i])
                        if j == 1:
                            dpg.add_text(tag="http_time_last")
                        if j == 2:
                            dpg.add_text(tag="http_status_tag")
                        if j == 3:
                            dpg.add_text("HTTP")
                        if j == 4:
                            dpg.add_text(tag="http_service_tag")
                    #ICMP
                    if i == 2:
                        if j == 0:
                            dpg.add_text(servers[i])
                        if j == 1:
                            dpg.add_text(tag="ICMP_time_last")
                        if j == 2:
                            dpg.add_text(tag="ICMP_status_tag")
                        if j == 3:
                            dpg.add_text("ICMP")
                        if j == 4:
                            dpg.add_text(tag="ICMP_service_tag")
                    #NTP
                    if i == 3:
                        if j == 0:
                            dpg.add_text(servers[i])
                        if j == 1:
                            dpg.add_text(tag="NTP_time_last")
                        if j == 2:
                            dpg.add_text(tag="NTP_status_tag")
                        if j == 3:
                            dpg.add_text("NTP")
                        if j == 4:
                            dpg.add_text(tag="NTP_service_tag")
                    #DNS
                    if i == 4:
                        if j == 0:
                            dpg.add_text(servers[i][0])
                        if j == 1:
                            dpg.add_text(tag="DNS_time_last")
                        if j == 2:
                            dpg.add_text(tag="DNS_status_tag_A")
                        if j == 3:
                            dpg.add_text("DNS")
                        if j == 4:
                            dpg.add_text(tag="DNS_service_tag_A")
                    #TCP
                    if i == 5:
                        if j == 0:
                            dpg.add_text(servers[i][0])
                        if j == 1:
                            dpg.add_text(tag="TCP_time_last")
                        if j == 2:
                            dpg.add_text(tag="TCP_status_tag")
                        if j == 3:
                            dpg.add_text("TCP")
                        if j == 4:
                            dpg.add_text(tag="TCP_service_tag")
                    #UDP
                    if i == 6:
                        if j == 0:
                            dpg.add_text(servers[i][0])
                        if j == 1:
                            dpg.add_text(tag="UDP_time_last")
                        if j == 2:
                            dpg.add_text(tag="UDP_status_tag")
                        if j == 3:
                            dpg.add_text("UDP")
                        if j == 4:
                            dpg.add_text(tag="UDP_service_tag")
                    #DNS
                    if i == 7:
                        if j == 0:
                            dpg.add_text(servers[4][0])
                        if j == 1:
                            dpg.add_text(tag="DNS_time_last_AAAA")
                        if j == 2:
                            dpg.add_text(tag="DNS_status_tag_AAAA")
                        if j == 3:
                            dpg.add_text("DNS")
                        if j == 4:
                            dpg.add_text(tag="DNS_service_tag_AAAA")
                    #TCP echo server
                    if i == 8:
                        if j == 0:
                            dpg.add_text("TCP echo Server")
                        if j == 1:
                            dpg.add_text(tag="ECHO_time_last")
                        if j == 2:
                            dpg.add_text(tag="ECHO_status_tag")
                        if j == 3:
                            dpg.add_text("TCP")
                        if j == 4:
                            dpg.add_text(tag="ECHO_service_tag")


dpg.create_viewport(title='Custom Title', width=1020, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

"""
Render loop to continuously check status of servers and services
"""
ti = dpg.get_total_time()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    tf = dpg.get_total_time()
    if (tf - ti) > 1: #approx 1 second intevals
        ti = tf
        ti_string = str(int(ti))
        serviceCheck(ti_string)

    dpg.render_dearpygui_frame()

dpg.destroy_context()