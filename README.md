# A wheel glove

Build a simple human input device based on 3-axis accelerometer (MPU6050) gesture recognition on a glove form factor to intelligently interface with machines without touch and just in-air.

We draw inspiration from one of the greatest interface technology of our generation - the iPod wheel used for volume control, menu scrolling, etc. Our glove will give an extra spin to recognize human wheel gestures over the air.

<img src="ref/photo.png" alt="drawing" width="500"/>

The MPU6050 sensor talks to an Ardunio Uno which sends 3-axis accelerometer values periodically to a host machine. The host runs a simple 1-layer neural network to recognize a left or right wheel intent and gives a user feedback. A sample live demo is shown below.

![](ref/output.gif)
