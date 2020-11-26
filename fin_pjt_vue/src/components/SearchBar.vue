<template>
  <div class="hello">
    <input v-model="movie-title" @keydown.enter="search" type="text">
    <button @click="search"></button>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    msg: String
  },
  data: function () {
    return {
      movie_title: ''
    }
  },
  methods: {
    search: function () {
      console.log(this.movie_title)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
