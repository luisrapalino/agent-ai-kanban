<template>
  <v-app>
    <v-main class="bg-grey-lighten-3 d-flex justify-center align-center fill-height">
      <v-container class="ma-0 pa-0" style="max-width: 600px">

        <v-card elevation="3">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>🧠 Asistente IA - Kanban</v-toolbar-title>
          </v-toolbar>

          <v-card-text class="chat-window" ref="chatContainer">
            <div v-if="mensajes.length === 0 && !cargando"
              class="d-flex flex-column align-center justify-center text-center fill-height">
              <v-icon size="64" color="grey">mdi-chat-outline</v-icon>
              <p class="mt-2 text-grey-darken-1">Inicia una conversación con tu asistente IA</p>
            </div>

            <div v-else>
              <div v-for="(msg, index) in mensajes" :key="index" class="mb-3">
                <div :class="['message-bubble', msg.rol]">
                  <template v-if="msg.rol === 'ai'">
                    <v-avatar class="mr-2" size="32">
                      <v-icon color="deep-purple">mdi-robot</v-icon>
                    </v-avatar>
                    <div class="message-content ai-msg">{{ msg.texto }}</div>
                  </template>

                  <template v-else>
                    <div class="message-content user-msg">{{ msg.texto }}</div>
                    <v-avatar class="ml-2" size="32">
                      <v-icon color="blue-darken-2">mdi-account</v-icon>
                    </v-avatar>
                  </template>
                </div>
              </div>

              <!-- Loader del asistente -->
              <div v-if="cargando" class="message-bubble ai mb-3">
                <v-avatar class="mr-2" size="32">
                  <v-icon color="deep-purple">mdi-robot</v-icon>
                </v-avatar>
                <v-progress-circular indeterminate color="primary" size="24" />
              </div>
            </div>

          </v-card-text>



          <v-slide-y-transition>
            <v-card-text v-show="mostrarSugerencias" class="pa-3 pt-0">
              <div class="d-flex flex-wrap gap-2">
                <v-chip v-for="(s, i) in sugerencias" :key="i" color="blue lighten-4" class="ma-1"
                  :class="{ 'chip-usada': usadas.includes(s) }" @click="usarSugerencia(s)" prepend-icon="mdi-lightbulb"
                  variant="outlined">
                  {{ s }}
                </v-chip>
              </div>
            </v-card-text>
          </v-slide-y-transition>

          <v-divider />

          <v-card-actions>
            <v-text-field v-model="entrada" label="Escribe tu mensaje" hide-details dense clearable class="flex-grow-1"
              @keydown.enter="enviarMensaje" :disabled="cargando" />

            <v-btn icon color="warning" @click="mostrarSugerencias = !mostrarSugerencias">
              <v-icon>{{ mostrarSugerencias ? 'mdi-close' : 'mdi-lightbulb-outline' }}</v-icon>
            </v-btn>

            <v-btn color="primary" @click="enviarMensaje" :disabled="cargando">
              <v-icon left>mdi-send</v-icon>
              Enviar
            </v-btn>

          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      entrada: '',
      mensajes: [],
      mostrarSugerencias: true,
      usadas: [],
      cargando: false,
      sugerencias: [
        "¿Cuántos tableros hay, y como se llaman?",
        "¿Qué tareas están pendientes, y el nombre del tablero al que pertenecen?",
        "¿Cuantos checklists se han creado, y completado?",
        "¿Qué tablero tiene más columnas, y como se llama?",
        "Dame un resumen de los tableros y dime que puedo hacer para mejorar",
      ],

    };
  },
  methods: {
    usarSugerencia(texto) {
      if (!this.usadas.includes(texto)) {
        this.usadas.push(texto);
        this.entrada = texto;
        this.enviarMensaje();
      }
    }
    ,
    async enviarMensaje() {
      const mensaje = this.entrada.trim();
      if (!mensaje || this.cargando) return;

      this.mensajes.push({ rol: 'user', texto: mensaje });
      this.entrada = '';
      this.mostrarSugerencias = false;
      this.scrollToBottom();


      this.cargando = true;
      try {
        const res = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mensaje }),
        });

        const data = await res.json();
        this.mensajes.push({ rol: 'ai', texto: data.respuesta });
      } catch (error) {
        this.mensajes.push({ rol: 'ai', texto: '❌ Error al contactar con el agente.' });
      } finally {
        this.cargando = false;
        this.scrollToBottom();
      }
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        if (container) container.scrollTop = container.scrollHeight;
      });
    },
  },
};
</script>

<style scoped>
.chat-window {
  height: 60vh;
  overflow-y: auto;
  background-color: #f5f5f5;
  padding: 16px;
}

.message-bubble {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
  max-width: 100%;
}

.message-bubble.ai {
  justify-content: flex-start;
}

.message-bubble.user {
  justify-content: flex-end;
}

.message-content {
  border-radius: 16px;
  padding: 10px 14px;
  max-width: 70%;
  font-size: 14px;
  line-height: 1.4;
  white-space: pre-wrap;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.ai-msg {
  background-color: #ede7f6;
  margin-left: 8px;
}

.user-msg {
  background-color: #d0eaff;
  margin-right: 8px;
}

.chip-usada {
  opacity: 0.5;
  pointer-events: none;
}
</style>
