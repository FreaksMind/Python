import tkinter as tk
from tkinter import ttk
import os

class PacketListApp:
    def __init__(self, root):
        self.root = root
        self.sniffer = None
        self.sniffer_running = True
        self.packets = []

        self.root.title("HTTP SNIFFER")

        self.root.option_add('*tearOff', False)
        self.menu_bar = tk.Menu(self.root)
        self.menu_file = tk.Menu(self.menu_bar)
        self.menu_edit = tk.Menu(self.menu_bar)
        self.sniffer_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.menu_file, label='File')
        self.menu_bar.add_cascade(menu=self.menu_edit, label='Edit')
        self.menu_bar.add_cascade(menu=self.sniffer_menu, label='Sniffer')
        self.sniffer_menu.add_command(label='Resume Sniffer', command=self.resume_sniffer)
        self.sniffer_menu.add_command(label='Pause Sniffer', command=self.pause_sniffer)
        

        self.root['menu'] = self.menu_bar


        self.grid = tk.PanedWindow(root, height=300, width=600, orient='vertical')
        self.grid.grid()
        self.grid.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(self.grid, columns=("Number", "Source", "Destination", "Protocol"))
        self.tree.heading("#0", text="Packet", )
        self.tree.heading("Number", text="Number")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Protocol", text="Protocol")
        self.tree.bind("<ButtonRelease-1>", self.show_packet_details)

        self.tree.tag_configure('GET', background='lightblue')
        self.tree.tag_configure('POST', background='green')

        self.tree.pack(expand=True, fill=tk.BOTH)


        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Delete", command=lambda: print("da"))

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.packet_counter = 0

        self.detail_text = tk.Text(self.grid, wrap="word", height=10, width=50)
        self.detail_text.pack(expand=True, fill=tk.BOTH)

        scrollbar_ = ttk.Scrollbar(self.detail_text, orient="vertical", command=self.detail_text.yview)
        self.detail_text.configure(yscroll=scrollbar_.set)
        scrollbar_.pack(side="right", fill="y")

        self.grid.add(self.tree)
        self.grid.add(self.detail_text)

        self.status_bar_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        self.status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.left_status_label = tk.Label(self.status_bar_frame, text=f"Packets received: {self.packet_counter}", anchor=tk.W, padx=5)
        self.left_status_label.pack(side=tk.LEFT)

        self.right_status_label = tk.Label(self.status_bar_frame, text="Sniffer: Running", anchor=tk.E, padx=5)
        self.right_status_label.pack(side=tk.RIGHT)

        self.status_bar_frame1 = tk.Frame(self.grid, bd=1, relief=tk.SUNKEN)
        self.status_bar_frame1.pack(side=tk.BOTTOM, fill=tk.X)


        self.request_method_label = tk.Label(self.status_bar_frame1, text="Request Method:")
        self.request_method_label.pack(side=tk.LEFT)

        self.request_method_entry = tk.Entry(self.status_bar_frame1)
        self.request_method_entry.pack(side=tk.LEFT)

        self.ip_filter_label = tk.Label(self.status_bar_frame1, text="IP Filter:")
        self.ip_filter_label.pack(side=tk.LEFT)

        self.ip_filter_entry = tk.Entry(self.status_bar_frame1)
        self.ip_filter_entry.pack(side=tk.LEFT)

        self.apply_filters_button = tk.Button(self.status_bar_frame1, text="Apply Filters", command=d)
        self.apply_filters_button.pack(side=tk.LEFT)

        self.left_status_label1 = tk.Label(self.status_bar_frame1, text=f"Packets filtered: 4", anchor=tk.W, padx=5)
        self.left_status_label1.pack(side=tk.LEFT)

    def show_packet_details(self):
        pass

    def add_packet(self, packet):
        self.packets.append(packet)
        self.packet_counter += 1

    def set_sniffer(self):
        pass
    def pause_sniffer(self):
        pass

    def resume_sniffer(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = PacketListApp(root)
    root.mainloop()