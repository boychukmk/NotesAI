<template>
  <div class="analytics-container">
    <h1 class="title">Notes Analytics</h1>
    <div v-if="analytics" class="stats">
      <div class="stat">
        <h3>Total Word Count</h3>
        <p>{{ analytics.total_word_count }}</p>
      </div>
      <div class="stat">
        <h3>Average Note Length</h3>
        <p>{{ analytics.average_note_length }} words</p>
      </div>
      <div class="stat">
        <h3>Most Common Words</h3>
        <ul>
          <li v-for="(word, index) in analytics.most_common_words" :key="index">
            {{ word }}
          </li>
        </ul>
      </div>
      <div class="stat">
        <h3>Top Notes</h3>
        <h4>Longest Notes</h4>
        <ul>
          <li v-for="(note, index) in analytics.top_notes.longest" :key="index">
            Note ID: {{ note.id }} - Length: {{ note.length }} words
          </li>
        </ul>
        <h4>Shortest Notes</h4>
        <ul>
          <li v-for="(note, index) in analytics.top_notes.shortest" :key="index">
            Note ID: {{ note.id }} - Length: {{ note.length }} words
          </li>
        </ul>
      </div>
      <div class="stat">
        <h3>Total Character Count</h3>
        <p>{{ analytics.total_character_count }}</p>
      </div>
      <div class="stat">
        <h3>Median Note Length</h3>
        <p>{{ analytics.median_note_length }} words</p>
      </div>
      <div class="stat">
        <h3>Common Bigrams</h3>
        <ul>
          <li v-for="(bigram, index) in analytics.common_bigrams" :key="index">
            {{ bigram }}
          </li>
        </ul>
      </div>
      <div class="stat">
        <h3>Common Trigrams</h3>
        <ul>
          <li v-for="(trigram, index) in analytics.common_trigrams" :key="index">
            {{ trigram }}
          </li>
        </ul>
      </div>
    </div>
    <div v-else class="loading">
      <p>Loading analytics...</p>
    </div>
    <div v-if="error" class="error">
      <p>Analytics currently unavailable. Please create a note.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      analytics: null,
      error: null,
    };
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/analytics/');
      this.analytics = response.data;
    } catch (error) {
      this.error = error.message;
    }
  }
};
</script>

<style scoped>
.analytics-container {
  background: linear-gradient(135deg, #00f, #ff00ff);
  padding: 30px;
  border-radius: 15px;
  color: #fff;
  text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
  font-family: 'Orbitron', sans-serif;
  max-width: 1200px;
  margin: 30px auto;
}

.title {
  font-size: 40px;
  text-align: center;
  color: #00ffcc;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.stat {
  background: rgba(0, 0, 0, 0.6);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 20px #ff00ff;
}

h3 {
  font-size: 24px;
  color: #00ffcc;
  margin-bottom: 10px;
}

p, ul {
  font-size: 16px;
  color: #fff;
}

ul {
  list-style-type: none;
  padding: 0;
}

.loading, .error {
  text-align: center;
  font-size: 18px;
  color: #ff3333;
}

.error {
  color: #ff0033;
}

.loading {
  color: #ffcc00;
}
</style>
