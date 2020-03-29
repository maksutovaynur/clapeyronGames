<template>
  <div id="app">
<!--    <img alt="Vue logo" src="./assets/logo.png">-->
    <PixiCanvas></PixiCanvas>
  </div>
</template>

<script>
import PixiCanvas from './components/PixiCanvas.vue'

export default {
  name: 'App',
  components: {
    PixiCanvas
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
