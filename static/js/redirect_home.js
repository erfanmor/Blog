//  <script src="{% static 'js/redirect_home.js' %}"></script>

function startCountdown(seconds) {
    let countdownElement = document.getElementById('countdown');
    let timer = setInterval(() => {
      countdownElement.innerText = seconds;
      seconds--;

      if (seconds < 0 ) {
        clearInterval(timer);
        window.location.href = "/"
      }
    }, 1000)
  }

  window.onload = () => {
    startCountdown(5);
  }