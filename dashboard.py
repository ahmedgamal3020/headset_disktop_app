from customtkinter import *
from PIL import Image
import tkinter as tk
import editing
import serial_data 
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy.engine import create_engine
import psycopg2
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%Y/%m/%d")


class Dashboard(CTkFrame):
    
    
    
    def filter_list(self,event):
        search_text = self.sreach_1.get().lower()
        
        filtered_list = [item for item in self.dataa if search_text in item.lower()]
        self.listbox.delete(0, tk.END)
        print('ahmed'+f'{len(filtered_list)}')
        for item in filtered_list:
            self.listbox.insert(tk.END, item)
        if len(filtered_list) == len(self.dataa):
            self.listbox.config(height=10)
        elif len(filtered_list) <= 35:
            self.listbox.config(height=self.listbox.size())
        elif len(filtered_list) > 35:
            self.listbox.config(height=35)
        elif len(filtered_list) == 0:
            self.listbox.config(height=0)

    def but(self):
        self.sreach_1.delete(0,END)
        self.editing_frame.pack_forget()
        self.editing_frame = editing.details_about(
        self,
        self.tabview.tab("Editing"),
        self.tabview,
        frame="",
        )
        self.tabview.set("Editing")
        self.listbox.get(0)
    
    def on_select(self, event='',selected_item=''):
        selected_index = self.listbox.curselection()
        if selected_index and selected_item != '':
            selected_item = self.listbox.get(selected_index[0])
            self.agent_data=self.work[self.work['agent_id'].isin([selected_item])]
            self.editing_frame.pack_forget()
            self.editing_frame = editing.details_about(
            self,
            self.tabview.tab("Editing"),
            self.tabview,
            frame="",
            american_name=''.join (self.agent_data['status']),
            serial=''.join (self.agent_data['serial']),
            name=''.join (self.agent_data['name']),
            date=''.join (self.agent_data['date']),
            id=''.join (self.agent_data['agent_id']),
            headset_type=''.join (self.agent_data['headset_type'])

            )
            self.tabview.set("Editing")
            self.sreach_1.delete(0,END)
            
        else:
            pass  

        
       
        
    def press_enter(self,event):

        search_text = self.sreach_1.get().lower()
        listbox_item=self.listbox.get(0).lower()
        if search_text ==listbox_item :
            self.agent_d=self.work[self.work['agent_id'].isin([listbox_item.title()])]

            self.editing_frame.pack_forget()
            self.editing_frame = editing.details_about(
            self,
            self.tabview.tab("Editing"),
            self.tabview,
            dt_string=dt_string,
            frame="",
            american_name=''.join (self.agent_d['status']),
            serial=''.join (self.agent_d['serial']),
            name=''.join (self.agent_d['name']),
            date=''.join (self.agent_d['date']),
            id=''.join (self.agent_d['agent_id']),
            headset_type=''.join (self.agent_d['headset_type'])
        )
            self.tabview.set("Editing")
            self.sreach_1.delete(0,END)
            

        else:
            print('ahmedssss')
    
    def clean(self):
        self.editing_frame.pack_forget()
        self.serial_frame.pack_forget()
        self.editing_frame = editing.details_about(
            self,
            self.tabview.tab("Editing"),
            self.tabview,
            )
        self.serial_frame = serial_data.getmeframe(
            self,
            self.tabview.tab("Serial"),
            self.tabview,
            self.parent_hight,
            self.parent_width,
            data=self.data,
           )
        self.sreach_1.delete(0,END)
        self.refresh_data()
    
    def show_toast(message):
        pass
    def remove_levers(self):
        self.connection
        levers=self.headset_data[self.headset_data['agent_id'].isin(self.levers)]
        levs=str("""','""".join( levers['agent_id']))
        # self.headset_data=self.headset_data[~self.headset_data['status'].isin(self.levers)]
        mess=f'Leavers removed : {levers.shape[0]}'
        self.show_toast()
        sql_query = f"""update headset SET status='available' WHERE agent_id IN('{levs}')"""
        sql_query = f"""update serial_hestory SET last_date='{dt_string}' WHERE agent_name IN('{levs}')"""
        self.cursor.execute(sql_query)
        self.connection.commit()
        self.refresh_data()
        duration=3000
        # Create a top-level window
        toast = tk.Toplevel()
        toast.wm_overrideredirect(True)  # Remove window decorations (border, close button, etc.)
        
        # Get the screen width and height
        screen_width = toast.winfo_screenwidth()
        screen_height = toast.winfo_screenheight()
        
        # Set the dimensions and position of the toast
        width = 300
        height = 50
        x = (screen_width // 2) - (width // 2)  # Center horizontally
        y = screen_height  - height -50  # Center buttomly
        toast.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create a label to display the message
        label = tk.Label(toast, text=mess, bg="black", fg="white", font=("Helvetica", 12))
        label.pack(expand=True, fill='both')
        
        # Make the window semi-transparent
        toast.attributes("-alpha", 0.8)
        
        # Destroy the toast after the specified duration
        toast.after(duration, toast.destroy)
        
        
    def __init__(self, app, parent_hight, parent_width, old_frame=""):
        self.parent_hight = parent_hight
        self.parent_width = parent_width
        super().__init__(app)
        if old_frame == "":
            pass
        else:
            old_frame.pack_forget()
        self.tabview = CTkTabview(app,command=self.clean)
        
        self.data=self.headset_data
        self.dataa=[]
        self.data['status']=self.data['status'].str.title()
        self.data['name']=self.data['name'].str.title()
        self.data['serial']=self.data['serial'].str.title()
        self.data['headset_type']=self.data['headset_type'].str.strip().replace(' ','').str.title()
        self.working=self.data[~self.data.status.isin(['Available','Not Available'])]
        self.avalible=self.data[self.data.status.isin(['Available'])]
        self.not_avalible=self.data[self.data.status.isin(['Not Available'])]
        self.dataa=self.working['agent_id'].unique()
        self.work=self.working
        self.tabview.add("Dashboard")
        self.tabview.add("Editing")
        self.tabview.add("Serial")

        self.editing_frame = editing.details_about(
            self,
            self.tabview.tab("Editing"),
            self.tabview,
            )
        self.serial_frame = serial_data.getmeframe(
            self,
            self.tabview.tab("Serial"),
            self.tabview,
            parent_hight,
            parent_width,
            data=self.data,
           )
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        self.frame = CTkFrame(master=self.tabview.tab("Dashboard"))
        
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure((0, 1), weight=0)
        self.frame.grid_rowconfigure((2), weight=1)
      

        self.cus_font = CTkFont(family="arial", weight="bold", size=40)
        self.cus_font2 = CTkFont(family="arial", weight="bold", size=20)
        self.img = Image.open(
            r"assets/pngimg.com - headphones_PNG101962.png"
        )
        self.imag = CTkImage(
            self.img,
            size=(self.parent_width * 0.15, self.parent_hight * 0.15),
        )
    
        # ###############################################image######################################################
        self.frame_image = CTkFrame(master=self.frame, fg_color="transparent")
        self.frame_image.grid(row=0, column=0, sticky="wnse", padx=10, pady=(10, 10))
        self.frame_image.grid_columnconfigure(0, weight=1)
        self.frame_image.grid_rowconfigure(0, weight=1)
        self.label = CTkLabel(master=self.frame_image, text="", image=self.imag)
        self.label.grid(row=0, column=0, sticky="wsne")
        # ################################################Total###############################################################

        self.frame_total = CTkFrame(master=self.frame)
        self.frame_total.grid(
            row=0, column=1, columnspan=2, sticky="wnse", padx=(0, 10), pady=(10, 10)
        )
        self.label1 = CTkLabel(master=self.frame_total, text="Total", font=self.cus_font)
        self.label1.pack(pady=(10))
        self.total = CTkLabel(master=self.frame_total, text=f"{self.data['status'].count()}", font=self.cus_font2)
        self.total.pack(pady=10)
        # ################################################################################################################

        self.frame_child1 = CTkFrame(master=self.frame)
        self.frame_child1.grid(row=1, column=0, sticky="wnse", padx=10, pady=(0, 10))
        self.labe2 = CTkLabel(
            master=self.frame_child1, text="Working", font=self.cus_font
        )
        self.labe2.pack(pady=(10, 0))
        self.total2 = CTkLabel(
            master=self.frame_child1, text=f"{self.working.shape[0]}", font=self.cus_font2
        )
        self.total2.pack(pady=10)

        self.frame_child2 = CTkFrame(master=self.frame)
        self.frame_child2.grid(
            row=1, column=1, sticky="wnse", padx=(0, 10), pady=(0, 10)
        )
        self.label3 = CTkLabel(
            master=self.frame_child2, text="Available", font=self.cus_font
        )
        self.label3.pack(pady=(10, 0))
        self.total3 = CTkLabel(
            master=self.frame_child2, text=f"{self.avalible.shape[0]}", font=self.cus_font2
        )
        self.total3.pack(pady=10)

        self.frame_child3 = CTkFrame(master=self.frame)
        self.frame_child3.grid(
            row=1, column=2, sticky="wnse", padx=(0, 10), pady=(0, 10)
        )
        self.label4 = CTkLabel(
            master=self.frame_child3, text="Not available", font=self.cus_font
        )
        self.label4.pack(pady=(10, 0))
        self.total4 = CTkLabel(
            master=self.frame_child3, text=f"{self.not_avalible.shape[0]}", font=self.cus_font2
        )
        self.total4.pack(pady=10)

    # ###############################search menu################################
        self.frame_child4 = CTkFrame(master=self.frame, corner_radius=0)
        self.frame_child4.grid(
            row=0, rowspan=4, column=3, sticky="wnse", padx=(0, 0), pady=0
        )
        self.frame_child4.pack_propagate(0)
        self.frame_child4.grid_columnconfigure(0, weight=1)
        self.frame_child4.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.label4 = CTkLabel(
            master=self.frame_child4, text="Title", font=self.cus_font
        )
        self.label4.pack()

        self.sreach_1 = CTkEntry(
            self.frame_child4,
        )
        self.sreach_1.pack(anchor="center", fill="both", padx=10, pady=(0, 10))
        self.sreach_1.bind("<KeyRelease>", 
                            lambda event : self.filter_list(event=event)
                            )
        self.sreach_1.bind("<Return>",lambda event :self.press_enter(event=event))

        self.listbox = tk.Listbox(self.frame_child4, bg="#333333", fg="#ffffff")
        for item in self.dataa:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(anchor="center", fill="both", padx=10, pady=(0, 10))
        self.listbox.bind("<<ListboxSelect>>",
                        lambda event : self.on_select(event=event,selected_item='1')
                            )

        self.button = CTkButton(
            master=self.frame_child4,fg_color='transparent',border_color='#2986CC',border_width=1,font=self.cus_font2, command=lambda: self.but(), text="add!"
        )
        self.button.grid(row=3, column=0, sticky="s", padx=10, pady=10)

        ############################################type1 frame#########################################
        self.sacFrame= CTkScrollableFrame(master=self.frame,fg_color='transparent')
        self.sacFrame.grid(
            row=2,
            columnspan=3, column=0, sticky="wnse", pady=(0, 10)
        )

        self.sacFrame.grid_columnconfigure((0), weight=1)
        self.sacFrame.grid_rowconfigure((0), weight=1)
        headset_type=self.data['headset_type'].unique()

        for i in range(len(headset_type)):
            self.frame_child5 = CTkFrame(master=self.sacFrame,fg_color='#2B2B2B')
            self.frame_child5.grid(
                row=i, column=0, sticky="wnse", pady=(0, 10)
            )
            
            self.frame_child5.grid_columnconfigure((0,1,2), weight=1)
            self.frame_child5.grid_rowconfigure((0,1,2), weight=1)
            
        
            self.label5 = CTkLabel(master=self.frame_child5,text=f'{headset_type[i]}',font=self.cus_font)
            self.label5.grid(row=i,column=0,columnspan=2,padx=5,pady=5,sticky='wn')

            self.label51 = CTkLabel(master=self.frame_child5,text='Working',font=self.cus_font2)
            self.label51.grid(row=i+1,column=0,padx=5,pady=5)
            self.label52 = CTkLabel(master=self.frame_child5,text='Available',font=self.cus_font2)
            self.label52.grid(row=i+1,column=1,padx=5,pady=5)
            self.label53 = CTkLabel(master=self.frame_child5,text='Not available',font=self.cus_font2)
            self.label53.grid(row=i+1,column=2,padx=5,pady=5)
            w=self.working[self.working['headset_type'].isin([headset_type[i]])].shape[0]
            v=self.avalible[self.avalible['headset_type'].isin([headset_type[i]])].shape[0]
            nv=self.not_avalible[self.not_avalible['headset_type'].isin([headset_type[i]])].shape[0]
            self.label512 = CTkLabel(master=self.frame_child5,text=f'{w}',font=self.cus_font2)
            self.label512.grid(row=i+2,column=0,padx=5,pady=5)
            self.label522 = CTkLabel(master=self.frame_child5,text=f'{v}',font=self.cus_font2)
            self.label522.grid(row=i+2,column=1,padx=5,pady=5)
            self.label532 = CTkLabel(master=self.frame_child5,text=f'{nv}',font=self.cus_font2)
            self.label532.grid(row=i+2,column=2,padx=5,pady=5)

        thred_frame=CTkFrame(master=self.frame,fg_color='transparent')
        thred_frame.grid(
            row=3,
            column=0,columnspan=3, sticky="w", pady=(0, 10)
        )
        remove_button=CTkButton(master=thred_frame,fg_color='transparent',border_color='#2986CC',border_width=1,
                        text='Remove leavers',command=lambda: self.remove_levers(),font=self.cus_font2) 
        remove_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.frame.pack()
        
    def refresh_data(self):
        # Retrieve new data from the database
        print('refresh')
        self.new_data =  pd.read_sql('''
            select * from headset
            ''',self.engine)
        self.new_data['headset_type']=self.new_data['headset_type'].str.strip().replace(' ','').str.title()
        self.data=self.new_data
        self.data['status']=self.data['status'].str.title()
        self.data['name']=self.data['name'].str.title()
        self.data['serial']=self.data['serial'].str.title()
        self.data['headset_type']=self.data['headset_type'].str.title()
        self.working=self.data[~self.data.status.isin(['Available','Not Available'])]
        self.avalible=self.data[self.data.status.isin(['Available'])]
        self.not_avalible=self.data[self.data.status.isin(['Not Available'])]
        self.dataa=self.working['agent_id'].unique()
        self.work=self.working

        self.frame.forget()
        self.create_widgets()
        # Refresh or redraw the tab
        self.tabview.update()
        self.serial_frame.pack_forget()

        self.serial_frame = serial_data.getmeframe(
            self,
            self.tabview.tab("Serial"),
            self.tabview,
            self.parent_hight,
            self.parent_width,
            data=self.new_data,
        
           )
        return self.new_data

    uri = "postgresql://postgres:%s@192.168.4.204/headset" % quote_plus("123321")
    engine = create_engine(uri)

    headset_data = pd.read_sql('''
        select * from headset
        ''',engine)
    connection = psycopg2.connect(
    database="headset", user="postgres", password="123321", host="192.168.4.204", port="5432")
    cursor = connection.cursor()
    try:
        levers=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSqnEbChd9UdQLAXWsFdWq0D6bqzWqXqprDcSBvQXczhu5ayehqtTreHcxTE5SuNAJmZaflZfwk-30C/pub?gid=1785867491&single=true&output=csv',low_memory=False,encoding='utf-8',usecols=['Column1']) 
        levers=levers['Column1'].unique()
        
    except Exception as e:
        levers=None
   