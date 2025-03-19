<template>
  <div class="note-form">
    <h2>{{ isEdit ? 'Edit Note' : 'Create Note' }}</h2>

    <form @submit.prevent="saveNote">
      <div class="form-group">
        <label for="title">Title</label>
        <input id="title" v-model="note.title" required />
      </div>

      <div class="form-group">
        <label for="content">Content</label>
        <textarea id="content" v-model="note.content" required></textarea>
      </div>

      <button type="submit" class="btn-submit">{{ isEdit ? 'Update' : 'Create' }}</button>
    </form>

    <div  class="note-stats">
      <h3>Note Statistics</h3>
      <p>Word Count: {{ wordCount }}</p>
      <p>Characters: {{ charCount }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ["id"],
  data() {
    return {
      note: { title: "", content: "" },
      isEdit: false
    };
  },
  computed: {
    wordCount() {
      return this.note.content.split(/\s+/).filter(Boolean).length;
    },
    charCount() {
      return this.note.content.length;
    }
  },
  methods: {
    async fetchNote() {
      if (this.id) {
        this.isEdit = true;
        try {
          const response = await axios.get(`http://127.0.0.1:8000/notes/${this.id}`);
          this.note = response.data;
        } catch (error) {
          console.error("Error fetching note:", error);
        }
      }
    },
    async saveNote() {
      try {
        if (this.isEdit) {
          await axios.put(`http://127.0.0.1:8000/notes/${this.id}`, this.note);
        } else {
          await axios.post("http://127.0.0.1:8000/notes/", this.note);
        }
        this.$router.push("/");
      } catch (error) {
        console.error("Error saving note:", error);
      }
    }
  },
  mounted() {
    this.fetchNote();
  }
};
</script>

<style scoped>
.note-form {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  background: #222;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 255, 255, 0.2);
  color: #fff;
  font-family: 'Roboto', sans-serif;
}

h2 {
  color: #00ffcc;
  text-align: center;
  font-size: 28px;
  text-shadow: 0 0 5px #00ffcc, 0 0 10px #ff00ff;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 14px;
  color: #ddd;
  margin-bottom: 5px;
}

input, textarea {
  padding: 12px;
  background: #333;
  border: 1px solid #444;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

button {
  background: #00ffcc;
  color: #222;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

button:hover {
  background: #ff00ff;
  transform: scale(1.05);
}

.note-stats {
  margin-top: 40px;
  padding: 20px;
  background: #444;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  color: #ddd;
}

.note-stats p {
  font-size: 18px;
  margin: 10px 0;
}

.note-stats h3 {
  color: #00ffcc;
  margin-bottom: 15px;
  font-size: 22px;
  text-align: center;
}
</style>
