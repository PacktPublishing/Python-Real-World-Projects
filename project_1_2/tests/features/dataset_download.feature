# Python Real-World Projects -- Project 1.2: Acquire data from web service
Feature:
  The application will download a dataset from Kaggle.com

@fixture.kaggle_server
Scenario: Request for carlmcbrideellis/data-anscombes-quartet extracts file from ZIP archive.
    The download command is
    "python src/acquire.py -k kaggle.json -o quartet \
      --zip carlmcbrideellis/data-anscombes-quartet"

  Given proper keys are in "kaggle.json"
  When we run the kaggle download command
  Then log has INFO line with "header: ['mock', 'data']"
  And log has INFO line with "count: 1"
