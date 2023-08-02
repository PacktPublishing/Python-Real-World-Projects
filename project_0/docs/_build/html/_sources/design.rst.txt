..  Python Real-World Projects -- Project Zero: A template for other projects

######
Design
######

The application has the following
structure:

..  uml::

    class hello_world.greeting << (F, white) >> {
    }
    hide hello_world.greeting members

    class hello_world.main << (F, white) >> {
    }
    hide hello_world.main members

    class hello_world.get_options << (F, white) >> {
    }
    hide hello_world.get_options members

    hello_world.main -> hello_world.get_options : "calls"
    hello_world.main -> hello_world.greeting : "calls"


There are three functions that interact to produce
the greeting.
