<template>
  <div>
    <!-- Button to start the second step -->
    <button v-if="!experimentsStarted" @click="startExperiments">Start the Second Step</button>

    <!-- Experiment content -->
    <div v-if="experimentsStarted">
      <h1>Experiment {{ currentExperiment }}</h1>

      <div v-if="counter < 5">
        <div class="box">{{ boxWords.options_camel_case.original_word }}</div>
        <div v-for="(word, index) in currentWords" :key="index" @click="boxClicked(word)" class="clickable-box" :style="{ 'float': index % 2 === 0 ? 'left' : 'none' }">
          {{ word }}
        </div>
        <div class="clear-float"></div>
      </div>

      <div v-else>
        <div class="box">{{ boxWords.options_kebab_case.original_word }}</div>
        <div v-for="(word, index) in currentWords" :key="index" @click="boxClicked(word)" class="clickable-box" :style="{ 'float': index % 2 === 0 ? 'left' : 'none' }">
          {{ word }}
        </div>
        <div class="clear-float"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      experimentsStarted: false,
      totalExperiments: 10,
      currentExperiment: 1,
      boxWords: {
        options_camel_case: { original_word: '', options_camel_case: [] },
        options_kebab_case: { original_word: '', options_kebab_case: [] }
      },
      currentCase: 'camelCase', // Initial case
      counter: 0,
      startTime: null,
    };
  },
  methods: {
    async fetchBoxWords() {
      try {
        this.startTime = performance.now();
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
    async startExperiments() {
      this.experimentsStarted = true;
      await this.fetchBoxWords();
    },
    boxClicked(word) {
      // Handle box click event
      const endTime = performance.now();
      const timeTaken = endTime - this.startTime;
      let isCorrect = "";

      if (this.currentCase === "camelCase") {
        isCorrect = word === this.boxWords.options_camel_case.correct_camel_case;
      } else {
        isCorrect = word === this.boxWords.options_kebab_case.correct_kebab_case;
      }

      this.currentCase = this.counter < 5 ? 'camelCase' : 'kebabCase';

      let answerData = {
        ex:2,
        age: this.participantData.age,
        gender: this.participantData.gender,
        programming_experience: this.participantData.programmingExperience,
        camel_case_familiarity: this.participantData.familiarityCamelCase,
        kebab_case_familiarity: this.participantData.familiarityKebabCase,
        type: this.currentCase === "camelCase" ? "camelCase" : "kebabCase",
        word: this.currentCase === "camelCase" ? this.boxWords.options_camel_case.original_word : this.boxWords.options_kebab_case.original_word,
        clickedWord: word,
        isCorrect,
        timeTaken
      };

      // Update currentCase after using it


      this.submitAnswerData(answerData);
      this.counter = this.counter + 1;
      this.currentExperiment = this.currentExperiment + 1;
      this.fetchBoxWords();
      console.log("currentCase", this.currentCase);
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
  created() {
    const participantData = this.$route.params.participantData;
    if (participantData) {
      this.participantData = JSON.parse(participantData);
    }
  }
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
  width: 48%; /* Set the width to 48% to fit two boxes in a row */
  box-sizing: border-box; /* Include padding and border in the box's total width */

}

.clickable-box:hover {
  transform: scale(1.1); /* Increase the size on hover */
}

</style>
