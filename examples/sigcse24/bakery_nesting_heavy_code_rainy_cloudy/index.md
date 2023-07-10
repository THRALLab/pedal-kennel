Copy over the dataclasses you defined in the previous problem. Then, define the function `rainiest_cloudy` that consumes a list of `Forecast` and produces a boolean representing whether or not the day with the *most* rainfall was `cloudy`.

If there were no days in any reports, then just return `False`.

**Hint:** Write a helper function that consumes a list of `Forecast`s and returns a list of `Report`s by using the Map pattern appropriately.