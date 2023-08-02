# Python Real-World Projects -- Project Zero: A template for other projects
# Project 0.

Feature: The Cheerful Greeting CLI interface provides a greeting
    to a specific name.

Scenario: The application writes the greeting message.
  When we run command "python src/hello_world.py"
  Then output has "Hello, World!"
