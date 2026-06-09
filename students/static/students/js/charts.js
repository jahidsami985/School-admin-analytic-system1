function loadDashboardJson(url) {
  return fetch(url)
    .then((res) => {
      if (!res.ok) {
        throw new Error('Failed to load dashboard JSON: ' + res.status);
      }
      return res.json();
    });
}

function renderBarChart(canvasId, labels, values, label, color) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) {
    console.warn('Canvas not found:', canvasId);
    return;
  }

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        backgroundColor: color || 'rgba(54, 162, 235, 0.6)',
        borderColor: color ? color.replace('0.6', '1') : 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

function renderDoughnutChart(canvasId, labels, values, colors) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) {
    console.warn('Canvas not found:', canvasId);
    return;
  }

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}
