<!-- PersonalInformationView.vue -->

<template>
  <div v-if="!this.statingExperiment" class="personal-info-container">
    <h1>Personal Information</h1>
    <form @submit.prevent="submitForm">
      <!-- Demographics Questions -->
      <div class="form-group">
        <label for="age">Age:</label>
        <input type="number" id="age" v-model="participantData.age" required>
      </div>

      <div class="form-group">
        <label for="gender">Gender:</label>
        <select id="gender" v-model="participantData.gender" required>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">Programming Experience (years):</label>
        <select id="gender" v-model="participantData.programmingExperience" required>
          <option value="male">0 I do not now How to programm</option>
          <option value="female">Less than 3</option>
          <option value="other">More than 3</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">Are you familiar with "camelCase"</label>
        <select id="gender" v-model="participantData.familiarityCamelCase" required>
          <option value="male">Yes</option>
          <option value="female">No</option>
        </select>
      </div>
      <div class="form-group">
        <label for="gender">Are you familiar with "kebab-case"</label>
        <select id="gender" v-model="participantData.familiarityKebabCase" required>
          <option value="male">Yes</option>
          <option value="female">No</option>
        </select>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
  <div v-else class="experiment-container">
    <h1 class="experiment-title">Experiment</h1>
    <p class="experiment-description">
      This is the experiment page. The experiment will start when you press the start button. Once started, a timer will
      begin, and you will be presented with five different buttons, each containing a word. Your task is to click on the
      button that displays the same word as the one presented. The timer will measure the time it takes for you to
      complete the task.
    </p>

    <button v-if="!flagCountdown" class="start-button" @click="startExperiment">Start Experiment</button>
    <div v-if="flagCountdown" class="countdown">{{ countdown }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      participantData: {
        age: null,
        gender: null,
        programmingExperience: null,
        familiarityCamelCase: null,
        familiarityKebabCase: null,
      },
      statingExperiment: false,
      countdown: 3,
      flagCountdown: false,
    };
  },
  methods: {
    submitForm() {
      console.log('Participant Data:', this.participantData);
      this.statingExperiment = true;
    },
    startExperiment() {
      // Show countdown
      this.flagCountdown = true;
      this.showCountdown();

      // Start experiment route after countdown
      setTimeout(() => {
        this.$router.push('/experiment');
      }, (this.countdown + 1) * 1000);
    },
    showCountdown() {
      let count = 3; // Set the initial countdown value

      const countdownInterval = setInterval(() => {
        this.countdown--;

        if (this.countdown < 0) {
          clearInterval(countdownInterval);
          this.countdown = 0;
        }
      }, 1000);
    },
  },
};
</script>

<style scoped>
.personal-info-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #45a049;
}
.experiment-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.experiment-title {
  font-size: 60px;
  color: #333;
  margin-bottom: 10px;
  color: white;
}

.experiment-description {
  font-size: 25px;
  color: #555;
  margin-bottom: 20px;
  color : white;
}

.start-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

.start-button:hover {
  background-color: #45a049;
}
.countdown {
  font-size: 32px;
  font-weight: bold;
  color: green;
  text-align: center;
  margin-top: 20px;
}
</style>
