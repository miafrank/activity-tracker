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

<b-modal ref="addActivityModal"
         id="activity-modal"
         title="Add a new activity"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-date-group"
                label="Date:"
                label-for="form-date-input">
      <b-form-input id="form-date-input"
                    type="text"
                    v-model="addActivityForm.date"
                    required
                    placeholder="Enter Date">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-duration-group"
                  label="Duration:"
                  label-for="form-duration-input">
        <b-form-input id="form-duration-input"
                      type="text"
                      v-model="addActivityForm.duration"
                      required
                      placeholder="Enter Duration">
        </b-form-input>
      </b-form-group>
          <b-form-group id="form-name-group"
                  label="Name:"
                  label-for="form-name-input">
        <b-form-input id="form-name-input"
                      type="text"
                      v-model="addActivityForm.name"
                      required
                      placeholder="Enter author">
        </b-form-input>
      </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      activities: [],
      addActivityForm: {
        date: '',
        duration: '',
        name: '',
      },
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
    addActivity(json) {
      const path = 'http://localhost:5000/activities';
      axios.post(path, json)
        .then(() => {
          this.getActivities();
        });
    },
  },
  created() {
    this.getActivities();
  },
};
</script>
