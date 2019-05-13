<template>
  <div>
<h1>Activities</h1>
<table class="table table-hover">
    <thead>
        <tr>
            <th scope="col">Date</th>
            <th scope="col">Duration</th>
            <th scope="col">Name</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="activity in activities" v-bind:key="activity.activity_id">
            <td>{{activity.activity_date}}</td>
            <td>{{activity.activity_duration}}</td>
            <td>{{activity.activity_name}}</td>
        </tr>
    </tbody>
</table>
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
