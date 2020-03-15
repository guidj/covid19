---
title: "Virality Simulation"
---
{% include_relative _partials/head.html %}

# Virality

Here, I briefly discuss the rate of new cases of confirmed cases.
Back in late January, the number of confirmed cases started spiking.
On the 28th of January, it was around 1.9.

To understand the importance of monitoring the rate of new cases, we can do a simulation.
In the chart below, we plot the number of cases that would exist in the world
comparing three different rates: 1.5, 2.0, and 2.5.

{% include_relative _partials/virality-simulation.html %}

This simulation assumes a starting point of five cases for every scenario. 
Despite the small difference between the rates, we see vast differences in the number of cases, as time goes by.
Exactly 15 days after our starting point of five cases, we end up with roughly 1,500 (1.5), 80,000 (2.0) or 1,800,000 cases (2.5).
This is because with each day, the number of new cases of infection ($$\Delta N_{d}$$) is a based on the 
number of people that were infected the day before ($$N_{d}$$), the number of people exposed to them ($$E$$),
and the likelihood of transmitting the virus ($$p$$).

$$
\begin{align*}

  \Delta N_{d} = E * p * N_{d}
\end{align*}
$$

A few days before the rate peaked in January, measures were put in place in Wuhan to
prevent further spread of the virus. 
While unprecedented, I believe they played a non-trivial role in diminishing exposure.
Likewise, around the world, actions that reduce the exposure of the virus, such as
cancelling large gathering, are critical to reduce it's impact. 
The earlier the better, as we've seen with the simulation.

Note that though I think there should be concern, I don't think there is reason for grave panic about the virus itself.
Being a new strain, there is much we're still learning about it. 
We know that the [elderly and the sick are at a higher risk than others](https://www.bbc.com/news/world-asia-china-51540981).
But measures of precaution can prevent wider spread, as advised by local authorities.
It is true that quarantines can disrupt businesses and every day life.
And some of those disruptions will undoubtably have medium and long terms consequences to different sectors
of the economy. 
But these are unusual times, and they require unusual and measured responses.
Doing so also buys [time for a vaccine](https://time.com/5790545/first-covid-19-vaccine/).
The sooner we're safer, the sooner we can return to normal life.


Helpful Material:

  - [Exponential Growth and Epidemics from 3Blue1Brown (Youtube)](https://www.youtube.com/watch?v=Kas0tIxDvrg)