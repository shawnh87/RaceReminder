# racereminder_proj

http://racereminder.site

RaceRiminder is an email delivery (reminder) service for bike racers relying on BikeReg.com.

The majority of cycling events in the northeast are hosted via bikereg. Unfortunately, bikreg does not offer any service to let participants know of upcoming races that may interest them.

The project allows users to create an account with updateable race preferences. Based on these preferences, custom query strings and run dates are created for each user (run dates are based on user selected cadence and delivery weekday).

Daily there is a crontab that calls a custom management function looking for all users with scheduled run dates. On run the user will receive an email notification of all races that fit their preferences. Their user event page will be updated to reflect what was emailed.

This project is not a replacement for BikeReg, simply an enhancement.

Future enhancements: move static files to S3, add SSL protection, cut distribution over to stronger service (SES)
