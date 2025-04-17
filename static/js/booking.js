function disableBookedDates(bookedRanges) {
    const startInput = document.getElementById('start_date');
    const endInput = document.getElementById('end_date');
  
    const disabledDates = new Set();
    bookedRanges.forEach(([startStr, endStr]) => {
      let current = new Date(startStr);
      const end = new Date(endStr);
      while (current <= end) {
        disabledDates.add(current.toISOString().split('T')[0]);
        current.setDate(current.getDate() + 1);
      }
    });
  
    function isDateDisabled(dateStr) {
      return disabledDates.has(dateStr);
    }
  
    function validateDates() {
      if (isDateDisabled(startInput.value)) {
        alert("Check-in date is not available.");
        startInput.value = '';
      }
      if (isDateDisabled(endInput.value)) {
        alert("Check-out date is not available.");
        endInput.value = '';
      }
    }
  
    startInput.addEventListener('change', validateDates);
    endInput.addEventListener('change', validateDates);
  }
  