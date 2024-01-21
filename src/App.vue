<template>
  <div id="app">
    <Header />
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/Header.vue';

export default {
  components: {
    Header,
  },
};
</script>

<style>
#app {
  min-height: 100vh;
  overflow: hidden;
  
}
/* Reset default margin on body and HTML elements */
body, html {
  margin: 0;
  padding: 0;
  /* Dark background color */
  /* background-color: #202124;  */
  /* Light background color */
  background-color: #f4f4f4;
}

/* Optional: Set a default font and other styles */
body {
  font-family: 'YourPreferredFont', sans-serif;
  font-size: 16px;
  line-height: 1.6;

  /* Dark background color */
  /* color: #ffffff;  */
  /* Light background color */
  color: #000000; 
}

</style>
