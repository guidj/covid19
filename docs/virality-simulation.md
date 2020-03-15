---
title: "Virality Simulation"
navigation_weight: 2
---
{% include_relative _partials/head.html %}

# Virality

Here, I briefly discuss the rate of new confirmed cases.
To understand the importance of monitoring the rate of new cases, we can do a simulation.
In the chart below, we plot the number of cases that would exist in the world
comparing three different rates: 1.5, 2.0, and 2.5.

{% include_relative _partials/virality-simulation.html %}

This simulation assumes a starting point of five cases for every scenario. 
Despite the small difference between the rates, we see vast differences in the number of cases, as time goes by.
Exactly 15 days after our starting point of five cases, we end up with roughly 1,500 (1.5), 80,000 (2.0) or 1,800,000 cases (2.5).
This is because with each day, the number of new cases of infection ($$\Delta N_{d}$$) is a based on the 
number of people that were infected on that day ($$N_{d}$$), the number of people exposed to them ($$E$$),
and the likelihood of transmitting the virus ($$p$$).

$$
\begin{align*}

  \Delta N_{d} = E * p * N_{d}
\end{align*}
$$

Back in late January, the number of confirmed cases started spiking.
On the 28th of January, the rate was around 1.9.
A few days before the rate peaked in January, measures were put in place in Wuhan to
prevent further spread of the virus.
Namely, the entire city of Wuhan was placed under quarantine.
While unprecedented, I believe this played a non-trivial role in diminishing exposure.
Likewise, around the world, actions that reduce the exposure to virus, such as
cancelling large gatherings, are critical to reduce its impact.
The earlier the better, as we've seen with the simulation.

Isolation can be rather difficult and strange. 
And some of those disruptions will undoubtably have medium and long terms consequences to different sectors
of the economy. 
Not to mention that people's personal lives are also being disrupted, through the delay
of planned events or distancing from their loved ones.
So I think it's important to know why we need to do this still.

An analysis on the largest group of infected people, 
[44,000 from China](https://www.telegraph.co.uk/global-health/science-and-disease/coronavirus-new-data-china-tells-us-disease/), 
shows that approximately 5% of the infected people need critical care, and 14% had a severe case.
Assuming the worst case scenario with the projection above, 5% of 1.8M is 90,000 and 14% is 252,000.
That many patients in need of care, either critical or moderate, is extremely hard if not impossible to manage with the health
care infrastructure of most countries. And that's with 15 days only. And from a starting point of five patients.
The virus has been spreading for over 60 days now.

Today (March 16, 2020), our current starting point is 145,000 cases, and the rate of new cases is slightly above 1.1. 
For as long as the rate of new cases remains above 1.0, we have more new confirmed cases each day than we did the day before.
And the only way to stop this is to either reduce the number of currently infected people - 
e.g. though vaccination, which we're still far more - or more realistic by reducing the chances
of new infection by bringing down exposure, i.e. isolating people as much as possible.

Note that though I think there should be concern, I don't think there is reason for grave panic about the virus itself.
Being a new strain, there is much we're still learning about it. 
We know that the [elderly and the sick are at a higher risk than others](https://www.bbc.com/news/world-asia-china-51540981), but
young adults are not immune to it. And while children are [less likely to fall sick, they tend to exhibit only
mild symptoms](https://www.cdc.gov/coronavirus/2019-ncov/prepare/children-faq.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fspecific-groups%2Fchildren-faq.html), and can more easily go unnoticed.

These are unusual times, and they require unusual and measured responses.
Doing so also buys [time for treatment options](https://time.com/5790545/first-covid-19-vaccine/).
The sooner we're safer, the sooner we can return to normal life.


Helpful Material:

  - [Exponential Growth and Epidemics from 3Blue1Brown (Youtube)](https://www.youtube.com/watch?v=Kas0tIxDvrg)
  - [Prof. Marcel Salathé - COVID update 8.3.2020 (Youtube)](https://www.youtube.com/watch?v=u0cjSnAynGs):
  video about the pandemic curve and discussion on COVID-19 from a professor of Epidemiology at EPFL, Marcel Salathé.
  - [Social Distancing: This is not a Snow Day](https://www.ariadnelabs.org/resources/articles/news/social-distancing-this-is-not-a-snow-day/):
  article from MD and director of the Ariadne Labs (Boston), Asaf Bitton, on why people should isolate themselves and what they can do to care for themselves and others.