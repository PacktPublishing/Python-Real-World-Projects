# Python Real-World Projects -- Project 1.3: Scrape data from a web page
Feature: Extracts table from Wikipedia Page

Scenario: Finds captioned table and extracts data.
    The command is
      python src/acquire.py -o quartet --page "$GIVEN_FILENAME" --caption "Anscombe's quartet"

  Given an HTML page "example_1.html"
    """
      <!DOCTYPE html>
      <html>
      <head></head>
      <body>
      <p>Some Text</p>
      <table class="wikitable">
          <tbody>
          <tr><th>Wrong Table</th></tr>
          <tr><td>Wrong Table</td></tr>
          </tbody>
      </table>
      <table class="wikitable">
          <caption>Anscombe's quartet
          </caption>
          <tbody>
          <tr><th>Skip titles</th><th>In th tags</th></tr>
          <tr><td>Keep this</td><td>Data</td></tr>
          <tr><td>And this</td><td>Data</td></tr>
          </tbody>
      </body>
      </html>
    """
  When we run the html extract command
  Then log has INFO line with "header: ['Keep this', 'Data']"
  And log has INFO line with "count: 1"
