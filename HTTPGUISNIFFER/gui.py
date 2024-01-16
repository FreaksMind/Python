import tkinter as tk
from tkinter import ttk
import os
from threading import Thread
import Sniffer
import utils


class HTTPSNIFFER:
    def __init__(self, root):
        self.root = root
        self.sniffer = None
        self.sniffer_running = True
        self.packets = []
        self.deleted_items = []
        self.filtered_packets = 0
        self.packet_counter = 0

        self.root.title("HTTP SNIFFER")

        self.root.option_add('*tearOff', False)
        
        self.menu_bar = tk.Menu(self.root)
        self.sniffer_menu = tk.Menu(self.menu_bar)
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

        self.tree.tag_configure('GET', background='khaki')
        self.tree.tag_configure('POST', background='brown2')
        self.tree.tag_configure('PUT', background='lightskyblue')
        self.tree.tag_configure('PATCH', background='gray')
        self.tree.tag_configure('DELETE', background='darkseagreen3')
        self.tree.tag_configure('HEAD', background='darkturquoise')
        self.tree.tag_configure('OPTIONS', background='dodgerblue3')
        self.tree.tag_configure('none', background='white')

        self.tree.pack(expand=True, fill=tk.BOTH)


        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

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


        self.left_status_label1 = tk.Label(self.status_bar_frame1, text=f"Packets filtered: 0", anchor=tk.W, padx=5)
        self.left_status_label1.pack(side=tk.LEFT)

        self.update_status_bar()

    def show_packet_details(self, event):        
        """
        Function to show more details about a selected packet

        Args:
            self (HTTPSNIFFER): the HTTPSNIFFER object instance to acces the selected packet

        Returns:
            None
        """
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            
            packet_number = int(item[0])

            self.detail_text.delete(1.0, tk.END)
            details = ""

            ip_info = utils.parse_ip_header(self.packets[packet_number])
            tcp_info = utils.parse_tcp_header(self.packets[packet_number][ip_info['ihl']:])
            payload = utils.parse_http_payload(self.packets[packet_number][ip_info['ihl'] + tcp_info['header_length']:])
            details += f'Source address: {ip_info['src_ip']}\n'
            details += f'Source port: {tcp_info['src_port']}\n'
            details += f'Destination address: {ip_info['dest_ip']}\n'
            details += f'Destination port: {tcp_info['dest_port']}\n'
            details += f'TTL: {ip_info['ttl']}\n'
            

            details += '\nHEADERS:\n\n'
            for h in payload[1]:
                details += h + '\n'


            details += '\nPAYLOAD:\n\n'
            details += payload[2]

            self.detail_text.insert(tk.END, details)

    def add_packet(self, packet):
        """
        Function to add a new packet to the packet list and to the treeview

        Args:
            self (HTTPSNIFFER): the HTTPSNIFFER object instance to add the packet to
            packet (bytes array): the bytes array of the packet to be added to the list

        Returns:
            None
        """
        self.packets.append(packet)
        ipinfo = utils.parse_ip_header(packet)
        source = ipinfo['src_ip']
        destination = ipinfo['dest_ip']
        protocol = ipinfo['protocol']
        output = utils.parse_tcp_header(packet[ipinfo['ihl']:])
        packet_payload = utils.parse_http_payload(packet[ipinfo['ihl'] + output['header_length']:])
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
        """
        Function to call the pause function of the sniffer.

        Args:
            self (HTTPSNIFFER): the HTTPSNIFFER object instance to access sniffer object

        Returns:
            None
        """
        self.sniffer.pause()
        self.sniffer_running = False

    def resume_sniffer(self):
        """
        Function to call the unpause function of the sniffer.

        Args:
            self (HTTPSNIFFER): the HTTPSNIFFER object instance to access sniffer object

        Returns:
            None
        """
        self.sniffer.resume()
        self.sniffer_running = True

    def update_status_bar(self):
        """
        Function called every 1 second to update the information on the bottom of the window

        Args:
            self (HTTPSNIFFER): the HTTPSNIFFER object instance to access the labels

        Returns:
            None
        """
        self.left_status_label.config(text=f"Packets received: {self.packet_counter}")
        self.right_status_label.config(text="Sniffer: " + "".join('Running' if self.sniffer_running is True else 'Paused'))
        self.left_status_label1.config(text=f"Packets filtered: {self.filtered_packets}")

        self.root.after(1000, self.update_status_bar)

    def apply_filters(self):
        """
        Function to filter the packets based on 2 conditions (IP ADDRESS and REQUEST METHOD)

        Args:
            self (HTTPSNIFFER): the HTTPSNIFFER object instance to access the packets and the filters

        Returns:
            None
        """
        self.filtered_packets = 0
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
                if request_method != '' and ip_filter != '':
                    if (self.tree.item(item[1], 'values')[1] == ip_filter or self.tree.item(item[1], 'values')[2] == ip_filter) and self.tree.item(item[1], 'values')[3] == request_method:
                        self.filtered_packets += 1
                        self.tree.move(item[1], "", item[0])
                        #self.tree.reattach(item[1], '', 'end')
                else:
                    if self.tree.item(item[1], 'values')[1] == ip_filter or self.tree.item(item[1], 'values')[2] == ip_filter or self.tree.item(item[1], 'values')[3] == request_method:
                        self.filtered_packets += 1
                        self.tree.move(item[1], "", item[0])
                        #self.tree.reattach(item[1], '', 'end')


if __name__ == "__main__":
    root = tk.Tk()
    app = HTTPSNIFFER(root)
    sniffer = Sniffer.Sniffer(app)
    app.set_sniffer(sniffer)
    sniffer.start()
    root.mainloop()