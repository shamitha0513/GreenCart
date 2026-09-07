/* Admin Dashboard Chart.js Integration (PDF Section 25) */

document.addEventListener("DOMContentLoaded", function () {
  const catChartEl = document.getElementById("categorySalesChart");
  const statusChartEl = document.getElementById("orderStatusChart");
  const topPlantsChartEl = document.getElementById("topPlantsChart");

  if (!catChartEl || !statusChartEl || !topPlantsChartEl) return;

  fetch("/admin/chart-data")
    .then((res) => res.json())
    .then((data) => {
      // 1. Category Sales Chart (Doughnut)
      new Chart(catChartEl, {
        type: "doughnut",
        data: {
          labels: data.categories,
          datasets: [
            {
              label: "Plants Sold",
              data: data.category_sales,
              backgroundColor: [
                "#1b4332", "#2d6a4f", "#52b788", "#74c69d", "#b7e4c7", "#d8f3dc",
                "#40916c", "#95d5b2", "#ffb703", "#fb8500", "#023e8a", "#0077b6"
              ],
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "right" },
          },
        },
      });

      // 2. Order Status Breakdown Chart (Bar)
      new Chart(statusChartEl, {
        type: "bar",
        data: {
          labels: data.statuses,
          datasets: [
            {
              label: "Number of Orders",
              data: data.status_counts,
              backgroundColor: [
                "#ffb703", "#2196f3", "#9c27b0", "#ff9800", "#00bcd4", "#4caf50", "#f44336"
              ],
              borderRadius: 8,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
          },
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 1 } },
          },
        },
      });

      // 3. Top Selling Plants Chart (Horizontal Bar)
      new Chart(topPlantsChartEl, {
        type: "bar",
        data: {
          labels: data.top_plants.length ? data.top_plants : ["Snake Plant", "Peace Lily", "Monstera"],
          datasets: [
            {
              label: "Units Sold",
              data: data.top_plant_qtys.length ? data.top_plant_qtys : [15, 12, 8],
              backgroundColor: "#2d6a4f",
              borderRadius: 8,
            },
          ],
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
          },
          scales: {
            x: { beginAtZero: true, ticks: { stepSize: 1 } },
          },
        },
      });
    })
    .catch((err) => console.error("Error loading admin chart data:", err));
});
