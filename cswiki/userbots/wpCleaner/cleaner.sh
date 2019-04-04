#!/bin/bash

java -cp ~/bin/WikipediaCleaner.jar org.wikipediacleaner.Bot cs UrbanecmBot $(cat ~/.wpcleaner_botpassword) UpdateISBNWarnings
