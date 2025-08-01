 document.addEventListener("DOMContentLoaded", function() {
                                            var ctx = document.getElementById('mixedpolarChart').getContext('2d');
                                            new Chart(ctx, {
                                                type: 'polarArea',
                                                data: {
                                                    labels: ['Red', 'Green', 'Yellow', 'Blue', 'Purple'],
                                                    datasets: [{
                                                        label: 'Dataset 1',
                                                        data: [11, 16, 7, 3, 14],
                                                        backgroundColor: [
                                                            'rgba(255, 99, 132, 0.5)',
                                                            'rgba(75, 192, 192, 0.5)',
                                                            'rgba(255, 205, 86, 0.5)',
                                                            'rgba(54, 162, 235, 0.5)',
                                                            'rgba(153, 102, 255, 0.5)'
                                                        ],
                                                        borderColor: [
                                                            'rgba(255, 99, 132, 1)',
                                                            'rgba(75, 192, 192, 1)',
                                                            'rgba(255, 205, 86, 1)',
                                                            'rgba(54, 162, 235, 1)',
                                                            'rgba(153, 102, 255, 1)'
                                                        ],
                                                        borderWidth: 1
                                                    }]
                                                },
                                                options: {
                                                    responsive: true,
                                                    legend: {
                                                        position: 'right'
                                                    },
                                                    title: {
                                                        display: false
                                                    }
                                                }
                                            });
                                        });