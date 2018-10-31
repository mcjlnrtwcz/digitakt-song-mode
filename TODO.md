# TODO
* cleanup tkinter imports
* configure logger
* block midi out option menu when running
* block bpm when running
* quantized stop - finish on measure (or configurable in the future)
* processing instead of threading
* midi wrapper
* comparison between counters (counterdelta?)
* previous/current/next pattern label
* serialize data from JSON
* tempo from JSON
* create event class, PatternSequence is an Event, and there's Stop event
* support for other measure counts than 4/4
* when sequence reaches last patter, stop sequencer
* send clock before sending start (to maintain consistent tempo)