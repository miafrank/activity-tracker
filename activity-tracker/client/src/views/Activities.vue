<template>
  <div class="container">
<h1>Activities</h1>
<alert :message=message v-if="showMessage"></alert>
<button type="button" class="btn btn-success btn-sm" v-b-modal.activity-modal>Add Activity</button>
<br><br>
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
            <td>
                <div class="btn-group" role="group">
                <b-button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.edit-activity-modal
                    @click="editActivity(activity)">
                Update</b-button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
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
                    v-model="addActivityForm.activity_date"
                    required
                    placeholder="Enter Date">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-duration-group"
                  label="Duration:"
                  label-for="form-duration-input">
        <b-form-input id="form-duration-input"
                      type="text"
                      v-model="addActivityForm.activity_duration"
                      required
                      placeholder="Enter Duration">
        </b-form-input>
      </b-form-group>
          <b-form-group id="form-name-group"
                  label="Name:"
                  label-for="form-name-input">
        <b-form-input id="form-name-input"
                      type="text"
                      v-model="addActivityForm.activity_name"
                      required
                      placeholder="Enter author">
        </b-form-input>
      </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>

<b-modal ref="editActivityModal"
         id="edit-activity-modal"
         title="Edit an activity"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-date-edit-group"
                label="Date:"
                label-for="form-date-edit-input">
      <b-form-input id="form-date-edit-input"
                    type="text"
                    v-model="editActivityForm.activity_date"
                    placeholder="Edit Date">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-duration-edit-group"
                  label="Duration:"
                  label-for="form-duration-edit-input">
        <b-form-input id="form-duration-edit-input"
                      type="text"
                      v-model="editActivityForm.activity_duration"
                      placeholder="Edit Duration">
        </b-form-input>
      </b-form-group>
          <b-form-group id="form-name-edit-group"
                  label="Name:"
                  label-for="form-name-edit-input">
        <b-form-input id="form-name-edit-input"
                      type="text"
                      v-model="editActivityForm.activity_name"
                      placeholder="Edit author">
        </b-form-input>
      </b-form-group>
    <b-button type="submit" class="btn btn-warning btn-sm" v-b-modal.edit-activity-modal>
        Update</b-button>
    <b-button type="reset" class="btn btn-warning btn-sm" variant="danger">Cancel</b-button>
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
        activity_date: '',
        activity_duration: '',
        activity_name: '',
      },
      editActivityForm: {
        activity_id: '',
        activity_date: '',
        activity_duration: '',
        activity_name: '',
      },
      message: '',
      showMessage: false,
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
    updateActivity(activityId) {
      const path = `http://localhost:5000/activities/${activityId}`;
      axios.put(path, activityId)
        .then(() => {
          this.getActivities();
          this.message = 'Activity updated!';
        });
    },
    initForm() {
      this.addActivityForm.activity_date = '';
      this.addActivityForm.activity_duration = '';
      this.addActivityForm.activity_name = '';
      this.editActivityForm.activity_id = '';
      this.editActivityForm.activity_date = '';
      this.editActivityForm.activity_duration = '';
      this.editActivityForm.activity_name = '';
    },
    onSubmit(event) {
      event.preventDefault();
      this.$refs.addActivityModal.hide();
      const json = {
        activity_date: this.addActivityForm.activity_date,
        activity_duration: this.addActivityForm.activity_duration,
        activity_name: this.addActivityForm.activity_name,
      };
      this.addActivity(json);
      this.initForm();
    },
    onReset(event) {
      event.preventDefault();
      this.$refs.addActivityModal.hide();
      this.initForm();
    },
    onResetUpdate(event) {
      event.preventDefault();
      this.$refs.editActivityModal.hide();
      this.initForm();
      this.getActivities();
    },
    editActivity(activity) {
      console.log('activity object');
      console.log(activity);
      this.editActivityForm = activity;
    },
    onSubmitUpdate(event) {
      event.preventDefault();
      this.$refs.editActivityModal.hide();
      const json = {
        activity_date: this.editActivityForm.activity_date,
        activity_duration: this.editActivityForm.activity_duration,
        activity_name: this.editActivityForm.activity_name,
      };
      console.log('onsubmitupdate');
      console.log(json);
      this.updateActivity(this.editActivity.activity_id);
    },
  },
  created() {
    this.getActivities();
  },
};
</script>
