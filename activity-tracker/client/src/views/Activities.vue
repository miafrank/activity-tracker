<template>
  <div>
    <ul id="activities">
      <li v-for="activity in activities" v-bind:key="activity.activity_id">
          {{ activity.activity_id }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      activities: [],
    };
  },
  methods: {
    getActivities() {
      const path = 'http://localhost:5000/activities';
      axios.get(path)
        .then((res) => {
          this.activities = res.data.activities;
        });
    },
  },
  created() {
    this.getActivities();
  },
};
</script>
