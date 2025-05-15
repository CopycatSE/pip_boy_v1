<template>
  <div class="container">
    <h1 class="text-center">My Bootstrap Component</h1>
    <button class="btn btn-primary" @click="fetchData">Fetch Data</button>
    <ul class="list-group mt-3">
      <li class="list-group-item" v-for="item in data" :key="item.id">{{ item.data }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: []
    }
  },
  methods: {
    fetchData() {
      fetch("/api/data")
        .then(response => response.json())
        .then(data => {
          this.data = data;
        });
    }
  }
};
</script>
