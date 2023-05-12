# nenufar-inventory
Makes an inventory of pulsar observations from nenufar, along with a database containing the main parameters of the observed pulsars and how much they have been observed.

The observation inventory is stored in the *pulsar-obs-inventory-**date**.csv* file and the parameters/observation information is stored in the *psr_info.csv* file.

The code to make the observation timeline (*obs-timeline.py*) can be run once the inventory file is created. 

## How to use
* Install the project with git
* Move into the newly created directory
* Execute the *launcher.sh* file
* Enjoy!

## Requirements
* Python3 with the following packages:
  * numpy
  * pandas
  * matplotlib
  * astropy
  * psrqpy (version 1.2.6 or higher is best)
  * warnings, os and glob (usually installed by default)

* psrchive
* Linux distribution with the following utilities:
   * bc (Basic Calculator)

## Additional info
* You can safely ignore the ```ls: cannot access '*.fits': No such file or directory``` error messages when the inventory is being created, they come up when the directory for an observation mode is empty.
