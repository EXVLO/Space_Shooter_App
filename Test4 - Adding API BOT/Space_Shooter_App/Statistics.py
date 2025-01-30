import numpy as np
import matplotlib.pyplot as plt


def show_graph(curr_client, server):
    message = f"%%%GETSTATS"
    server.serv.send(message.encode("utf-8"))

