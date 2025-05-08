// static/js/chat.js
(function () {
    var Message; //Crear mensaje en la plantilla
    Message = function (arg) {
        this.text = arg.text;
        // User (right) Server (left)
        this.message_side = arg.message_side;
        this.draw = () => {
            // Clonar bloque de la plantilla y configurar contenido
            var $message;
            // Clona la plantilla del mensaje
            $message = $($('.message_template').clone().html());
            // Alinea el mensaje a la izquierda o derecha según su tipo
            $message.addClass(this.message_side).find('.text').html(this.text);
            $('.messages').append($message);
            // Muestra el mensaje con una transición de aparición
            setTimeout(function () {
                $message.addClass('appeared');
            }, 0);
        };
    };

    // Enviar mensaje del usuario
    function sendUserMessage(text) {
        var userMessage = new Message({
            text: text,
            message_side: 'right'
        });
        userMessage.draw();
    }
    // Mostrar la respuesta del servidor
    function sendServerMessage(text) {
        var serverMessage = new Message({
            text: text,
            message_side: 'left'
            });
        serverMessage.draw();
    }

    // Activar cuando usuario envia mensaje
    function triggerSend() {
        var $input = $('.message_input'),
            text = $input.val();
        if (text.trim() === '') {
            return;
        }
        // Clean
        $input.val('');
        // Mostrar msg
        sendUserMessage(text);

        // Call server con AJAX
        $.ajax({
            type: "POST",
            url: "/api/rpc_call", //endpoint flask
            data: { mensaje: text },
            success: function (data) {
                // recibir respuesta
                sendServerMessage(data.response);

                var $messages = $(".messages");
                $messages.animate({ scrollTop: $messages.prop('scrollHeight')}, 300);
            },
            error: function () {
                sendServerMessage("Error al obtener respuesta del servidor");
            }
        });
        // Scroll para ver nuevo mensaje
        var $messages = $(".messages");
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
    }

    // jQuery
    $(function () {
        $('.send_message').click(function (e) {
            triggerSend();
        });
        // Detectar Enter
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                triggerSend();
            }
        });
    });
}.call(this));

/*
    $(function () {
      var getMessageText, message_side, sendMessage;
      message_side = 'right';
      getMessageText = function () {
        var $message_input;
        $message_input = $('.message_input');
        return $message_input.val();
      };
      sendMessage = function (text) {
        var $messages, message;
        if (text.trim() === '') {
          return;
        }
        $('.message_input').val('');
        $messages = $('.messages');
        // Alterna el mensaje entre lado izquierdo y derecho
        message_side = message_side === 'left' ? 'right' : 'left';
        message = new Message({
          text: text,
          message_side: message_side
        });
        message.draw();
        return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
      };
      $('.send_message').click(function (e) {
        return sendMessage(getMessageText());
      });
      $('.message_input').keyup(function (e) {
        if (e.which === 13) {
          return sendMessage(getMessageText());
        }
      });
      // Mensajes de ejemplo
      /*
      sendMessage('Hello Philip! :)');
      setTimeout(function () {
        return sendMessage('Hi Sandy! How are you?');
      }, 1000);
      return setTimeout(function () {
        return sendMessage("I'm fine, thank you!");
      }, 2000);
    });*/
  