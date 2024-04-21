document.addEventListener('DOMContentLoaded', function() {
  const observeButtons = document.querySelectorAll('.observe');
  const popup = document.getElementById('popup');
  const closeButton = document.querySelector('.close');
  const form = document.getElementById('observation-form');
  const targetLabel = document.getElementById('target-label');
  const targetSelect = document.getElementById('target');

  // Add event listener to each observe button
  observeButtons.forEach(button => {
      button.addEventListener('click', () => {
          // Check which object is being observed
          if (button.id === 'Moon') {
              // Update label and select options for Moon
              targetLabel.textContent = 'Enter Details for Moon';
              targetSelect.innerHTML = '<option value="1">1 sec</option><option value="2">2 sec</option><option value="3">3 sec</option>';
          } else if (button.id === 'Sun') {
              // Update label and select options for Sun
              targetLabel.textContent = 'Enter Details for Sun';
              targetSelect.innerHTML = '<option value="5">5 sec</option><option value="10">10 sec</option><option value="15">15 sec</option>';
          }
          popup.style.display = 'block'; // Show the popup
      });
  });

  // Add event listener to close button
  closeButton.addEventListener('click', () => {
      popup.style.display = 'none'; // Hide the popup when close button is clicked
  });

  // Add event listener to form submission
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    // Handle form submission here, e.g., send an AJAX request
    console.log('Form submitted:', e.target);
    popup.style.display = 'none'; // Hide the popup after form submission

    // Display a browser popup with a message
    window.alert('Images will be mailed shortly.');
});
});
