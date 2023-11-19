from tkinter import *
from tkinter import messagebox
import requests
from api_key import key
import logging

# Logs configurations
# a logs.log file will be created in logs folder
# logs from INFO level above will be displayed
logging.basicConfig(filename="C:/Users/Ysa/PycharmProjects/Weather_app/logs/logs.log",
                    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Interface
root = Tk()
root.geometry("700x350")
root.resizable(True, False)
root.title("Weather")
root.iconbitmap("icons_vreme/logo_api.ico")


class Application:
    def __init__(self, main):
        # Label widget is created for the text: "Insert the city name:"
        self.city_head = Label(main, text='Insert the city name:', font='Calibri 12 bold')
        self.city_head.pack(padx=20, pady=5)

        # Entry widget is created for the user to write the city
        self.user_input = StringVar()
        self.city_entry = Entry(main, width=36, textvariable=self.user_input,
                                justify=CENTER, foreground="black",
                                font='Calibri 12 bold')
        self.city_entry.pack(padx=20, pady=7)

        # Button widget is created for Search function
        # a picture (deget.png) is displayed
        self.deget_pic = PhotoImage(file="icons_vreme/deget.png")
        self.search_btn = Button(main, text="Search",
                                 width=92, bg="azure3",
                                 font="Calibri 16 bold",
                                 command=self.search,
                                 relief="ridge",
                                 borderwidth=7,
                                 padx=15, pady=6,
                                 image=self.deget_pic,
                                 compound="left")
        self.search_btn.pack(pady=8)

        # Label widget is created for gray background from the bottom of the interface
        # the background appears only after the Search button is used
        self.label_background_color = Label(main, width=700, height=30)
        self.label_background_color.place(x=0, y=230)

        # Label widget is created for displaying the city and the country
        self.location_city_country = Label(main, text="", font=("Calibri", 36), foreground="red3")
        self.location_city_country.pack()

        # Label widget is created for displaying the temperature
        # a picture (poza_termometru.png) is displayed
        self.poza_termometru = PhotoImage(file="")
        self.temp_lbl = Label(main, text="",
                              font=("bold", 17),
                              image=self.poza_termometru,
                              compound="left")
        self.temp_lbl.place(x=45, y=250)

        # Label widget is created for the value of the wind
        # a picture (pic_vant.png) is displayed
        self.pic_vant = PhotoImage(file="icons_vreme/pic_vreme.png")
        self.vant_lbl = Label(main, text="",
                              font=("bold", 17),
                              compound="left")
        self.vant_lbl.place(x=270, y=265)

        # Label widget is created for displaying the atmospheric status
        # a picture (poza_vreme.png) is displayed
        self.poza_vreme = PhotoImage(file="")
        self.vremea_lbl = Label(main, text="",
                                font=("bold", 17),
                                foreground="black",
                                image=self.poza_vreme,
                                compound="left")
        self.vremea_lbl.place(x=480, y=230)

    @staticmethod
    def get_weather(city):
        # the request taking into consideration the city and the key
        result = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + key)
        if result:
            result_json = result.json()  # the info received is contained in the variable result_json
            # the city, country, weather, temperature and the wind are extracted from json
            city = result_json["name"]
            tara = result_json["sys"]["country"]
            weather = result_json["weather"][0]["main"]
            temp_kelvin = result_json["main"]["temp"]
            temp_celsius = temp_kelvin - 273.15
            imagine = result_json["weather"][0]["icon"]
            vant = result_json["wind"]["speed"]
            rezultat_final = [city, tara, temp_celsius, weather, imagine, vant]
            # an info message is displayed in logs.log file
            logging.info("The request for data was made and successfully received!")
            return rezultat_final  # a list is returned
        else:
            return None

    def search(self):
        city = self.user_input.get()  # the information from Entry widget is stored in the variable "city"
        if not self.user_input.get():
            # pop up message when there is no entry
            messagebox.showinfo(title="Error", message="Please enter a city!")
            # a warning message is displayed in logs.log file
            logging.warning("No city name was provided!")
        else:
            # try/except when there are technical problems (no internet, maintenance, other technical issues)
            try:
                # get_weather funtion is called and the information is stored in the "vremea_final" variable (a list)
                vremea_final = self.get_weather(city)
                if vremea_final:
                    # the widgets are updated with the information received from get_weather() function
                    self.location_city_country["text"] = f"{vremea_final[0]}, {vremea_final[1]}"
                    self.temp_lbl["text"] = f" {vremea_final[2]:.0f}°C"
                    self.temp_lbl["bg"] = "azure3"
                    self.vremea_lbl["text"] = vremea_final[3]
                    self.vremea_lbl["bg"] = "azure3"
                    self.poza_vreme["file"] = f"icons_vreme/{vremea_final[4]}.png"
                    self.vant_lbl["text"] = f" {vremea_final[5]} m/s"
                    self.vant_lbl["image"] = self.pic_vant
                    self.vant_lbl["bg"] = "azure3"
                    self.label_background_color["bg"] = "azure3"
                    self.poza_termometru["file"] = f"icons_vreme/termometru.png"
                else:
                    # pop up message when the text from the Entry widget is not correct spelled (no city is recognized)
                    messagebox.showinfo(title="Error", message=f"No city with the name {city} was found!")
                    # a warning message is displayed in logs.log file
                    logging.warning("A wrong city name was provided!")
            except:
                # pop up message when there are technical problems (no internet, maintenance, other technical issues)
                messagebox.showinfo(title="Error", message=f"Technical problem, please check!")
                # an error message is displayed in logs.log file
                logging.error("There are some technical problems, please check!")

Application(root)

root.mainloop()
