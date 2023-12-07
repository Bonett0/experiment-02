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
          this.$router.push('/end-view');
        }
      } catch (error) {
        console.error('Error fetching words:', error);
      }
    },
    boxClicked(word) {
      // Handle box click event
      const startTime = new Date().getTime(); // Get the current time in milliseconds
      let isCorrect = "";
      if (this.currentCase === "camelCase") {
        isCorrect = word === this.boxWords.options_camel_case.original_word
      } else {
        isCorrect = word === this.boxWords.options_kebab_case.original_word
      }
      // const isCorrect = word === this.boxWords.original_word; // Check if the clicked word is correct
      const endTime = new Date().getTime(); // Get the current time in milliseconds
      const timeTaken = endTime - startTime; // Calculate the time taken to click the box

      // // Save the answer data
      // if (!this.answersData[this.currentExperiment]) {
      //   this.answersData[this.currentExperiment] = [];
      // }
      // this.answersData[this.currentExperiment].push({
      //   word: this.boxWords.original_word,
      //   clickedWord: word,
      //   isCorrect,
      //   timeTaken,
      // });
      let answerData = {
        word: this.currentCase === "camelCase" ? this.boxWords.options_camel_case.original_word : this.boxWords.options_kebab_case.original_word,
        clickedWord: word,
        isCorrect,
        timeTaken
      }

      this.submitAnswerData(answerData);
      this.counter = this.counter + 1;
      this.currentExperiment = this.currentExperiment + 1;
      this.fetchBoxWords();
    },
    async submitAnswerData(answerData) {
      try {
        // Make a POST request to the combined endpoint
        const response = await axios.post('http://localhost:5000/submit-and-export', answerData);
        console.log('Submitted answer data:', response.data);

        // Check if it's time to export to CSV (e.g., after 10 experiments)
        if (this.counter === this.totalExperiments) {
          // Make a GET request to trigger CSV export
          const exportResponse = await axios.get('http://localhost:5000/submit-and-export');
          console.log('Exported answer data to CSV:', exportResponse.data);

          // Optionally, you can redirect to a new page after exporting to CSV
          this.$router.push('/end-view');
        }
      } catch (error) {
        console.error('Error submitting answer data:', error);
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
