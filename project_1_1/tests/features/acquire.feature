# Python Real-World Projects
# Project 1.1: Data Acquisition Base Application

Feature: Extract four data series from a file with the peculiar Anscombe Quartet format.

Scenario: When requested, the application extracts all four series.
  Given the "Anscombe_quartet_data.csv" source file exists
  And the "quartet" directory exists
  When we run command "python src/acquire.py -o quartet Anscombe_quartet_data.csv"
  Then the "quartet/series_1.json" file exists
  And the "quartet/series_2.json" file exists
  And the "quartet/series_3.json" file exists
  And the "quartet/series_3.json" file exists
  And the "quartet/series_1.json" file starts with '{"x": "10.0", "y": "8.04"}'


Scenario: When the file does not exist, the log has the expected error message.
  Given the "Anscombe_quartet_data.csv" source file does not exist
  And the "quartet" directory exists
  When we run command "python src/acquire.py -o quartet Anscombe_quartet_data.csv"
  Then the log contains "File not found: Anscombe_quartet_data.csv"

