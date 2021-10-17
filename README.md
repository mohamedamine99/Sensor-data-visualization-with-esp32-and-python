# Sensor-data-visualization-with-esp32-and-python


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>  
    <li><a href="#hardware-requirements">Hardware Requirements</a></li>
    <li><a href="#software-requirements">Software Requirements</a></li>
      <ul>
        <li><a href="#python-environment">Python environment</a></li>
        <li><a href="#packages">Packages</a></li>
      </ul>
    </li>      
    <li><a href="#software-implementation">Software implementation</a></li>
      <ul>
        <li><a href="#arduino-code">Arduino code</a></li>
        <li><a href="#python-implementation">Python implementation</a></li>  
      </ul>
    <li><a href="#results">Results</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
    <li><a href="#contact">Contact</a></li>
       
  </ol>
</details>

## About the project
Our eyes are drawn to colors and patterns.  Data visualization is a form of visual art that grabs our interest and keeps our eyes on the message. When we see a chart, we quickly see trends and outliers.

This projects consists of sending DHT11 sensor data acquired on a esp32 board and visualizing the data with a python script using matplotlib
## Hardware Requirements:
* ESP32 board ( or any board compatible with arduino IDE)
* DHT11 temperature and humidity sensor
 
**PS** : if You dont have the entire DHT11 module then you would need a 10k ohm resistor

## Software Requirements:

### Python environment:

* Python 3 
* A python IDE , in my case I used [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/).
* Arduino IDE.

