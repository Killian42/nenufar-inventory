# nenufar-inventory
Makes an inventory of pulsar observations from NenuFAR, along with a database containing the main parameters of the observed pulsars, and how much they have been observed. A timeline of these observations is made in pdf format.

The observation inventory is stored in the *pulsar-obs-inventory-**date**.csv* file and the parameters/observation information is stored in the *psr_info.csv* file.

The code to make the observation timeline (*obs-timeline.py*) can be run on its own once the inventory file is created. 

## How to use
* Install the project with git
* Move into the newly created directory
* Execute the *launcher.sh* file
* Enjoy!

*obs-timeline.py* has the following command line arguments:
* -s,--scope : Makes the timeline for the last week (*thisweek* option) or since the beginning (*all* option) (Default: *all*)
* -e,--email : Sends the pdf by email to the given email adresse(s) (Default: None)
These options can be given directly when running *launcher.sh*, they will be relayed to *obs-timeline.py*.

## Requirements
* Python3 with the following packages:
  * numpy
  * pandas
  * matplotlib
  * astropy
  * psrqpy (version 1.2.6 or higher is best)
  * warnings, os, glob, argparse, subprocess and datetime (usually installed by default)

* psrchive
* Linux distribution with the following utilities:
   * bc (Basic Calculator)
   * mail

## Additional info
* You can safely ignore the ```ls: cannot access '*.fits': No such file or directory``` error messages when the inventory is being created, they come up when the directory for an observation mode is empty.
