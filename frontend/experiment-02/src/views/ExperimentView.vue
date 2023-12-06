<template>
  <div>
    <h1>Experiment {{ this.currentExperiment }}</h1>

    <div v-if="counter < 5">

      <!-- Box above the clickable boxes -->
      <div class="box">{{ boxWords.options_camel_case.original_word }}</div>

      <!-- Four clickable boxes side by side -->
      <div v-for="(word, index) in currentWords" :key="index" @click="boxClicked(word)" class="clickable-box">
        {{ word }}
      </div>

    </div>
    <div v-else>
      <!-- Box above the clickable boxes -->
      <div class="box">{{ boxWords.options_kebab_case.original_word }}</div>

      <!-- Four clickable boxes side by side -->
      <div v-for="(word, index) in currentWords" :key="index" @click="boxClicked(word)" class="clickable-box">
        {{ word }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      totalExperiments: 10,
      currentExperiment: 1,
      boxWords: {
        options_camel_case: { original_word: '', options_camel_case: [] },
        options_kebab_case: { original_word: '', options_kebab_case: [] }
      },
      currentCase: 'camelCase', // Initial case
      counter: 0,
      answersData: {},
    };
  },
  methods: {
    async fetchBoxWords() {
      try {
        const response = await axios.get('http://localhost:5000/words');
        this.boxWords = response.data;
        console.log('Fetched words:', this.boxWords);

        if (this.counter === this.totalExperiments) {
          // Redirect to a new page after 10 experiments
          await this.submitAnswerData();
          await this.writeAnswerDataToCSV();
          this.$router.push('/end-view');
        }
      } catch (error) {
        console.error('Error fetching words:', error);
      }
    },
    boxClicked(word) {
      // Handle box click event
      const startTime = new Date().getTime(); // Get the current time in milliseconds
      const isCorrect = word === this.boxWords.original_word; // Check if the clicked word is correct
      const endTime = new Date().getTime(); // Get the current time in milliseconds
      const timeTaken = endTime - startTime; // Calculate the time taken to click the box

      // Save the answer data
      if (!this.answersData[this.currentExperiment]) {
        this.answersData[this.currentExperiment] = [];
      }
      this.answersData[this.currentExperiment].push({
        word: this.boxWords.original_word,
        clickedWord: word,
        isCorrect,
        timeTaken,
      });

      this.counter = this.counter + 1;
      this.currentExperiment = this.currentExperiment + 1;
      this.fetchBoxWords();
    },
    async submitAnswerData() {
      try {
        const response = await axios.post('http://localhost:5000/submit-answer', this.answersData);
        console.log('Submitted answer data:', response.data);
      } catch (error) {
        console.error('Error submitting answer data:', error);
      }
    },
    async writeAnswerDataToCSV() {
      try {
        const response = await axios.get('http://localhost:5000/write-to-csv');
        console.log('CSV file written successfully:', response.data);
      } catch (error) {
        console.error('Error writing to CSV:', error);
      }
    },
  },
  computed: {
    currentWords() {
      // Return words based on the current case and counter value
      return this.counter < 5
          ? this.currentCase === 'camelCase' ? this.boxWords.options_camel_case.options_camel_case : []
          : this.boxWords.options_kebab_case.options_kebab_case;
    },
  },
  mounted() {
    this.fetchBoxWords();
  },
};
</script>

<style scoped>
/* Add component styles here */
h1 {
  text-align: center;
  margin-top: 20%;
}

.box {
  margin-top: 20px;
  background-color: transparent;
  border: 1px solid #e0e0e0;
  padding: 10px;
}

.clickable-box {
  margin-top: 10px;
  margin-right: 10px;
  background-color: transparent;
  border: 1px solid #e0e0e0;
  padding: 10px;
  cursor: pointer;
  display: inline-block;
  transition: transform 0.3s; /* Smooth transition for the transform property */
}

.clickable-box:hover {
  transform: scale(1.1); /* Increase the size on hover */
}
</style>