### Packages:
* [pySerial](https://pythonhosted.org/pyserial/) : It will allows access for the serial port.
* [Matplotlib](https://matplotlib.org/) : Matplot libs allows to make all types of plots and charts in order to properly and easily visualize data.
* [DHTNEW](https://github.com/RobTillaart/DHTNew) : **Arduino library** for DHT11 and DHT22 with automatic sensor type recognition.

**NB**: All these packages need to be installed properly.

## Software implementation:
### Arduino code:
* The first phase of this project is collecting data from our sensor. This is done using an Esp32 board and the code snippets below :
* First let's properly setup our variables:
 ```cpp
 #include <dhtnew.h>     // the dhtnew library to interface with our sensor

DHTNEW mySensor(15);    // attach the sensor data pin to the D15 pin of the esp32 board

byte H ;         // byte variable to store the humidity value read fro the sensor
float T;         // float variable to store the temperature value read fro the sensor

void setup()
{
  Serial.begin(115200);   // set communication rate with the serial port to 115200 bauds 
  mySensor.setSuppressError(true);
}
 ``` 
 * The humidity value was stored as byte ( values from 0 to 255) since in my case I didn't need the entire precision. the integer value was enough.
 * the `mySensor.setSuppressError(true)` line serves a very important role . the `getHumidity()` and  `getTemperature()` functions returns last read value (float) or -999 in case of error. This might cause huge negative spikes in case we want to properly visualize the data , hence `mySensor.setSuppressError(true)` suppresses the error and replaces the -999 value with the last correctly read value.
 
 * Now let's get to the loop function :
 
 ```cpp
void loop()
{
  if (millis() - mySensor.lastRead() > 2000) // get values from the sensor every 2 seconds
  {

    int errcode = mySensor.read();        //begin reading
    T = mySensor.getTemperature();        // getting the data
    H = mySensor.getHumidity();

    Serial.print(uint16_t(T*1000 + H)) ;  // sending the data via the serial port
    
  }
}
 ``` 
* explaining the `Serial.print(uint16_t(T*1000 + H))`  line :
* the humidity value is generally under 100 which means it has 2 digits.
* the temperature value is a float with one decimal number . so we multiply it by 1000 and add to it the humidity value and convert t to a 2-bytes-integer uint16_t
* example : say wa have a humidity value of 40 and a temperature value of 22.3 the value sent by the arduino is 223040. this 2-bytes value will be later converted to a string to be easily manipulated and to extract data with the python code.


### Python implementation:
Now let's get to our code:  
Let's begin with importing the required packages

 ```py
 
 import matplotlib.pyplot as plt                 # plotting 
from matplotlib.animation import FuncAnimation   # animating the plots since there are new values added in real-time
from datetime import date
from datetime import datetime
import serial                                    # For serial communication
  ``` 
  Let's establish a serial communication on `COM4` port with `115200` baud rate and 0.1 sec timeout: 
  
  ```py
esp_board = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
  ```  
  Let's setup our plotting variables : 
   
  ```py
  #get the current date in the OCT - 17 - 2020 format
today = date.today()
date = today.strftime("%b-%d-%Y")
print("date = ", date)

#setup a figure containing 2 plots (for humidity and temperature respactively) over one row and 2 columns
fig , (hum_plt, temp_plt) = plt.subplots(1,2,constrained_layout=False)

#The lists that contains the data 
dates = list()   # list of time frames for the x-axis
Hum = list()
m_Hum= list()    # mean humidity values
Temp = list()
m_Temp= list()   # mean temperatures values

# thresholds that will be represented by one dashed line each.
Temp_thresh_high_lst =list()
Hum_thresh_high_lst = list()
Temp_thresh_low_lst = list()
Hum_thresh_low_lst = list()
  ```  
  the below function to calculate the mean value of a list
  
 ```py 
  def mean(ls):
    moy=0
    if len(ls)>0:
        for i in ls:
            moy += i
        moy = moy / len(ls)
        return moy
 ``` 
    Now to the most important function that adds new data and plots.
  
```py  
  def add_new_data(x):
    data = esp_board.readline()                # return data sent by the board as bytes
    str_data = data.decode('utf-8').rstrip()   # reformats the bytes into a string of characters
    if (len(str_data) > 0) and (str_data.isnumeric()):
        Temp_val = float(str_data[0:3]) / 10    # the first 3 chars represent the temperature value
        Hum_val = int(str_data[3:])             # the last 2 chars represent the Humidity value   
        print("Temp val = ", Temp_val, "Hum val = ", Hum_val)
        
        # Get the current time and append it to the list
        now = datetime.now()              
        dates.append(now)
        
        # append data to the lists
        Hum.append(Hum_val)
        Temp.append(Temp_val)
        
        # Set the thresholds values
        Temp_thresh_high_lst.append(30)
        Hum_thresh_high_lst.append(60)
        Temp_thresh_low_lst.append(20)
        Hum_thresh_low_lst.append(30)

        # Calculate the means of data and append them to the means lists
        m_hum = mean(Hum)
        m_Hum.append(m_hum)
        m_temp = mean(Temp)
        m_Temp.append(m_temp)


    hum_plt.cla()
    temp_plt.cla()

    # Setting plot titles ans axis labels
    hum_plt.set_title('Humdity')
    hum_plt.set_xlabel('Time')
    hum_plt.set_ylabel('Value')

    temp_plt.set_title('Temperature')
    temp_plt.set_xlabel('Time')
    temp_plt.set_ylabel('Value')

    # Plotting the data
    hum_plt.plot(dates,m_Hum, color='#444444', linestyle=':', label = 'Mean Humidity')
    temp_plt.plot(dates, m_Temp, color='#dc00d6', linestyle=':', label='Mean Temperature')
    temp_plt.plot_date(dates, Temp,'r-', label= 'Temperature')
    hum_plt.plot_date(dates, Hum, 'b-', label='Humidity')
    # Plotting the threshold lines
    temp_plt.plot(dates, Temp_thresh_high_lst, color='#f10d0d', linestyle='--', label='High temperature threshold')
    temp_plt.plot(dates, Temp_thresh_low_lst, color='#f10d0d', linestyle='--', label='Low Temperature threshold')
    hum_plt.plot(dates, Hum_thresh_high_lst, color='#f10d0d', linestyle='--', label='High Humidity threshold')
    hum_plt.plot(dates, Hum_thresh_low_lst, color='#f10d0d', linestyle='--', label='Low Humidity threshold')
    # Adding legends and the title of the figure which is the current date 
    temp_plt.legend(loc = "upper left",ncol = 1 )
    hum_plt.legend(loc = "best",ncol = 1)
    fig.suptitle('DATE : ' + date, fontsize=16)
    fig.autofmt_xdate()  # to have a nice time format 
```
Let's actually animate and display the plots:
```py 
anim = FuncAnimation(fig,add_new_data,interval=1700)

plt.show()

```

  ## Results:
  
  
  
  ## Conclusion:
In this project, we successfullty collected data from DHT11 sensor send them to the pc via the serial communication and displayed the data  ,using the matplotlib module.
  
  ### Contact:
* Mail : mohamedamine.benabdeljelil@insat.u-carthage.tn -- mohamedaminebenjalil@yahoo.fr
* Linked-in profile: https://www.linkedin.com/in/mohamed-amine-ben-abdeljelil-86a41a1a9/
