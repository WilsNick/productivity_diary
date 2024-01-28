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

body,
html {
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}

body {
  font-family: 'YourPreferredFont', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #000000;
}
</style>
