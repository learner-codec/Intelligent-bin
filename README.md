# Intelligent-bin
### Intelligent waste-bin for Smart cities. A project to develop an AI solution to waste management in Smart Cities (Jiangsu, Huaian, HYIT)
There are two deployed Bins, One In a small community area near Wanda plaza and another Downstairs of School of Computer and Software Engineering LAB
This Video was made as a demonstration of The *Intelligent Bin* Installed In the LAB
```
For The Instructions and Design Of the project please contact me
```
---


[Bin first Demo](https://github.com/learner-codec/Intelligent-bin/assets/56203705/ccdd191c-6438-4bdf-9d8b-663f6bf8ae89)




---
# Architecture
---
<div align="center">
<img src="https://github.com/learner-codec/Intelligent-bin/assets/56203705/80d8f3a1-eaf2-47f3-b406-a40ad6f7ee50" />
</div>

### 1.Hardware Setup For the doors and garbage measurement system
- For the micro controller we have used Jetson tx1.
![scematic](https://github.com/learner-codec/Intelligent-bin/assets/56203705/34d2b43a-06d3-4890-ab32-602f0b77b545)


### 2.Custom Designed Trash Bin
- for weight and volume measurement. Weight sensor is used to measure the weight and for volume measurement we have used the ultrasonic sensor on top as shown in 1.
<div align="center">
<img width="665" alt="bin_design" src="https://github.com/learner-codec/Intelligent-bin/assets/56203705/c10a09ee-e6f4-4e2f-8f98-74066b4e8645">
</div>


### 3. Actuators for the Doors.
<div align="center">
<img width="656" alt="actuator" src="https://github.com/learner-codec/Intelligent-bin/assets/56203705/39a9ada7-6e41-43f4-ae14-83463cbb82f3">
</div>

### 4. SOftware Design

The software is developed in python and C, Python is used for Web interface and Object recognition task and C is used for the drivers and on low level horware.
<div align="center">
<img src="https://github.com/learner-codec/Intelligent-bin/assets/56203705/f004c9da-e4cf-442c-bb8f-c541231627e9"/>
</div>

### 5. Hardware Requirements

| Item name	| Date needed |
|---|---|
| Jetson TX2	| 16.11.21 |
| Arduino	| 23.11.21 |
| Weight sensors	| 23.11.21 |
| Ultrasonic sensors	| 23.11.21 |
| Door sensors	| 23.11.21 |
| Actuators	| 23.11.21 |
| Bin housing	| 26.12.21 |

