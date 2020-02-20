# racereminder_proj

racereminder.site

RaceRiminder is an email delivery (reminder) service for bike racers that relying on BikeReg.com. 

At least in the northeast, the majority of cycling events are hosted via bikereg. Unfortunatley, bikreg does not offer any service to let participants know of upcoming races that may interest them.

The project allows users to create an account and updateable preferences. Based on these preferences custom querystrings and run dates are created for each user (run dates are based on user selected cadence and delivery weekday).

Daily there is a crontab that calls a custom management function looking for all users with scheduled rundates. On run the user will receive an email notificaiton of all races that fit their preferences. Their user event page will be updated to reflect what was emailed.

This project is not a replacement for BikeReg, simply an enhancement. 

