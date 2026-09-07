/* Live AJAX Status Polling for GreenCart (PDF Section 21) */

function startOrderLivePolling(orderId) {
  if (!orderId) return;

  const statuses = ['Placed', 'Confirmed', 'Assigned', 'Accepted', 'Out for Delivery', 'Delivered'];
  
  function pollStatus() {
    fetch(`/api/order-status/${orderId}`)
      .then(response => response.json())
      .then(data => {
        if (!data || data.error) return;

        const currentStatus = data.order_status;
        const currentIdx = statuses.indexOf(currentStatus);

        // 1. Update Progress Bar
        const progressBar = document.getElementById('progressBar');
        if (progressBar && currentIdx !== -1) {
          const percentage = (currentIdx / (statuses.length - 1)) * 100;
          progressBar.style.width = percentage + '%';
        }

        // 2. Update Stepper Circles
        statuses.forEach((st, idx) => {
          const stepElement = document.getElementById(`step-${st.replace(/\s+/g, '-')}`);
          if (stepElement) {
            const circle = stepElement.querySelector('.step-circle');
            if (idx <= currentIdx) {
              stepElement.classList.add('completed');
              if (circle) {
                circle.className = 'step-circle mx-auto mb-2 rounded-circle d-flex align-items-center justify-content-center fw-bold bg-success text-white';
                circle.innerHTML = '<i class="bi bi-check-lg"></i>';
              }
            } else {
              stepElement.classList.remove('completed');
              if (circle) {
                circle.className = 'step-circle mx-auto mb-2 rounded-circle d-flex align-items-center justify-content-center fw-bold bg-light text-muted border';
                circle.innerText = idx + 1;
              }
            }
          }
        });

        // 3. Update Title & Timestamp
        const currentStatusTitle = document.getElementById('currentStatusTitle');
        const lastUpdatedTime = document.getElementById('lastUpdatedTime');
        
        if (currentStatusTitle) {
          let statusText = currentStatus;
          if (currentStatus === 'Placed') statusText = 'Order Placed Successfully';
          else if (currentStatus === 'Confirmed') statusText = 'Order Confirmed by Admin';
          else if (currentStatus === 'Assigned') statusText = 'Delivery Partner Assigned';
          else if (currentStatus === 'Accepted') statusText = 'Order Accepted by Delivery Partner';
          else if (currentStatus === 'Out for Delivery') statusText = 'Out for Delivery';
          else if (currentStatus === 'Delivered') statusText = 'Delivered Successfully! 🌿';
          
          currentStatusTitle.innerText = statusText;
        }

        if (lastUpdatedTime && data.updated_at) {
          lastUpdatedTime.innerText = data.updated_at;
        }

        // 4. Update Delivery Partner Box
        const dpName = document.getElementById('dpName');
        const dpPhone = document.getElementById('dpPhone');
        if (dpName && data.delivery_partner && data.delivery_partner !== "Not Assigned") {
          dpName.innerText = data.delivery_partner;
          if (dpPhone) dpPhone.innerText = data.delivery_partner_phone || '';
        }
      })
      .catch(err => console.error("Polling error:", err));
  }

  // Initial poll and set 3-second interval
  pollStatus();
  setInterval(pollStatus, 3000);
}
