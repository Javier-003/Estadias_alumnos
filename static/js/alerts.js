
document.addEventListener('DOMContentLoaded', function() {
          setTimeout(function() {
            var flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(function(message) {
              var alert = new bootstrap.Alert(message);
              alert.close();
            });
          }, 2000); // 5000 ms = 5 segundos
});


