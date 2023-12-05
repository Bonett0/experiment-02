<template>
  <div>
    <h1>Experiment {{ this.currentExperiment }}</h1>

    <!-- Box above the clickable boxes -->
    <div class="box">{{ boxWords[0] }}</div>

    <!-- Four clickable boxes side by side -->
    <div v-for="(word, index) in boxWords.slice(1)" :key="index" @click="boxClicked(index)" class="clickable-box">
      {{ word }}
    </div>
  </div>
</template>

<script>
export default {
  // Add component logic here
  data() {
    return {
      totalExperiments: 10,
      currentExperiment: 1,
      boxWords: ['Box 1', 'Box 2', 'Box 3', 'Box 4', 'Box 5'],
    };
  },
  methods: {
    boxClicked(index) {
      // Handle box click event
      console.log('Box clicked:', index);
    },
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
