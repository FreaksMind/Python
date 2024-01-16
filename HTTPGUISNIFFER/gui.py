import tkinter as tk
from tkinter import ttk
import os
from threading import Thread
import Sniffer
import utils


class PacketListApp:
    def __init__(self, root):
        self.root = root
        self.sniffer = None
        self.sniffer_running = True
        self.packets = []
        self.deleted_items = []

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

        self.tree = ttk.Treeview(self.grid, columns=("Number", "Source", "Destination", "Method", "Protocol"))
        self.tree.heading("#0", text="Packet", )
        self.tree.heading("Number", text="Number")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Method", text="Method")
        self.tree.heading("Protocol", text="Protocol")
        self.tree.bind("<ButtonRelease-1>", self.show_packet_details)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.tree.tag_configure('GET', background='khaki')
        self.tree.tag_configure('POST', background='brown2')
        self.tree.tag_configure('PUT', background='lightskyblue')
        self.tree.tag_configure('PATCH', background='gray')
        self.tree.tag_configure('DELETE', background='darkseagreen3')
        self.tree.tag_configure('HEAD', background='darkturquoise')
        self.tree.tag_configure('OPTIONS', background='dodgerblue3')
        self.tree.tag_configure('none', background='white')

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

        self.apply_filters_button = tk.Button(self.status_bar_frame1, text="Apply Filters", command=self.apply_filters)
        self.apply_filters_button.pack(side=tk.LEFT)


        self.left_status_label1 = tk.Label(self.status_bar_frame1, text=f"Packets filtered: 4", anchor=tk.W, padx=5)
        self.left_status_label1.pack(side=tk.LEFT)

        self.update_status_bar()

    def show_packet_details(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            
            packet_number = int(item[0])

            self.detail_text.delete(1.0, tk.END)
            details = f"Details for Packet {packet_number}:\n"

            ip_info = utils.parse_ip_header(self.packets[packet_number])
            payload = utils.parse_http_payload(self.packets[packet_number][ip_info['ihl']:])

            for h in payload[1]:
                details += h + '\n'

            details += payload[2]

            self.detail_text.insert(tk.END, details)

    def add_packet(self, packet):
        self.packets.append(packet)
        ipinfo = utils.parse_ip_header(packet)
        source = ipinfo['src_ip']
        destination = ipinfo['dest_ip']
        protocol = ipinfo['protocol']
        packet_payload = utils.parse_http_payload(packet[ipinfo['ihl']:])
        tag = None
        if('GET' in packet_payload[0]):
            tag = 'GET'
        elif('POST' in packet_payload[0]):
            tag = 'POST'
        elif('PUT' in packet_payload[0]):
            tag = 'PUT'
        elif('PATCH' in packet_payload[0]):
            tag = 'PATCH'
        elif('HEAD' in packet_payload[0]):
            tag = 'HEAD'
        elif('DELETE' in packet_payload[0]):
            tag = 'DELETE'
        elif('OPTIONS' in packet_payload[0]):
            tag = 'OPTIONS'    
        else:
            tag = 'none'
        self.tree.insert("", "end", values=(self.packet_counter, source, destination, tag, protocol), tags=(tag,))
        self.packet_counter += 1

    def set_sniffer(self, sniffer):
        self.sniffer = sniffer

    def pause_sniffer(self):
        self.sniffer.pause()
        self.sniffer_running = False

    def resume_sniffer(self):
        self.sniffer.resume()
        self.sniffer_running = True

    def update_status_bar(self):
        self.left_status_label.config(text=f"Packets received: {self.packet_counter}")
        self.right_status_label.config(text="Sniffer: " + "".join('Running' if self.sniffer_running is True else 'Paused'))

        self.root.after(1000, self.update_status_bar)

    def apply_filters(self):
        request_method = self.request_method_entry.get()
        ip_filter = self.ip_filter_entry.get()

        if request_method == '' and ip_filter == '':
            #for item in self.tree.get_children():
                #self.tree.detach(item)

            print(len(self.deleted_items))
            for item in self.deleted_items[::-1]:
                self.tree.move(item[1], "", item[0])
            
            self.deleted_items.clear()

        else:
            for item in self.tree.get_children():
                self.deleted_items.append((self.tree.index(item), item))
                self.tree.detach(item)
        
            for item in self.deleted_items:
                if self.tree.item(item[1], 'values')[1] == ip_filter or self.tree.item(item[1], 'values')[2] == ip_filter or self.tree.item(item[1], 'values')[3] == request_method:
                    self.tree.move(item[1], "", item[0])
                    #self.tree.reattach(item[1], '', 'end')

        
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.context_menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketListApp(root)
    sniffer = Sniffer.Sniffer(app)
    app.set_sniffer(sniffer)
    sniffer.start()
    root.mainloop()
