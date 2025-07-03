document.addEventListener('DOMContentLoaded', () => {
  // Handle student login form
  const loginForm = document.querySelector('#loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

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
          window.location.href = '/attendance';
        } else {
          alert(data.message || 'Login failed');
        }
      } catch (error) {
        alert('❌ Server error. Please try again.');
        console.error(error);
      }
    });
  }

  // Handle admin login form
  const adminForm = document.querySelector('#adminLoginForm');
  if (adminForm) {
    adminForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value.trim();

      if (!username || !password) {
        alert('Please enter both admin ID and password.');
        return;
      }

      try {
        const res = await fetch('/api/admin-login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
          // ✅ Admin login success — redirect to analysis page with today's date
          const today = new Date();
          const day = String(today.getDate()).padStart(2, '0');
          const monthShort = today.toLocaleString('en-US', { month: 'short' });
          const formattedDate = `${day} ${monthShort}`;

          window.location.href = `/analysis/${formattedDate}`;
        } else {
          alert(data.message || 'Admin login failed');
        }
      } catch (error) {
        alert('❌ Server error. Please try again.');
        console.error(error);
      }
    });
  }
});
