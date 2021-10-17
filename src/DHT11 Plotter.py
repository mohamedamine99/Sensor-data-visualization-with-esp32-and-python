
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import date
from datetime import datetime
import serial

esp_board = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


today = date.today()
date = today.strftime("%b-%d-%Y")
print("date = ", date)

fig , (hum_plt, temp_plt) = plt.subplots(1,2,constrained_layout=False)

dates = list()
Hum = list()
m_Hum= list()
Temp = list()
m_Temp= list()
Temp_thresh_high_lst =list()
Hum_thresh_high_lst = list()
Temp_thresh_low_lst = list()
Hum_thresh_low_lst = list()


def mean(ls):
    moy=0
    if len(ls)>0:
        for i in ls:
            moy += i
        moy = moy / len(ls)
        return moy


def add_new_data(x):
    data = esp_board.readline()  # return data sent by the board as bytes
    str_data = data.decode('utf-8').rstrip()  # reformats the bytes into a string of characters
    if (len(str_data) > 0) and (str_data.isnumeric()):
        Temp_val = float(str_data[0:3]) / 10
        Hum_val = int(str_data[3:])
        print("Temp val = ", Temp_val, "Hum val = ", Hum_val)

        now = datetime.now()
        dates.append(now)
        Hum.append(Hum_val)
        Temp.append(Temp_val)

        Temp_thresh_high_lst.append(30)
        Hum_thresh_high_lst.append(60)
        Temp_thresh_low_lst.append(20)
        Hum_thresh_low_lst.append(30)


        m_hum = mean(Hum)
        m_Hum.append(m_hum)

        m_temp = mean(Temp)
        m_Temp.append(m_temp)

    hum_plt.cla()
    temp_plt.cla()

    hum_plt.set_title('Humdity')
    hum_plt.set_xlabel('Time')
    hum_plt.set_ylabel('Value')

    temp_plt.set_title('Temperature')
    temp_plt.set_xlabel('Time')
    temp_plt.set_ylabel('Value')



    """hum_plt.plot(dates,Hum,color = '#246fe5',label= 'Humidity')
    hum_plt.plot(dates,m_Hum, color='#444444', linestyle='--', label = 'Mean Humidity')

    temp_plt.plot(dates,Temp,color = '#dc0600',label= 'Temperature')
    temp_plt.plot(dates,m_Temp, color='#dc00d6', linestyle='--', label = 'Mean Temperature')"""

    hum_plt.plot(dates,m_Hum, color='#444444', linestyle=':', label = 'Mean Humidity')
    temp_plt.plot(dates, m_Temp, color='#dc00d6', linestyle=':', label='Mean Temperature')
    temp_plt.plot_date(dates, Temp,'r-', label= 'Temperature')
    hum_plt.plot_date(dates, Hum, 'b-', label='Humidity')

    temp_plt.plot(dates, Temp_thresh_high_lst, color='#f10d0d', linestyle='--', label='High temperature threshold')
    temp_plt.plot(dates, Temp_thresh_low_lst, color='#f10d0d', linestyle='--', label='Low Temperature threshold')
    hum_plt.plot(dates, Hum_thresh_high_lst, color='#f10d0d', linestyle='--', label='High Humidity threshold')
    hum_plt.plot(dates, Hum_thresh_low_lst, color='#f10d0d', linestyle='--', label='Low Humidity threshold')

    temp_plt.legend(loc = "upper left",ncol = 1 )
    hum_plt.legend(loc = "best",ncol = 1)
    fig.suptitle('DATE : ' + date, fontsize=16)
    fig.autofmt_xdate()


anim = FuncAnimation(fig,add_new_data,interval=1700)

plt.show()