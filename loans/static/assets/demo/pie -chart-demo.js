var options = {
  chart: {
    height: 350,
    type: "pie",
  },
  dataLabels: {
    enabled: false
  },
  series: [44, 55, 13, 33]
}
var chart = new ApexCharts(
  document.querySelector("#apexcharts-pie"),
  options
);
chart.render();