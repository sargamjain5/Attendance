document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#loginForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Stop form from refreshing the page

    const enrolment_no = document.getElementById('enroll').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!enrolment_no || !password) {
      alert('Please enter both enrollment no and password.');
      return;
    }

    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enrolment_no, password })
      });

      const data = await res.json();

      if (res.ok) {
        // ✅ Login success — redirect
        window.location.href = '/attendance';
      } else {
        // ❌ Login failed — show message, inputs remain
        alert(data.message || 'Login failed');
      }

    } catch (error) {
      alert('❌ Server error. Please try again.');
      console.error(error);
    }
  });
});
