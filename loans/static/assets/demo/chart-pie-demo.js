document.addEventListener("DOMContentLoaded", function() {
                                            var ctx = document.getElementById("myPieChart").getContext('2d');
                                            new Chart(ctx, {
                                                type: 'pie',
                                                data: {
                                                    labels: ["Red", "Blue", "Yellow"],
                                                    datasets: [{
                                                        data: [300, 50, 100],
                                                        backgroundColor: [
                                                            "#dc3545",
                                                            "#007bff",
                                                            "#ffc107"
                                                        ],
                                                    }],
                                                },
                                                options: {
                                                    responsive: true,
                                                    plugins: {
                                                        legend: {
                                                            position: 'top',
                                                        },
                                                        title: {
                                                            display: false,
                                                        }
                                                    }
                                                }
                                            });
                                        });