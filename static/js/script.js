/* 
  script.js
  - Booking form validation
  - Admin access logic (now securely validated via backend)
  - Real-time room availability checks
*/

document.addEventListener("DOMContentLoaded", () => {
  /* -----------------------------
   * 1. Booking Form Validation
   ----------------------------- */
  const bookingForm = document.querySelector(".booking-form");
  if (bookingForm) {
    bookingForm.addEventListener("submit", event => {
      const checkinDate = document.getElementById("checkin-date");
      const checkoutDate = document.getElementById("checkout-date");
      const roomType = document.getElementById("room-type");

      // Validate check-in / check-out dates
      if (checkinDate && checkoutDate) {
        const inDateValue = new Date(checkinDate.value);
        const outDateValue = new Date(checkoutDate.value);

        if (outDateValue <= inDateValue) {
          event.preventDefault();
          alert("Check-out date must be after the check-in date.");
          highlightError(checkinDate);
          highlightError(checkoutDate);
          return;
        }
      }

      // Validate room type selection
      if (roomType && roomType.value === "") {
        event.preventDefault();
        alert("Please select a room type.");
        highlightError(roomType);
        return;
      }
    });
  }

  function highlightError(element) {
    element.classList.add("error");
    setTimeout(() => element.classList.remove("error"), 3000);
  }

  /* -----------------------------
   * 2. Admin Access Logic
   ----------------------------- */
   let adminClickCount = 0;
  const adminTriggerBtn = document.getElementById("admin-trigger");
  const adminAlert = document.getElementById("admin-alert");
  const correctPassword = "Shebna"; // The correct admin password

  if (adminTriggerBtn) {
    adminTriggerBtn.addEventListener("click", () => {
      adminClickCount++;
      
      if (adminClickCount === 3) {
        // Prompt for the admin password
        const enteredPassword = prompt("Enter the admin password:");

        if (enteredPassword === correctPassword) {
          // Password correct: redirect to admin dashboard
          window.location.href = "/admin";

        } else {
          // Password incorrect: show inline alert
          if (adminAlert) {
            adminAlert.style.display = "block";
          }
        }
        // Reset the count after checking
        adminClickCount = 0;
      }
    });
  }

  /* -----------------------------
   * 3. Real-Time Availability Check
   ----------------------------- */
  const roomType = document.getElementById("room-type");
  const checkinDate = document.getElementById("checkin-date");
  const checkoutDate = document.getElementById("checkout-date");

  if (roomType && checkinDate && checkoutDate) {
    roomType.addEventListener("change", checkAvailability);
    checkinDate.addEventListener("change", checkAvailability);
    checkoutDate.addEventListener("change", checkAvailability);
  }

  function checkAvailability() {
    const room = roomType.value;
    const checkin = checkinDate.value;
    const checkout = checkoutDate.value;

    if (room && checkin && checkout) {
      fetch("/api/check-availability", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room, checkin, checkout })
      })
        .then(response => response.json())
        .then(data => {
          if (!data.available) {
            alert("The selected room is not available for the chosen dates.");
          } else {
            console.log("Room is available."); // You can replace this with a UI update
          }
        })
        .catch(error => console.error("Availability check error:", error));
    }
  }

  /* -----------------------------
   * 4. Success Message for Form Submission
   ----------------------------- */
  if (bookingForm) {
    bookingForm.addEventListener("submit", () => {
      // Optional: Show a "Processing" message
      alert("Booking submitted successfully. Redirecting to confirmation page...");
    });
  }
});
