# Python Real-World Projects -- Project 1.5: Acquire data from a SQL extract
Feature:
  Database Extraction.

@fixture.sqlite
Scenario: Extract data from the enterprise database

  Given a series named "test1"
  And sample values "[(11, 13), (17, 19)]"
  When we run the database extract command with the test fixture database
  Then log has INFO line with "series: test1"
  And log has INFO line with "count: 2"
  And output directory has file named "quartet/test1.csv"
