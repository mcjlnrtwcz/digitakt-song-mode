# TODO
* get rid of magic numbers, and 24 * 4
* midi wrapper
* configurable midi channel, closing and opening ports as necessary - check if requested port exists etc.
* handle muting tracks
* block midi out option menu when running
* block bpm when running
* quantized stop - finish on measure (or configurable in the future)
* comparison between counters (counterdelta?)
* previous/current/next pattern label
* serialize and validate data from JSON
* create event class, PatternSequence is an Event, and there's Stop event
* support for other measure counts than 4/4 (counter implementation!)
* logging wrapper for setting timestamp
* advanced logging with module name printed