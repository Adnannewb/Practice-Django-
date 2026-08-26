// D:\just_physiosphere\static\js\appointment.js

function initLiveSerial(apiUrl) {
    const container = document.getElementById('live-serial-container');
    if (!container) return;

    // Helper: format diff in ms as:
    //   "3 days 5 hours 45 minutes"
    //   "5 hours 45 minutes"
    //   "45 minutes"
    //   "Now"
    function formatTimeDiff(diffMs) {
        if (diffMs <= 0) {
            return 'Now';
        }

        const totalMinutes = Math.floor(diffMs / 60000);
        const days = Math.floor(totalMinutes / (24 * 60));
        const hours = Math.floor((totalMinutes % (24 * 60)) / 60);
        const minutes = totalMinutes % 60;

        const parts = [];

        if (days > 0) {
            parts.push(days + ' day' + (days !== 1 ? 's' : ''));
        }
        if (hours > 0) {
            parts.push(hours + ' hour' + (hours !== 1 ? 's' : ''));
        }

        // If there are no days/hours, always show minutes.
        // If there are days/hours, show minutes only when > 0.
        if (minutes > 0 || (days === 0 && hours === 0)) {
            parts.push(minutes + ' minute' + (minutes !== 1 ? 's' : ''));
        }

        return parts.join(' ');
    }

    function renderRows(appointments) {
        container.innerHTML = '';

        appointments.forEach(appt => {
            const row = document.createElement('div');
            row.className = 'live-serial-row';

            const label = document.createElement('div');
            label.textContent = `${appt.patient} with ${appt.therapist}`;

            const countdown = document.createElement('div');
            countdown.className = 'countdown';

            const startEl = document.createElement('div');
            const startDate = new Date(appt.start_time);
            startEl.textContent = startDate.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            });

            row.appendChild(label);
            row.appendChild(countdown);
            row.appendChild(startEl);
            container.appendChild(row);

            function updateCountdown() {
                const now = new Date().getTime();
                const diff = startDate.getTime() - now;
                countdown.textContent = formatTimeDiff(diff);
            }

            updateCountdown();
            // minutes-based view: update every 30 seconds
            setInterval(updateCountdown, 30000);
        });

        if (!appointments || appointments.length === 0) {
            container.innerHTML = '<p>No upcoming sessions.</p>';
        }
    }

    function fetchSerial() {
        fetch(apiUrl)
            .then(r => r.json())
            .then(data => renderRows(data.appointments || []))
            .catch(err => console.error('Live serial error', err));
    }

    fetchSerial();
    setInterval(fetchSerial, 30000);
}