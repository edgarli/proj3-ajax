# proj3-ajax
Reimplement the RUSA ACP controle time calculator with flask and ajax

## ACP controle times

That's "controle" with an 'e', because it's French, although "control" is also accepted.  Controls are points where 
a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must
arrive at the location.  

The algorithm for calculating controle times is described at http://www.rusa.org/octime_alg.html . The description is ambiguous, but the examples help.  Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly. 

We are essentially replacing the calculator at http://www.rusa.org/octime_acp.html .  We can also use that calculator to clarify requirements.  

## AJAX and Flask reimplementation

The current RUSA controle time calculator is a Perl script that takes an HTML form and emits a text page. The reimplementation will fill in times as the input fields are filled.  Each time a distance is filled in, the corresponding open and close times should be filled in.

## Requirements.txt
Flask==0.10.1
Jinja2==2.8
MarkupSafe==0.23
Werkzeug==0.10.4
arrow==0.6.0
itsdangerous==0.24
python-dateutil==2.4.2
six==1.10.0

## introduction of rules
this calculation app is based on ACP Brevet Control calculator algorithm. opentime output is using the maximum speed to calculate. closetime is using the minimum speed to calculate. the detail of max speed and min speed at the http://www.rusa.org/octime_alg.html.

## notes
 the last controle distance should be between the brevet distance and that distance plus 10%.
 brevet distance in range of (200, 300, 400, 600, 1000)

