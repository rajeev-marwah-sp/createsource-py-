getoken.py - Gets the token from the IdentityNow tenant using the credentials from config.ini file
Createsource_agg.py - Creates the source and aggregates the accounts, uses input from Input.csv to get the inputs
Uncorrelatedaccounts.py - Provides report about the uncorrelated accounts, takes input from sourceout.csv

config.ini - Contains Pat ID, Pat Secret , URL
Input.csv - Input file to create source script, contains all necessary parameters for building the source
sourceoutput.csv - Contains the source Id of the source , this is an input to the uncorrelated accounts script