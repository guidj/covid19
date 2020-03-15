---
title: "COVID19 Monitoring"
layout: default
navigation_weight: 1
---

# COVID-19 Monitoring

{% include_relative _partials/agg-chart.html %}

We monitor the number of confirmed cases and growth rate to understand how quickly we can expect
the virus to spread. There are caveats with this last measure:

   - It's computed based on the number of confirmed cases each day. Given that the virus
   has an [estimated incubation period of 5 days](https://annals.org/aim/fullarticle/2762808/incubation-period-coronavirus-disease-2019-covid-19-from-publicly-reported),
   there are likely more sick people each day than accounted for. This is compounded by cases
   that simply haven't been tested. This means *we can expect the actual rate to be higher
   than the one reported here*.
  - The disease is spreading at different rates around the world. The growth chart on top
  aggregates cases from everywhere, so expect regional variances depending on where you are.
  


To better understand the impact of the growth rate, refer to the [virality page]({{ site.baseurl }}{% link virality-simulation.md %}). 
Basic guidance:

  - $$\theta < 1.0$$: means there are less new cases each day compared to the previous day.
  - $$\theta > 1.0$$: means there are more new cases each day compared to the previous day.
  - $$\theta > 2.0$$: means we have a very serious problem!

Note: data is pulled from the [Johns Hopkins CSSE COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19),
and updated daily. They have a [geo dashboard with more information](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6).
