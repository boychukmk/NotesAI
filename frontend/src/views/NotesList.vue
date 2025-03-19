<template>
  <div class="notes-list">
    <h1 class="title">Notes</h1>
    <div v-if="notes.length === 0" class="no-notes">No notes found. Create it!</div>
    <div v-else class="notes-container">
      <div v-for="note in notes" :key="note.id" class="note-card">
        <h2>{{ note.title }}</h2>
        <p>{{ note.content.slice(0, 100) }}...</p>
        <router-link :to="`/note/${note.id}`" class="read-more">Read more</router-link>
        <div class="actions">
          <button @click="editNote(note.id)" class="action-btn edit-btn">Edit</button>
          <button @click="deleteNote(note.id)" class="action-btn delete-btn">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { notes: [] };
  },
  methods: {
    async fetchNotes() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/notes/");
        this.notes = response.data;
      } catch (error) {
        console.error("Error fetching notes:", error);
      }
    },
    editNote(id) {
      this.$router.push(`/edit/${id}`);
    },
    async deleteNote(id) {
      if (!confirm("Are you sure you want to delete this note?")) return;
      try {
        await axios.delete(`http://127.0.0.1:8000/notes/${id}`);
        this.fetchNotes();
      } catch (error) {
        console.error("Error deleting note:", error);
      }
    }
  },
  mounted() {
    this.fetchNotes();
  }
};
</script>

<style scoped>
.notes-list {
  text-align: center;
  padding: 30px;
  background: #1e1e1e;
  color: #fff;
  font-family: 'Orbitron', sans-serif;
}

.title {
  font-size: 36px;
  color: #00ffcc;
  text-transform: uppercase;
  letter-spacing: 3px;
  text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
  margin-bottom: 20px;
  padding-bottom: 20px;
}

.no-notes {
  font-size: 18px;
  color: #ff3333;
  text-shadow: 0 0 5px #ff3333;
}

.notes-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.note-card {
  background: #333;
  padding: 20px;
  width: 280px;
  border-radius: 12px;
  box-shadow: 0 0 15px #00ffcc;
  text-align: left;
  transition: transform 0.3s ease;
}

.note-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 25px #ff00ff;
}

h2 {
  font-size: 22px;
  color: #00ffcc;
}

p {
  font-size: 16px;
  color: #bbb;
  margin-bottom: 10px;
}

.read-more {
  display: inline-block;
  margin-top: 10px;
  color: #00ffcc;
  text-decoration: none;
  font-size: 16px;
  text-shadow: 0 0 5px #00ffcc;
}

.read-more:hover {
  color: #ff00ff;
}

.actions {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
}

.action-btn {
  padding: 8px 15px;
  font-size: 14px;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.edit-btn {
  background: #00ffcc;
}

.edit-btn:hover {
  background: #00cc99;
}

.delete-btn {
  background: #ff3333;
}

.delete-btn:hover {
  background: #cc0000;
}

button:focus {
  outline: none;
}
</style>
