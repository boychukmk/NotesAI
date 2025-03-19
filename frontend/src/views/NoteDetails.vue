<template>
  <div class="note-details">
    <h1>{{ note.title }}</h1>
    <p>{{ note.content }}</p>

    <div class="buttons">
      <button @click="viewHistory">View History</button>
      <button @click="summarizeNote">Summarize Note</button>
      <button @click="goBack">Back</button>
    </div>

    <div v-if="history.length > 0" class="note-history">
      <h3>History:</h3>
      <ul>
        <li v-for="entry in history" :key="entry.id">
          <p>{{ entry.content }}</p>
          <small>{{ entry.created_at }}</small>
        </li>
      </ul>
    </div>
    <div v-if="historyError" class="error-message">
      <p>History not available for this note.</p>
    </div>

    <div v-if="aiSummary" class="ai-summary">
      <h3>AI-summary:</h3>
      <p>{{ aiSummary }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ["id"],
  data() {
    return {
      note: {},
      aiSummary: "",
      history: [],
      historyError: false
    };
  },
  methods: {
    async fetchNote() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/notes/${this.id}`);
        this.note = response.data;  // Зберігаємо інформацію про нотатку
      } catch (error) {
        console.error("Error fetching note:", error);
      }
    },
    async viewHistory() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/history/${this.id}`);
        this.history = response.data;
        this.historyError = false;
      } catch (error) {
        if (error.response && error.response.status === 404) {
          this.historyError = true;
        } else {
          console.error("Error fetching history:", error);
        }
      }
    },
    async summarizeNote() {
      try {
        const response = await axios.post(`http://127.0.0.1:8000/summarizer/${this.id}`);
        this.aiSummary = response.data.summary;
      } catch (error) {
        console.error("Error summarizing note:", error);
      }
    },
    goBack() {
      this.$router.push("/");
    }
  },
  mounted() {
    this.fetchNote();
  }
};
</script>

<style scoped>
.note-details {
  text-align: center;
  padding: 40px;
  background: #222;
  color: #fff;
  font-family: 'Orbitron', sans-serif;
  box-shadow: 0 0 15px #00ffcc;
  border-radius: 8px;
}

h1 {
  font-size: 36px;
  color: #00ffcc;
  text-transform: uppercase;
  letter-spacing: 3px;
  text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
}

p {
  font-size: 18px;
  color: #bbb;
  margin: 20px 0;
}

.buttons {
  margin-top: 30px;
}

button {
  margin: 10px;
  padding: 12px 24px;
  background-color: #00ffcc;
  color: #222;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #ff00ff;
  transform: scale(1.05);
}

button:focus {
  outline: none;
}

.note-history, .ai-summary {
  margin-top: 40px;
  padding: 20px;
  background: rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
}

.note-history ul {
  list-style-type: none;
  padding: 0;
}

.note-history li {
  margin-bottom: 20px;
}

small {
  display: block;
  margin-top: 5px;
  font-size: 0.9em;
  color: #888;
}

.error-message {
  color: #ff3333;
  font-weight: bold;
  margin-top: 20px;
}

.ai-summary p {
  font-size: 18px;
  color: #fff;
}
</style>
