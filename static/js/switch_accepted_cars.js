(() => {
      const btn = document.getElementById('toggle-pending');
      const all = document.getElementById('all-list');
      const pending = document.getElementById('pending-list');
      let showingPending = false;
      btn.addEventListener('click', () => {
        showingPending = !showingPending;
        all.hidden = showingPending;
        pending.hidden = !showingPending;
        btn.textContent = showingPending ? 'Покажи всички' : 'Покажи най-чакащите';
        btn.classList.toggle('active', showingPending);
      });
    })();