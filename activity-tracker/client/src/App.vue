<template>
  <div id="app">
    <notifications group="activity-added" />
    <router-view/>
  </div>
</template>

<style>
@viewport {
  min-height: 100vh;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: darkslategrey;
}
#jumbotron {
  padding-left:0px;
}
#add-new-activity {
  position:relative;
  left: 370px;
}
#all-activities {
  padding-top: 0px;
}
.container {
  background-color: white;
  padding-bottom: 99px;
  padding-right: 0px;
  padding-left: 0px;
  min-height: 100vh;
}
#nav {
  padding: 30px;
}
#all-activities {
  font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
  Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
