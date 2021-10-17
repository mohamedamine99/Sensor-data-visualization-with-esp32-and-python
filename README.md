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
    <li><a href="#acknowledgements">Acknowledgements</a></li>
       
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


  ``` 
  ## Results:
  
  ![results](https://github.com/mohamedamine99/Ninja-Fruit-Like-Game-with-hand-gesture-and-opencv/blob/main/results.gif)
  
  ## Conclusion:
In this project, we successfullty detected and tracked a hand and its landmarks ,using the mediapipe module, and were able to extract data in order to create an interactive hand gesture mini-game with basic gameplay features such as  score , difficulty level and losing conditions.
  
  ### Contact:
* Mail : mohamedamine.benabdeljelil@insat.u-carthage.tn -- mohamedaminebenjalil@yahoo.fr
* Linked-in profile: https://www.linkedin.com/in/mohamed-amine-ben-abdeljelil-86a41a1a9/

### Acknowledgements:
* Google developers for making the [Mediapipe hand tracking module](https://google.github.io/mediapipe/solutions/hands)
* OpenCV team for making the awesome [Opencv Library](https://opencv.org/)
* [NumPy Team](https://numpy.org/gallery/team.html) for making the [Numpy Library](https://numpy.org/about/)
