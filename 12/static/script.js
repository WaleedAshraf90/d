function createChart(ctx, type, data, labels, label) {
    new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: ["#ff6384", "#36a2eb", "#ffcd56", "#4bc0c0", "#9966ff"],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false, // لإلغاء تعبئة الخلفية
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,  // تعيين هذه الخاصية لتغيير الحجم تلقائيًا مع الشاشة
            plugins: {
                legend: {
                    position: 'top', // موقع الأسطورة
                    labels: {
                        font: {
                            size: 18, // حجم خط الأسطورة
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 16,
                            weight: 'bold',
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 16,
                            weight: 'bold',
                        },
                        beginAtZero: true, // يبدأ المحور من الصفر
                    }
                }
            }
        }
    });
}

function filterByMonth() {
    var month = document.getElementById("month").value;
    window.location.href = "/?month=" + month;
}

window.onload = function() {
    const donationsByProductData = {{ donations_by_product | tojson }};
    const donationsByMarketerData = {{ donations_by_marketer | tojson }};
    const donationsByPaymentData = {{ donations_by_payment | tojson }};
    const donationsByMonthData = {{ donations_by_month | tojson }};
    const peakHoursData = {{ peak_hours | tojson }};
    const donationCountsData = {{ donation_counts | tojson }};
    const targetVsActualData = {{ target_vs_actual | tojson }};
    
    const ctx1 = document.getElementById('donationsByProduct').getContext('2d');
    const ctx2 = document.getElementById('donationsByMarketer').getContext('2d');
    const ctx3 = document.getElementById('donationsByPayment').getContext('2d');
    const ctx4 = document.getElementById('donationsByMonth').getContext('2d');
    const ctx5 = document.getElementById('peakHours').getContext('2d');
    const ctx6 = document.getElementById('donationCounts').getContext('2d');
    const ctx7 = document.getElementById('targetVsActual').getContext('2d');
    
    ctx1.canvas.width = 1400;
    ctx1.canvas.height = 700;

    createChart(ctx1, 'bar', Object.values(donationsByProductData), Object.keys(donationsByProductData), "إجمالي التبرعات حسب مشروع ");
    createChart(ctx2, 'bar', Object.values(donationsByMarketerData), Object.keys(donationsByMarketerData), "إجمالي التبرعات حسب المسوق ");
    createChart(ctx3, 'pie', Object.values(donationsByPaymentData), Object.keys(donationsByPaymentData), "إجمالي التبرعات حسب طريقة الدفع ");
    createChart(ctx4, 'line', Object.values(donationsByMonthData), Object.keys(donationsByMonthData), "إجمالي التبرعات حسب الشهر ");
    createChart(ctx5, 'bar', peakHoursData, ["8-10", "10-12", "12-2", "2-4", "4-6"], "أوقات الذروة للتبرعات");
    createChart(ctx6, 'line', donationCountsData, Object.keys(donationCountsData), "عدد التبرعات");
    createChart(ctx7, 'bar', targetVsActualData, ["الهدف", "الفعلية"], "مقارنة الهدف مع التبرعات الفعلية");
}
